class Flag:
    DEFAULT_FLAGS = {}

    def __init__(self, flags: int | dict = None, schema: dict = None):
        if schema is not None:
            self.DEFAULT_FLAGS = schema
        if flags is None:
            self.flag = 0
        elif isinstance(flags, int):
            self.flag = flags
        elif isinstance(flags, dict):
            self.flag = self.to_int(flags)
        else:
            raise TypeError("flags must be int or dict")

    def get_flag(self) -> int:
        return self.flag

    def to_int(self, flags: dict) -> int:
        value = 0
        for i, key in enumerate(self.DEFAULT_FLAGS.keys()):
            if flags.get(key, self.DEFAULT_FLAGS[key]):
                value |= (1 << i)
        return value

    def to_dict(self) -> dict:
        result = {}
        for i, key in enumerate(self.DEFAULT_FLAGS.keys()):
            result[key] = bool(self.flag & (1 << i))
        return result

    def set_flags(self, flags: dict):
        for i, key in enumerate(self.DEFAULT_FLAGS.keys()):
            if key in flags:
                if flags[key]:
                    self.flag |= (1 << i)
                else:
                    self.flag &= ~(1 << i)

    def __repr__(self):
        return f"<DatatypeFlag {self.to_dict()} (int={self.flag})>"
