import platform
import sys

from mooch.require.exceptions import RequirementError


def python_version(python_version: str) -> None:
    """Throws an error if the current Python version is not compatible with the required one.

    Args:
        python_version (str): The Python version required. (e.g., '3.12').

    Returns:
        None

    """
    r = [int(x) for x in python_version.split(".")]
    msg = f"This package requires Python version {r[0]}.{r[1]}. "
    f"Current version is {sys.version_info[0]}.{sys.version_info[1]}"

    if sys.version_info[0] < r[0]:
        raise RequirementError(msg)

    if r[0] == sys.version_info[0] and sys.version_info[1] < r[1]:
        raise RequirementError(msg)


def operating_system(operating_system_name: str) -> None:
    """Throws an error if the current operating system does not match the required one.

    Args:
        operating_system_name (str): The name of the required operating system. (e.g., 'Windows', 'Linux', 'Darwin').

    Returns:
        None

    """
    if operating_system_name.lower() != platform.system().lower():
        msg = f"This package requires '{operating_system_name}' operating system. Current OS is: " + platform.system()
        raise RequirementError(msg)
