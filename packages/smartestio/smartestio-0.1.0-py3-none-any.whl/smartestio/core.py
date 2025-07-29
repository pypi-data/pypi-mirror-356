_input_buffer = []

def reset():
    """Clears the internal input buffer. Useful for testing or reuse."""
    global _input_buffer
    _input_buffer = []

def smart_input():
    """
    Replacement for built-in input().
    It returns the next token from a buffered line of input.
    Example: if input is '3 4 5', each call returns '3', then '4', then '5'.
    """
    global _input_buffer
    while not _input_buffer:
        _input_buffer = input.__original__().split()
    return _input_buffer.pop(0)

def smart_int():
    """Returns as an int."""
    return int(input())

def smart_float():
    """Returns as a float."""
    return float(input())

def smart_str():
    """Returns as a string (identical to input)."""
    return input()

input.__original__ = __builtins__.input
