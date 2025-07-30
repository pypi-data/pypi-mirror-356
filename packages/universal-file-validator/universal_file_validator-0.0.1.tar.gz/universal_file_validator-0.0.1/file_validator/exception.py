class FileValidationError(Exception):
    """Base exception for file validation errors."""

    pass


class FileSizeError(FileValidationError):
    """Raised when file size exceeds the limit."""

    pass


class FileSizeDisabledError(FileValidationError):
    """Raised when file size exceeds the limit."""

    pass


class FileMimeTypeError(FileValidationError):
    """Raised when MIME type is invalid."""

    pass


class FileMimeTypeDisabledError(FileValidationError):
    """Raised when MIME type is invalid."""

    pass


class FileExtensionError(FileValidationError):
    """Raised when file extension is invalid or missing."""

    pass


class FileExtensionDisabledError(FileValidationError):
    """Raised when file extension is invalid or missing."""

    pass


class FileExtensionMimeTypeMismatchError(FileValidationError):
    """Raised when extension doesn't match MIME type."""

    pass


class FileExtensionMimeTypeMismatchDisabledError(FileValidationError):
    """Raised when extension doesn't match MIME type."""

    pass
