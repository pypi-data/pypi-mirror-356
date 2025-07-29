from functools import wraps
from brain_sdk.types import ReasonerDefinition, SkillDefinition

def reasoner(reasoner_id: str, input_schema: dict, output_schema: dict):
    """Decorator to mark a function as a reasoner"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Attach metadata to the function
        wrapper._reasoner_def = ReasonerDefinition(
            id=reasoner_id,
            input_schema=input_schema,
            output_schema=output_schema
        )
        return wrapper
    return decorator

# TODO: Add @skill decorator
