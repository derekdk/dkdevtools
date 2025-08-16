"""dk-sayhi example package."""

__all__ = ["say_hi"]


def say_hi(name: str = "World") -> str:
    return f"Hi, {name}!"
