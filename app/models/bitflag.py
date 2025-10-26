# mixin class
class BitFlag:
    
    def __init__(self, flags_map: dict, flag: int):
        self.flags_map = flags_map
        self.flag = flag
        
    def get_flag(self) -> int:
        return self.flag

    def to_int(self, flags: dict) -> int:
        val = 0
        for i, key in enumerate(self.flags_map.keys()):
            if flags.get(key, self.flags_map[key]):
                val |= (1 << i)
        return val

    def to_dict_flags(self) -> dict:
        res = {}
        for i, key in enumerate(self.flags_map.keys()):
            res[key] = bool(self.flag & (1 << i)) 
        return res

    def set_flags(self, flags: dict):
        if self.flag is None:
            self.flag = 0
        for i, key in enumerate(self.flags_map.keys()):
            if key in flags:
                if flags[key]:
                    self.flag |= (1 << i)
                else:
                    self.flag &= ~(1 << i)
