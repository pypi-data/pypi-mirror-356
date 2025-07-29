def str2bool(value: str) -> bool:
    """
    Convert a string representation to a boolean value.

    Common truthy values include: "yes", "true", "t", "y", "1" (case-insensitive).

    :param value: Input string to convert.
    :type value: str
    :return: True if the value is considered truthy, False otherwise.
    :rtype: bool
    """
    return value.lower() in ("yes", "true", "t", "y", "1")
