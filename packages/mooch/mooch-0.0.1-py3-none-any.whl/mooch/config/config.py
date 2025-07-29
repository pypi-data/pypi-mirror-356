from __future__ import annotations

from pathlib import Path
from typing import Any

from trapdoor import Trapdoor


class Config:
    def __init__(self, settings_filepath: str, default_settings: dict | None = None) -> None:
        if default_settings is None:
            default_settings = {}
        p = Path(settings_filepath)
        directory = str(p.parent)
        filename = p.name
        self._trapdoor = Trapdoor(store_name="", store_directory=directory, config_filename=filename)

        self._set_defaults(default_settings)

    def _set_defaults(self, d: dict, parent_key: str = "") -> None:
        for k, v in d.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            if self.get(full_key) is None:
                self.set(full_key, v)

            elif isinstance(v, dict):
                self._set_defaults(v, full_key)

    def get(self, key: str) -> Any | None:  # noqa: ANN401
        """Return a value from the configuration by key.

        Args:
        key (str): The key to return a value from.

        Returns:
        Any | None: The value associated with the key, or None if the key does not exist.

        """
        return self._trapdoor.get(key)

    def __getitem__(self, key: str) -> Any | None:  # noqa: ANN401
        """Get an item from the configuration by key."""
        return self.get(key)

    def set(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set a value in the configuration by key.

        Args:
        key (str): The key to store the value under.
        value (Any): The value to set for the key.

        Returns:
        None

        """
        self._trapdoor.set(key, value)

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set an item in the configuration by key."""
        self.set(key, value)
