from app.models.datatypeflags import DatatypeFlag

class BitwiseMixin:
    """Reusable mixin for models that use a bitwise flag column."""

    FLAG_CLASS = DatatypeFlag  # Override in subclass if needed
    FLAG_FIELD = "flag"        # Name of the integer column in the model

    # flag utilities methods

    def _get_flag_value(self) -> int:
        return getattr(self, self.FLAG_FIELD, 0) or 0

    def _set_flag_value(self, value: int):
        setattr(self, self.FLAG_FIELD, value)

    def _flag_obj(self) -> DatatypeFlag:
        """Return a Flag object for the current value."""
        return self.FLAG_CLASS(self._get_flag_value())

    def flags_map(self) -> dict:
        """Return current flag state as booleans dict."""
        return self._flag_obj().to_dict()

    def can(self, key: str) -> bool:
        """Check if a permission is enabled."""
        flags = self._flag_obj()
        return flags.to_dict().get(key, False)

    def enable(self, key: str):
        """Enable a specific flag by name."""
        flags = self._flag_obj()
        flags.set_permissions({key: True})
        self._set_flag_value(flags.get_flag())
        return self

    def disable(self, key: str):
        """Disable a specific flag by name."""
        flags = self._flag_obj()
        flags.set_permissions({key: False})
        self._set_flag_value(flags.get_flag())
        return self

    def reset_flags(self):
        """Reset all flags to their default values."""
        default_flag = self.FLAG_CLASS().get_flag()
        self._set_flag_value(default_flag)
        return self

    def update_flags(self, updates: dict):
        """Bulk update multiple flags at once."""
        flags = self._flag_obj()
        flags.set_permissions(updates)
        self._set_flag_value(flags.get_flag())
        return self
