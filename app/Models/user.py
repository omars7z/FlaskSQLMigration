from app.Util.base_model import BaseModel2
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import Mapped, Integer, String, Optional
from datetime import datetime

class User(BaseModel2):
    
    flags_map = {
        "isActive": False,
        "isSuperAdmin": False
    }
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String(512))
    token: Mapped[str] = mapped_column(String(256))
    flag: Mapped[Optional[str]] = mapped_column(Integer, default=0)
    time_created: Mapped[datetime] = mapped_column(default=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "flag": self.flag,
            "flags_map": self.to_dict_flags(),
        }