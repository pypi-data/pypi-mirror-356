from enum import IntEnum


class SizeUnit(IntEnum):
    BYTES = 1
    KILOBYTES = 1024
    MEGABYTES = 1024**2
    GIGABYTES = 1024**3


class ValidatorConfig:
    def __init__(
        self,
        *,
        max_size: int = 0,
        size_unit: SizeUnit | str = SizeUnit.BYTES,
        allowed_types: dict[str, list[str]] = None,
        is_validate_extension: bool = True,
        is_validate_mime_type: bool = True,
        is_cross_validation: bool = True,
    ) -> None:
        """
        Args:
        max_size (int): Maximum file size in specified units of measurement.
            When set to 0, size validation is disabled. Default is 0.
        size_unit (SizeUnit | str): Unit of measurement for max_size.
            Can be SizeUnit enum or string ('B', 'KB', 'MB', 'GB', 'bytes',
            'kilobytes', 'megabytes', 'gigabytes'). Supports Russian names
            ('байт', 'килобайт', 'мегабайт', 'гигабайт'). Default is
            SizeUnit.BYTES.
        allowed_types (dict[str, list[str]]): Dictionary of allowed
            MIME types and their corresponding file extensions. Key is MIME type
            (e.g., 'image/jpeg'), value is list of allowed extensions
            (e.g., ['jpg', 'jpeg']). When None, MIME type validation and extension
            validation and cross-validation is disabled. Default is None.

            Example:
            {
                'image/jpeg': ['jpg', 'jpeg'],
                'image/png': ['png'],
            }
        is_validate_extension (bool): Enable file extension validation.
            Only works when allowed_types is provided. Checks that the file
            has an extension and it's in the allowed list. Default is True.
        is_validate_mime_type (bool): Enable MIME type validation for files.
            Only works when allowed_types is provided. Checks that the file
            has a MIME type and it's in the allowed list. Default is True.
        is_cross_validation (bool): Enable cross-validation of file extension
            against its MIME type. Only works when allowed_types is provided.
            Checks that the file extension corresponds to the specified
            MIME type. Default is True.
        """
        if isinstance(size_unit, str):
            size_unit = self.__parse_size_unit(size_unit)

        self.max_size = max_size * size_unit
        if self.max_size < 0:
            raise ValueError('max_size must be non-negative')

        self.allowed_types = allowed_types

        self._is_validate_size = bool(self.max_size)
        self._is_validate_extension = is_validate_extension and bool(self.allowed_types)
        self._is_validate_mime_type = is_validate_mime_type and bool(self.allowed_types)
        self._is_cross_validation = is_cross_validation and bool(self.allowed_types)

    def __parse_size_unit(
        self,
        size_unit: str,
    ) -> SizeUnit:
        """Parse size unit for str type.

        Args:
            size_unit (str): Size unit

        Raises:
            ValueError: If size unit is invalid

        Returns:
            SizeUnit: Parsed size unit
        """
        size_unit = size_unit.lower().strip()

        if size_unit in [
            'b',
            'byte',
            'bytes',
            'byte(s)',
            'bytes(s)',
            'б',
            'байт',
            'байтов',
            'байта',
            'байты',
            'байт(ы)',
            'байт(ов)',
            'байт(а)',
        ]:
            return SizeUnit.BYTES
        elif size_unit in [
            'kb',
            'kbyte',
            'kbytes',
            'kbyte(s)',
            'kbytes(s)',
            'кб',
            'килобайт',
            'килобайт',
            'килобайтов',
            'килобайта',
            'килобайты',
            'килобайт(ы)',
            'килобайт(ов)',
            'килобайт(а)',
        ]:
            return SizeUnit.KILOBYTES
        elif size_unit in [
            'mb',
            'mbyte',
            'mbytes',
            'mbyte(s)',
            'mbytes(s)',
            'мб',
            'мегабайт',
            'мегабайтов',
            'мегабайта',
            'мегабайты',
            'мегабайт(ы)',
            'мегабайт(ов)',
            'мегабайт(а)',
        ]:
            return SizeUnit.MEGABYTES
        elif size_unit in [
            'gb',
            'gbyte',
            'gbytes',
            'gbyte(s)',
            'gbytes(s)',
            'гб',
            'гигабайт',
            'гигабайтов',
            'гигабайта',
            'гигабайты',
            'гигабайт(ы)',
            'гигабайт(ов)',
            'гигабайт(а)',
        ]:
            return SizeUnit.GIGABYTES
        else:
            raise ValueError(f"Invalid size unit: {size_unit}")

    def get_allowed_extensions(self) -> set[str]:
        """Get allowed extensions

        Returns:
            set[str]: Set of allowed extensions
        """
        return set(sum(self.allowed_types.values(), []))
