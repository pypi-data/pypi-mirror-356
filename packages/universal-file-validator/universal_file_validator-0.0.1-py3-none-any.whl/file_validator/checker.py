import asyncio
import functools
from typing import Any, Awaitable, Callable, Type, TypeVar
from file_validator.config import ValidatorConfig
from file_validator.exception import (
    FileExtensionDisabledError,
    FileExtensionMimeTypeMismatchDisabledError,
    FileMimeTypeDisabledError,
    FileSizeDisabledError,
)

SyncFunc = TypeVar('SyncFunc', bound=Callable[..., Any])
AsyncFunc = TypeVar('AsyncFunc', bound=Callable[..., Awaitable[Any]])
ParentClass = TypeVar("ParentClass", bound=ValidatorConfig)


def require_validation(
    validation_attr: str,
    error_class: Type[Exception],
    error_message: str,
) -> Callable[[SyncFunc | AsyncFunc], SyncFunc | AsyncFunc]:
    """
    Universal decorator for checking validation

    Args:
        validation_attr: Name of validation attribute, e.g. '_is_validate_size'
        error_message: Error message
    """

    def decorator(func: SyncFunc | AsyncFunc) -> SyncFunc | AsyncFunc:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(
                self: ParentClass,
                *args: Any,
                **kwargs: Any,
            ) -> Any:
                if not getattr(self, validation_attr, False):
                    raise error_class(error_message)
                return await func(self, *args, **kwargs)

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(self: ParentClass, *args: Any, **kwargs: Any) -> Any:
                if not getattr(self, validation_attr, False):
                    raise error_class(error_message)
                return func(self, *args, **kwargs)

            return sync_wrapper

    return decorator


require_size_validation = require_validation(
    validation_attr='_is_validate_size',
    error_class=FileSizeDisabledError,
    error_message="File size validation is disabled",
)

require_extension_validation = require_validation(
    validation_attr='_is_validate_extension',
    error_class=FileExtensionDisabledError,
    error_message="Extension validation is disabled",
)

require_mime_type_validation = require_validation(
    validation_attr='_is_validate_mime_type',
    error_class=FileMimeTypeDisabledError,
    error_message="MIME type validation is disabled",
)

require_cross_validation = require_validation(
    validation_attr='_is_cross_validation',
    error_class=FileExtensionMimeTypeMismatchDisabledError,
    error_message="Cross validation is disabled",
)
