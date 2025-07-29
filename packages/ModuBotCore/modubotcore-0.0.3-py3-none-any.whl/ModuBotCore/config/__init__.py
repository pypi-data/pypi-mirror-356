import inspect
from typing import ClassVar, get_args, get_origin, get_type_hints

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """
    Base configuration class with runtime type checking for class variables.

    This class automatically validates ClassVar attributes on subclass creation.
    It ensures that the declared types match the actual values provided.

    Supported inner types for ClassVar are:
    - Primitive types: str, int, float, bool
    - Type wrappers, e.g., Type[SomeClass]

    :raises TypeError: If a ClassVar has an invalid or unsupported value/type.
    """

    def __init_subclass__(cls) -> None:
        hints = get_type_hints(cls)

        for attr, declared_type in hints.items():
            if get_origin(declared_type) is not ClassVar:
                continue

            inner_type = get_args(declared_type)[0]
            value = getattr(cls, attr, None)

            if get_origin(inner_type) is type:
                target_type = get_args(inner_type)[0]
                if not inspect.isclass(value) or not issubclass(value, target_type):
                    raise TypeError(
                        f"{attr} must be Type[{target_type.__name__}], got {value}"
                    )
            elif inner_type in (str, int, float, bool):
                if not isinstance(value, inner_type):
                    raise TypeError(
                        f"{attr} must be {inner_type.__name__}, got {type(value).__name__}"
                    )
            else:
                raise TypeError(f"{attr} uses unsupported type {inner_type}")


from .logger import LoggerConfig
