import asyncio
from io import BytesIO
from pathlib import Path
from typing import Union
import os

from file_validator.checker import (
    require_size_validation,
    require_extension_validation,
    require_mime_type_validation,
)
from file_validator.config import ValidatorConfig
from file_validator.exception import (
    FileExtensionError,
    FileExtensionMimeTypeMismatchError,
    FileMimeTypeError,
    FileSizeError,
)

try:
    from magic import Magic
except ImportError:
    raise ImportError(
        "python-magic is required. Install it with: pip install python-magic"
    )


class FileValidator(ValidatorConfig):
    @require_size_validation
    def validate_size(self, file_data: bytes | BytesIO) -> None:
        """
        Validate file size, if validation is enabled (max_size != 0).

        Args:
            file_data (bytes | BytesIO): File content

        Raises:
            FileSizeError: If file size exceeds the limit
        """
        if isinstance(file_data, bytes):
            size = len(file_data)
        elif isinstance(file_data, BytesIO):
            current_pos = file_data.tell()
            file_data.seek(0, os.SEEK_END)
            size = file_data.tell()
            file_data.seek(current_pos)
        else:
            raise ValueError("file_data must be bytes or BytesIO")

        if size > self.max_size:
            raise FileSizeError('File size exceeds the limit')

    @require_extension_validation
    def validate_extension_exists(self, filename: str) -> str:
        """
        Validate that file has an extension.

        Args:
            filename: Name of the file

        Returns:
            str: File extension in lowercase (without dot)

        Raises:
            FileExtensionError: If file has no extension
        """
        if not filename:
            raise FileExtensionError("Filename is empty")

        file_path = Path(filename)
        if not file_path.suffix:
            raise FileExtensionError("File has no extension")

        extension = file_path.suffix[1:].lower()
        if not extension:
            raise FileExtensionError("File extension is empty")

        return extension

    @require_extension_validation
    def validate_extension_allowed(self, extension: str) -> None:
        """
        Validate that extension is in allowed extensions.

        Args:
            extension: File extension (without dot)

        Raises:
            FileExtensionError: If extension is not allowed
        """
        extension = extension.lower()

        allowed_extensions = self.get_allowed_extensions()

        if extension not in allowed_extensions:
            raise FileExtensionError(
                f"Extension '{extension}' is not allowed. Allowed extensions: "
                + ', '.join(allowed_extensions),
            )

    @require_mime_type_validation
    def detect_mime_type(self, file_data: bytes | BytesIO) -> str:
        """
        Detect MIME type from file content.

        Args:
            file_data: File content as bytes or BytesIO

        Returns:
            str: Detected MIME type
        """
        if isinstance(file_data, bytes):
            content = file_data
        elif isinstance(file_data, BytesIO):
            current_pos = file_data.tell()
            file_data.seek(0)
            content = file_data.read()
            file_data.seek(current_pos)
        else:
            raise ValueError("file_data must be bytes or BytesIO")

        return Magic(mime=True).from_buffer(content)

    @require_mime_type_validation
    async def adetect_mime_type(self, file_data: bytes | BytesIO) -> str:
        """
        Detect MIME type from file content asynchronously.

        Args:
            file_data: File content as bytes or BytesIO

        Returns:
            str: Detected MIME type
        """
        try:
            return await asyncio.to_thread(self.detect_mime_type, file_data)
        except Exception:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.detect_mime_type, file_data)

    @require_mime_type_validation
    def validate_mime_type_allowed(self, mime_type: str) -> None:
        """
        Validate that MIME type is in allowed MIME types.

        Args:
            mime_type: MIME type to validate

        Raises:
            FileMimeTypeError: If MIME type is not allowed
        """
        if mime_type not in self.allowed_types.keys():
            raise FileMimeTypeError(
                f"MIME type '{mime_type}' is not allowed. "
                f"Allowed MIME types: {list(self.allowed_types.keys())}"
            )

    @require_mime_type_validation
    def validate_extension_mime_match(self, extension: str, mime_type: str) -> None:
        """
        Validate that extension matches MIME type.

        Args:
            extension: File extension (without dot)
            mime_type: MIME type

        Raises:
            FileExtensionMimeTypeMismatchError: If extension doesn't match MIME type
        """
        extension = extension.lower()

        allowed_extensions_for_mime = self.allowed_types[mime_type]

        if extension not in allowed_extensions_for_mime:
            raise FileExtensionMimeTypeMismatchError(
                f"Extension '{extension}' doesn't match MIME type '{mime_type}'. "
                f"Expected extensions for this MIME type: {allowed_extensions_for_mime}"
            )

    def validate_all(
        self, file_data: bytes | BytesIO, filename: str
    ) -> tuple[str, str]:
        """
        Perform complete file validation.

        Args:
            file_data: File content as bytes or BytesIO
            filename: Name of the file

        Raises:
            FileValidationError: If any validation fails

        Returns:
            tuple[str, str]: (extension, mime_type)
        """
        # 1. Validate size
        self.validate_size(file_data)

        # 2. Validate extension exists
        extension = self.validate_extension_exists(filename)

        # 3. Validate extension is allowed
        self.validate_extension_allowed(extension)

        # 4. Detect MIME type
        mime_type = self.detect_mime_type(file_data)

        # 5. Validate MIME type is allowed
        self.validate_mime_type_allowed(mime_type)

        # 6. Validate extension matches MIME type
        self.validate_extension_mime_match(extension, mime_type)

        return extension, mime_type

    async def avalidate_all(
        self, file_data: bytes | BytesIO, filename: str
    ) -> tuple[str, str]:
        """
        Perform complete file validation asynchronously.

        Args:
            file_data: File content as bytes or BytesIO
            filename: Name of the file

        Raises:
            FileValidationError: If any validation fails

        Returns:
            Tuple[str, str]: (extension, mime_type)
        """
        # 1. Validate size
        self.validate_size(file_data)

        # 2. Validate extension exists
        extension = self.validate_extension_exists(filename)

        # 3. Validate extension is allowed
        self.validate_extension_allowed(extension)

        # 4. Detect MIME type asynchronously
        mime_type = await self.adetect_mime_type(file_data)

        # 5. Validate MIME type is allowed
        self.validate_mime_type_allowed(mime_type)

        # 6. Validate extension matches MIME type
        self.validate_extension_mime_match(extension, mime_type)

        return extension, mime_type
