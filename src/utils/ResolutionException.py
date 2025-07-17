"""Create class-exception that will be raised when user enter wrong resolution. Lower than 640x480"""


class ResolutionException(Exception):
    def __init__(self, message: str, width: int, height: int) -> None:
        super().__init__(message)
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"{self.width}x{self.height} is too small. Please enter bigger resolution"