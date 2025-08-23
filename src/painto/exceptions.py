

# Two of these so list lookups can raise errors like list lookups, and
# attribute lookups can raise errors like attribute lookups.
class ColorNotFoundError(LookupError):
    def __init__(self, color: str) -> None:
        super().__init__(f"Color not found in any color list: {color}")

class ColorAttributeNotFoundError(AttributeError):
    def __init__(self, color: str) -> None:
        super().__init__(f"Color not found in any color list: {color}")

class ColorRangeError(ValueError):
    def __init__(self, steps: int) -> None:
        super().__init__(f"Color range steps must be greater than 0, got {steps}")

class InvalidHexStringError(ValueError):
    def __init__(self, hex_str: str) -> None:
        msg = f"Invalid hex string ({hex_str}). Format ust be one of: #RRGGBB, #RRGGBBAA, or #RGB"
        super().__init__(msg)

class RequestsRequiredError(ImportError):
    def __init__(self) -> None:
        super().__init__("requests is required for this functionality")
