import asyncio
import inspect
import json
import os
import re # Import re for regex operations
import threading
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Literal, Optional, Type, Union, get_type_hints # Added Literal

import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute # Import APIRoute
from pydantic import BaseModel, create_model
from httpx import HTTPStatusError # Import HTTPStatusError

from brain_sdk.multimodal import Audio, File, Image, Text
from brain_sdk.types import AIConfig, MemoryConfig, WorkflowContext
from brain_sdk.client import BrainClient # Import BrainClient
from brain_sdk.execution_context import ExecutionContext
from brain_sdk.utils import get_free_port

class Agent(FastAPI):
    """Brain Agent - FastAPI subclass for creating AI agent nodes"""

    def __init__(
        self,
        node_id: str,
        brain_server: str = "http://localhost:8080",
        version: str = "1.0.0",
        ai_config: Optional[AIConfig] = None,
        memory_config: Optional[MemoryConfig] = None,
        dev_mode: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.node_id = node_id
        self.brain_server = brain_server
        self.version = version
        self.reasoners = []
        self.skills = []
        self.base_url = None
        self._heartbeat_thread = None
        self._heartbeat_stop_event = threading.Event()
        self.dev_mode = dev_mode
        self.brain_connected = False
        self.client = BrainClient(base_url=brain_server) # Initialize BrainClient
        self._current_execution_context: Optional[ExecutionContext] = None

        # Initialize AI and Memory configurations
        self.ai_config = ai_config if ai_config else AIConfig.from_env() # Use from_env for proper initialization
        self.memory_config = memory_config if memory_config else MemoryConfig(
            auto_inject=[], memory_retention="session", cache_results=False
        )

        # Setup standard Brain routes
        self._setup_brain_routes()

    def _setup_brain_routes(self):
        """Setup standard routes that Brain server expects"""

        @self.get("/health")
        async def health():
            return {
                "status": "healthy",
                "node_id": self.node_id,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
            }

        @self.get("/reasoners")
        async def list_reasoners():
            return {"reasoners": self.reasoners}

        @self.get("/skills")
        async def list_skills():
            return {"skills": self.skills}

        @self.get("/info")
        async def node_info():
            return {
                "node_id": self.node_id,
                "version": self.version,
                "base_url": self.base_url,
                "reasoners": self.reasoners,
                "skills": self.skills,
                "registered_at": datetime.now().isoformat(),
            }

    def reasoner(self, path: Optional[str] = None):
        """
        Decorator to register a reasoner function.

        A reasoner is an AI-powered function that takes input and produces structured output using LLMs.
        It automatically handles input/output schema generation and integrates with the Brain's AI capabilities.

        Args:
            path (str, optional): The API endpoint path for this reasoner. Defaults to /reasoners/{function_name}.
        """

        def decorator(func: Callable) -> Callable:
            # Extract function metadata
            func_name = func.__name__
            endpoint_path = path or f"/reasoners/{func_name}"

            # Get type hints for input/output schemas
            type_hints = get_type_hints(func)
            sig = inspect.signature(func)

            # Create input schema from function parameters
            input_fields = {}
            for param_name, param in sig.parameters.items():
                if param_name not in ["self", "execution_context"]:
                    param_type = type_hints.get(param_name, str)
                    input_fields[param_name] = (param_type, ...)

            InputSchema = create_model(f"{func_name}Input", **input_fields)

            # Get output schema from return type hint
            return_type = type_hints.get("return", dict)

            # Create FastAPI endpoint
            @self.post(endpoint_path, response_model=return_type)
            async def endpoint(input_data: InputSchema, request: Request):
                # Extract execution context from request headers
                execution_context = ExecutionContext.from_request(request, self.node_id)
                
                # Store current context for use in app.call()
                self._current_execution_context = execution_context
                
                # Convert input to function arguments
                kwargs = input_data.dict()
                
                # Inject execution context if the function accepts it
                if 'execution_context' in sig.parameters:
                    kwargs['execution_context'] = execution_context

                # Call the original function
                if asyncio.iscoroutinefunction(func):
                    result = await func(**kwargs)
                else:
                    result = func(**kwargs)

                return result

            # Register reasoner metadata
            output_schema = {}
            if hasattr(return_type, "schema"):
                # If it's a Pydantic model, get its schema
                output_schema = return_type.schema()
            elif hasattr(return_type, "__annotations__"):
                # If it's a typed class, create a simple schema
                output_schema = {"type": "object", "properties": {}}
            else:
                # Default schema for basic types
                output_schema = {"type": "object"}

            self.reasoners.append(
                {
                    "id": func_name,
                    "input_schema": InputSchema.schema(),
                    "output_schema": output_schema,
                    "memory_config": self.memory_config.to_dict(),
                }
            )

            # The `ai` method is available via `self.ai` within the Agent class.
            # If you need to expose it directly on the decorated function,
            # consider a different pattern (e.g., a wrapper class or a global registry).
            return func

        return decorator

    def skill(self, tags: Optional[List[str]] = None, path: Optional[str] = None):
        """
        Decorator to register a skill function.

        A skill is a deterministic function for business logic, integrations, and non-AI operations.
        It automatically handles input/output schema generation.

        Args:
            tags (List[str], optional): A list of tags for organizing and categorizing skills.
            path (str, optional): The API endpoint path for this skill. Defaults to /skills/{function_name}.
        """

        def decorator(func: Callable) -> Callable:
            # Extract function metadata
            func_name = func.__name__
            endpoint_path = path or f"/skills/{func_name}"

            # Get type hints for input schema
            type_hints = get_type_hints(func)
            sig = inspect.signature(func)

            # Create input schema from function parameters
            input_fields = {}
            for param_name, param in sig.parameters.items():
                if param_name not in ["self", "execution_context"]:
                    param_type = type_hints.get(param_name, str)
                    input_fields[param_name] = (param_type, ...)

            InputSchema = create_model(f"{func_name}Input", **input_fields)

            # Get output schema from return type hint
            return_type = type_hints.get("return", dict)

            # Create FastAPI endpoint
            @self.post(endpoint_path, response_model=return_type)
            async def endpoint(input_data: InputSchema, request: Request):
                # Extract execution context from request headers
                execution_context = ExecutionContext.from_request(request, self.node_id)
                
                # Store current context for use in app.call()
                self._current_execution_context = execution_context
                
                # Convert input to function arguments
                kwargs = input_data.dict()
                
                # Inject execution context if the function accepts it
                if 'execution_context' in sig.parameters:
                    kwargs['execution_context'] = execution_context

                # Call the original function
                if asyncio.iscoroutinefunction(func):
                    result = await func(**kwargs)
                else:
                    result = func(**kwargs)

                return result

            # Register skill metadata
            self.skills.append(
                {"id": func_name, "input_schema": InputSchema.schema(), "tags": tags or []}
            )

            return func

        return decorator

    async def ai(
        self,
        *args: Any,
        system: Optional[str] = None,
        user: Optional[str] = None,
        schema: Optional[Type[BaseModel]] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = None,
        response_format: Optional[Literal["auto", "json", "text"]] = None,
        context: Optional[Dict] = None,
        memory_scope: Optional[List[str]] = None,
        **kwargs,
    ) -> Any:
        """
        Universal AI method supporting multimodal inputs with intelligent type detection.

        This method provides a flexible interface for interacting with various LLMs,
        supporting text, image, audio, and file inputs. It intelligently detects
        input types and applies a hierarchical configuration system.

        Args:
            *args: Flexible inputs - text, images, audio, files, or mixed content.
                   - str: Text content, URLs, or file paths (auto-detected).
                   - bytes: Binary data (images, audio, documents).
                   - dict: Structured input with explicit keys (e.g., {"image": "url"}).
                   - list: Multimodal conversation or content list.

            system (str, optional): System prompt for AI behavior.
            user (str, optional): User message (alternative to positional args).
            schema (Type[BaseModel], optional): Pydantic model for structured output validation.
            model (str, optional): Override default model (e.g., "gpt-4", "claude-3").
            temperature (float, optional): Creativity level (0.0-2.0).
            max_tokens (int, optional): Maximum response length.
            stream (bool, optional): Enable streaming response.
            response_format (str, optional): Desired response format ('auto', 'json', 'text').
            context (Dict, optional): Additional context data to pass to the LLM.
            memory_scope (List[str], optional): Memory scopes to inject (e.g., ['workflow', 'session', 'reasoner']).
            **kwargs: Additional provider-specific parameters to pass to the LLM.

        Returns:
            Any: The AI response - raw text, structured object (if schema), or a stream.

        Examples:
            # Simple text input
            response = await app.ai("Summarize this document.")

            # System and user prompts
            response = await app.ai(
                system="You are a helpful assistant.",
                user="What is the capital of France?"
            )

            # Multimodal input with auto-detection (image URL and text)
            response = await app.ai(
                "Describe this image:",
                "https://example.com/image.jpg"
            )

            # Multimodal input with file path (audio)
            response = await app.ai(
                "Transcribe this audio:",
                "./audio.mp3"
            )

            # Structured output with Pydantic schema
            class SentimentResult(BaseModel):
                sentiment: str
                confidence: float

            result = await app.ai(
                "Analyze the sentiment of 'I love this product!'",
                schema=SentimentResult
            )

            # Override default AI configuration parameters
            response = await app.ai(
                "Generate a creative story.",
                model="gpt-4-turbo",
                temperature=0.9,
                max_tokens=500,
                stream=True
            )

            # Complex multimodal conversation
            response = await app.ai([
                {"role": "system", "content": "You are a visual assistant."},
                {"role": "user", "content": "What do you see here?"},
                "https://example.com/chart.png",
                {"role": "user", "content": "Can you explain the trend?"}
            ])
        """
        # Apply hierarchical configuration: Agent defaults < Method overrides < Runtime overrides
        final_config = self.ai_config.copy(deep=True)

        # Apply method-level overrides
        if model:
            final_config.model = model
        if temperature is not None:
            final_config.temperature = temperature
        if max_tokens is not None:
            final_config.max_tokens = max_tokens
        if stream is not None:
            final_config.stream = stream
        if response_format is not None:
            final_config.response_format = response_format

        # TODO: Integrate memory injection based on memory_scope and self.memory_config
        # For now, just pass context if provided
        if context:
            # This would be where memory data is merged into the context
            pass

        # Prepare messages for LiteLLM
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        # Handle flexible user input with intelligent processing
        if user:
            messages.append({"role": "user", "content": user})
        elif args:
            processed_content = self._process_multimodal_args(args)
            if processed_content:
                messages.extend(processed_content)

        # Integrate LiteLLM call here
        try:
            import litellm
        except ImportError:
            raise ImportError("litellm is not installed. Please install it with `pip install litellm`.")

        # Prepare LiteLLM parameters using the config's method
        # This leverages LiteLLM's standard environment variable handling
        litellm_params = final_config.get_litellm_params(
            messages=messages,
            **kwargs  # Runtime overrides have highest priority
        )

        if schema:
            # Use LiteLLM's native Pydantic model support for structured outputs
            litellm_params["response_format"] = schema

        print(f"Making LiteLLM call with params: {litellm_params}")

        try:
            response = await litellm.acompletion(**litellm_params)
            if final_config.stream:
                # For streaming, return the generator
                return response
            else:
                # For non-streaming, return the content
                content = None
                if hasattr(response, 'choices') and response.choices:
                    message = response.choices[0].message
                    if hasattr(message, 'content'):
                        content = message.content

                if content is None:
                    raise ValueError("Received empty response content from LLM.")

                if schema:
                    # Parse JSON response and validate with Pydantic schema
                    try:
                        json_data = json.loads(str(content)) # Ensure content is string
                        return schema(**json_data)
                    except (json.JSONDecodeError, ValueError) as parse_error:
                        print(f"Failed to parse JSON response: {parse_error}")
                        print(f"Raw response: {content}")
                        # Fallback: try to extract JSON from the response
                        json_match = re.search(r'\{.*\}', str(content), re.DOTALL) # Ensure content is string
                        if json_match:
                            try:
                                json_data = json.loads(json_match.group())
                                return schema(**json_data)
                            except:
                                pass
                        # If all else fails, return a default instance or raise
                        raise ValueError(f"Could not parse structured response: {content}")
                return content
        except HTTPStatusError as e:
            print(f"LiteLLM HTTP call failed: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e: # Catch RequestException specifically
            print(f"LiteLLM network call failed: {e}")
            if e.response is not None: # Check if response attribute exists
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            raise
        except Exception as e:
            print(f"LiteLLM call failed: {e}")
            raise

    def _detect_input_type(self, input_data: Any) -> str:
        """Intelligently detect input type without explicit declarations"""
        
        if isinstance(input_data, str):
            # Smart string detection
            if input_data.startswith(('http://', 'https://')):
                return 'image_url' if self._is_image_url(input_data) else 'url'
            elif input_data.startswith('data:image'):
                return 'image_base64'
            elif input_data.startswith('data:audio'):
                return 'audio_base64'
            elif os.path.isfile(input_data):
                ext = os.path.splitext(input_data)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']:
                    return 'image_file'
                elif ext in ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac']:
                    return 'audio_file'
                elif ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.md']:
                    return 'document_file'
                elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']:
                    return 'video_file'
                else:
                    return 'file'
            return 'text'
        
        elif isinstance(input_data, bytes):
            # Detect file type from bytes
            if input_data.startswith(b'\xff\xd8\xff'):  # JPEG
                return 'image_bytes'
            elif input_data.startswith(b'\x89PNG'):  # PNG
                return 'image_bytes'
            elif input_data.startswith(b'GIF8'):  # GIF
                return 'image_bytes'
            elif input_data.startswith(b'RIFF') and b'WAVE' in input_data[:12]:  # WAV
                return 'audio_bytes'
            elif input_data.startswith(b'ID3') or input_data.startswith(b'\xff\xfb'):  # MP3
                return 'audio_bytes'
            elif b'ftyp' in input_data[:20]:  # MP4/M4A
                return 'audio_bytes'
            elif input_data.startswith(b'%PDF'):  # PDF
                return 'document_bytes'
            return 'binary_data'
        
        elif isinstance(input_data, dict):
            # Check for structured input patterns
            if any(key in input_data for key in ['system', 'user', 'assistant', 'role']):
                return 'message_dict'
            elif any(key in input_data for key in ['image', 'image_url', 'audio', 'file', 'text']):
                return 'structured_input'
            return 'dict'
        
        elif isinstance(input_data, list):
            if len(input_data) > 0:
                # Check if it's a conversation format
                if isinstance(input_data[0], dict) and 'role' in input_data[0]:
                    return 'conversation_list'
                # Check if it's multimodal content
                elif any(isinstance(item, (str, dict)) for item in input_data):
                    return 'multimodal_list'
            return 'list'
        
        return 'unknown'

    def _is_image_url(self, url: str) -> bool:
        """Check if URL points to an image based on extension or content type"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg']
        return any(url.lower().endswith(ext) for ext in image_extensions)

    def _is_audio_url(self, url: str) -> bool:
        """Check if URL points to audio based on extension"""
        audio_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac']
        return any(url.lower().endswith(ext) for ext in audio_extensions)

    def _process_multimodal_args(self, args: tuple) -> List[Dict[str, Any]]:
        """Process multimodal arguments into LiteLLM-compatible message format"""
        messages = []
        user_content = []
        
        for arg in args:
            detected_type = self._detect_input_type(arg)
            
            if detected_type == "text":
                user_content.append({"type": "text", "text": arg})
                
            elif detected_type == "image_url":
                user_content.append({
                    "type": "image_url", 
                    "image_url": {"url": arg, "detail": "high"}
                })
                
            elif detected_type == "image_file":
                # Convert file to base64 data URL
                try:
                    import base64
                    with open(arg, "rb") as f:
                        image_data = base64.b64encode(f.read()).decode()
                    ext = os.path.splitext(arg)[1].lower()
                    mime_type = self._get_mime_type(ext)
                    data_url = f"data:{mime_type};base64,{image_data}"
                    user_content.append({
                        "type": "image_url",
                        "image_url": {"url": data_url, "detail": "high"}
                    })
                except Exception as e:
                    print(f"Warning: Could not read image file {arg}: {e}")
                    user_content.append({"type": "text", "text": f"[Image file: {arg}]"})
                    
            elif detected_type == "audio_file":
                # For audio files, we might need transcription first
                # For now, just reference the file
                user_content.append({
                    "type": "text", 
                    "text": f"[Audio file: {os.path.basename(arg)}]"
                })
                
            elif detected_type == "document_file":
                # For documents, we might need to extract text
                # For now, just reference the file
                user_content.append({
                    "type": "text", 
                    "text": f"[Document file: {os.path.basename(arg)}]"
                })
                
            elif detected_type == "image_base64":
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": arg, "detail": "high"}
                })
                
            elif detected_type == "audio_base64":
                user_content.append({
                    "type": "text", 
                    "text": "[Audio data provided]"
                })
                
            elif detected_type == "image_bytes":
                # Convert bytes to base64 data URL
                try:
                    import base64
                    image_data = base64.b64encode(arg).decode()
                    # Try to detect image type from bytes
                    if arg.startswith(b'\xff\xd8\xff'):
                        mime_type = "image/jpeg"
                    elif arg.startswith(b'\x89PNG'):
                        mime_type = "image/png"
                    elif arg.startswith(b'GIF8'):
                        mime_type = "image/gif"
                    else:
                        mime_type = "image/png"  # Default
                    
                    data_url = f"data:{mime_type};base64,{image_data}"
                    user_content.append({
                        "type": "image_url",
                        "image_url": {"url": data_url, "detail": "high"}
                    })
                except Exception as e:
                    print(f"Warning: Could not process image bytes: {e}")
                    user_content.append({"type": "text", "text": "[Image data provided]"})
                    
            elif detected_type == "audio_bytes":
                user_content.append({
                    "type": "text", 
                    "text": "[Audio data provided]"
                })
                
            elif detected_type == "structured_input":
                # Handle dict with explicit keys
                if "system" in arg:
                    messages.append({"role": "system", "content": arg["system"]})
                if "user" in arg:
                    user_content.append({"type": "text", "text": arg["user"]})
                if "text" in arg:
                    user_content.append({"type": "text", "text": arg["text"]})
                if "image" in arg or "image_url" in arg:
                    image_url = arg.get("image") or arg.get("image_url")
                    user_content.append({
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "high"}
                    })
                if "audio" in arg:
                    user_content.append({
                        "type": "text", 
                        "text": f"[Audio: {arg['audio']}]"
                    })
                # Handle other configuration in the dict
                for key, value in arg.items():
                    if key not in ["system", "user", "text", "image", "image_url", "audio"]:
                        # These might be AI configuration overrides
                        pass
                        
            elif detected_type == "message_dict":
                # Handle message format dict
                messages.append(arg)
                
            elif detected_type == "conversation_list":
                # Handle list of messages
                messages.extend(arg)
                
            elif detected_type == "multimodal_list":
                # Handle mixed list of content
                for item in arg:
                    if isinstance(item, str):
                        user_content.append({"type": "text", "text": item})
                    elif isinstance(item, dict):
                        if "role" in item:
                            messages.append(item)
                        else:
                            # Process as structured input
                            sub_messages = self._process_multimodal_args((item,))
                            messages.extend(sub_messages)
                            
            elif detected_type == "dict":
                # Generic dict - convert to text representation
                user_content.append({
                    "type": "text", 
                    "text": f"Data: {json.dumps(arg, indent=2)}"
                })
                
            else:
                # Fallback for unknown types
                user_content.append({"type": "text", "text": str(arg)})
        
        # Add user content as a message if we have any
        if user_content:
            if len(user_content) == 1 and user_content[0]["type"] == "text":
                # Simplify single text content
                messages.append({"role": "user", "content": user_content[0]["text"]})
            else:
                # Multiple content types
                messages.append({"role": "user", "content": user_content})
        
        return messages

    def _get_mime_type(self, extension: str) -> str:
        """Get MIME type from file extension"""
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff',
            '.svg': 'image/svg+xml',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.m4a': 'audio/mp4',
            '.ogg': 'audio/ogg',
            '.flac': 'audio/flac',
            '.aac': 'audio/aac',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.rtf': 'application/rtf'
        }
        return mime_types.get(extension.lower(), 'application/octet-stream')

    async def call(self, target: str, **kwargs) -> Any:
        """
        Initiates a cross-agent call to another reasoner or skill via the Brain execution gateway.

        This method allows agents to seamlessly communicate and utilize reasoners/skills
        deployed on other agent nodes within the Brain ecosystem. It properly propagates
        workflow tracking headers and maintains execution context for DAG building.

        Args:
            target (str): The full target ID in format "node_id.reasoner_name" or "node_id.skill_name"
                         (e.g., "classification_team.classify_ticket", "support_agent.send_email").
            **kwargs: Arguments to pass to the target reasoner/skill.

        Returns:
            Any: The result from the target reasoner/skill execution.

        Examples:
            # Call another agent's reasoner
            sentiment = await app.call("sentiment_agent.analyze_sentiment", 
                                     message="I love this product!", 
                                     customer_id="cust_123")
            
            # Call another agent's skill
            result = await app.call("notification_agent.send_email",
                                  to="user@example.com",
                                  subject="Welcome!",
                                  body="Thank you for signing up.")
        """
        # Get current execution context
        current_context = self._get_current_execution_context()
        
        # Create child context for the cross-agent call
        child_context = current_context.create_child_context()
        
        # Prepare headers with proper workflow tracking
        headers = child_context.to_headers()
        
        # Use the enhanced BrainClient to make the call via execution gateway
        try:
            result = await self.client.execute(
                target=target,
                input_data=kwargs,
                headers=headers
            )
            
            # Extract the actual result from the response
            if isinstance(result, dict) and "result" in result:
                return result["result"]
            else:
                return result
                
        except Exception as e:
            print(f"❌ Cross-agent call failed: {target} - {e}")
            raise

    def _get_current_execution_context(self) -> ExecutionContext:
        """
        Get the current execution context, creating a new one if none exists.
        
        Returns:
            ExecutionContext: Current or new execution context
        """
        if self._current_execution_context:
            return self._current_execution_context
        else:
            # Create a new context if none exists (e.g., for direct agent calls)
            return ExecutionContext.create_new(
                agent_node_id=self.node_id,
                workflow_name=f"{self.node_id}_workflow"
            )

    def _register_with_brain_server(self, port: int):
        """Register this agent node with Brain server"""
        self.base_url = f"http://localhost:{port}"

        # Create complete registration data matching Go backend expectations
        registration_data = {
            "id": self.node_id,
            "team_id": "default",  # Default team for now
            "base_url": self.base_url,
            "version": self.version,
            "reasoners": self.reasoners,
            "skills": self.skills,
            "communication_config": {
                "protocols": ["http"],
                "websocket_endpoint": "",
                "heartbeat_interval": "30s",
            },
            "health_status": "healthy",
            "last_heartbeat": datetime.now().isoformat() + "Z",
            "registered_at": datetime.now().isoformat() + "Z",
            "features": {
                "cloud_analytics": False,
                "ab_testing": False,
                "advanced_metrics": False,
                "compliance": False,
                "audit_logging": False,
                "role_based_access": False,
                "experimental": {},
            },
            "metadata": {
                "deployment": {
                    "environment": "development",
                    "platform": "python",
                    "region": "local",
                    "tags": {"sdk_version": "1.0.0", "language": "python"},
                },
                "performance": {"latency_ms": 0, "throughput_ps": 0},
                "cloud": {
                    "connected": False,
                    "cloud_id": "",
                    "subscription": "",
                    "features": [],
                    "last_sync": datetime.now().isoformat() + "Z",
                },
                "custom": {},
            },
        }

        try:
            print(f"🔗 Attempting to register with Brain server at {self.brain_server}")
            response = requests.post(
                f"{self.brain_server}/api/v1/nodes/register",
                json=registration_data,
                headers={"Content-Type": "application/json"},
                timeout=5,  # Add timeout to fail fast
            )
            if response.status_code != 201:
                print(f"❌ Registration failed with status {response.status_code}")
                print(f"Response: {response.text}")
                try:
                    error_data = response.json()
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                except:
                    pass
            response.raise_for_status()
            print(f"✅ Registered node '{self.node_id}' with Brain server")
            self.brain_connected = True
            return response.json()
        except Exception as e:
            self.brain_connected = False
            if self.dev_mode:
                print(f"⚠️  Brain server not available: {e}")
                print(f"🔧 Running in development mode - agent will work standalone")
                print(f"💡 To connect to Brain server, start it at {self.brain_server}")
                return None
            else:
                print(f"❌ Failed to register with Brain server: {e}")
                if hasattr(e, "response") and e.response is not None:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response text: {e.response.text}")
                raise

    def _send_heartbeat(self):
        """Send heartbeat to Brain server"""
        if not self.brain_connected:
            return  # Skip heartbeat if not connected to Brain
            
        try:
            response = requests.post(
                f"{self.brain_server}/api/v1/nodes/{self.node_id}/heartbeat",
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
            if response.status_code == 200:
                print(f"💓 Heartbeat sent successfully")
            else:
                print(
                    f"⚠️ Heartbeat failed with status {response.status_code}: {response.text}"
                )
        except Exception as e:
            print(f"❌ Failed to send heartbeat: {e}")

    def _heartbeat_worker(self, interval: int = 30):
        """Background worker that sends periodic heartbeats"""
        if not self.brain_connected:
            print("💓 Heartbeat worker skipped - not connected to Brain server")
            return
            
        print(f"💓 Starting heartbeat worker (interval: {interval}s)")
        while not self._heartbeat_stop_event.wait(interval):
            self._send_heartbeat()
        print("💓 Heartbeat worker stopped")

    def _start_heartbeat(self, interval: int = 30):
        """Start the heartbeat background thread"""
        if not self.brain_connected:
            return  # Skip heartbeat if not connected to Brain
            
        if self._heartbeat_thread is None or not self._heartbeat_thread.is_alive():
            self._heartbeat_stop_event.clear()
            self._heartbeat_thread = threading.Thread(
                target=self._heartbeat_worker, args=(interval,), daemon=True
            )
            self._heartbeat_thread.start()

    def _stop_heartbeat(self):
        """Stop the heartbeat background thread"""
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            print("💓 Stopping heartbeat worker...")
            self._heartbeat_stop_event.set()
            self._heartbeat_thread.join(timeout=5)

    def serve(
        self,
        port: Optional[int] = None,
        host: str = "0.0.0.0",
        dev: bool = False,
        heartbeat_interval: int = 2,
        auto_port: bool = False,
        **kwargs,
    ):
        """
        Start the agent node server.

        This method initializes the FastAPI server, registers the agent with the Brain server,
        and starts a background heartbeat to maintain its registration.

        Args:
            port (int, optional): The port on which the agent server will listen. 
                                If None and auto_port is True, will find an available port.
                                Defaults to 8001 if not specified.
            host (str): The host address for the agent server. Defaults to "0.0.0.0".
            dev (bool): If True, enables development mode features (e.g., hot reload, debug UI).
                        Note: `reload` is explicitly set to `False` for uvicorn to avoid import string issues.
            heartbeat_interval (int): The interval in seconds for sending heartbeats to the Brain server.
                                      Defaults to 2 seconds.
            auto_port (bool): If True, automatically find an available port. Defaults to False.
            **kwargs: Additional keyword arguments to pass to `uvicorn.run`.
        """
        # Handle port assignment
        if port is None:
            if auto_port or os.getenv('BRAIN_AUTO_PORT') == 'true':
                try:
                    port = get_free_port()
                    print(f"🔍 Auto-assigned port: {port}")
                except RuntimeError as e:
                    print(f"❌ Failed to find free port: {e}")
                    port = 8001  # Fallback to default
            else:
                port = 8001  # Default port
        
        print(f"🚀 Starting agent node '{self.node_id}' on port {port}")

        # Register with Brain server
        self._register_with_brain_server(port)

        # Start heartbeat worker
        self._start_heartbeat(heartbeat_interval)

        print(f"🌐 Agent server running at http://{host}:{port}")
        print("📡 Available endpoints:")
        for route in self.routes:
            # Check if the route is an APIRoute (has .path and .methods)
            if isinstance(route, APIRoute):
                for method in route.methods:
                    if method != "HEAD":  # Skip HEAD methods
                        print(f"  {method} {route.path}")

        try:
            # Start FastAPI server - disable reload to avoid import string issues
            uvicorn.run(
                self,
                host=host,
                port=port,
                reload=False,  # Disable reload to avoid import string requirement
                **kwargs,
            )
        finally:
            # Ensure heartbeat is stopped when server shuts down
            self._stop_heartbeat()
