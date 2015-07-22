from throttling.decorators import throttle as original_throttle
from .utils import to_yard_decorator

@to_yard_decorator
def throttle():
    return original_throttle
