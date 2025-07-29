
class ExtractionError(Exception):
    """General exception for extraction failures."""
    pass

class UnsupportedFormatError(ExtractionError):
    """Raised when the file format is not supported."""
    pass

class FileReadError(ExtractionError):
    """Raised when the input file cannot be read or parsed."""
    pass
