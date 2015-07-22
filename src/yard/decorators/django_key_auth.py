from keyauth.decorators import key_required as original_key_required
from .utils import to_yard_decorator

@to_yard_decorator
def key_required():
    return original_key_required
