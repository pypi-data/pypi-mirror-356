import re

def remove_think_block(text: str) -> str:
    """
    Removes the <think>...</think> block (including tags and content) from the input string.
    """
    return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)

def yellow(text: str) -> str:
    """Return text colored yellow for terminal output."""
    return f"\033[33m{text}\033[0m"
