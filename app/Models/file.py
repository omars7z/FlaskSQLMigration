from app.Models.base import BaseDBModel
from typing import Optional
from sqlalchemy import Integer, String, DateTime, BigInteger, Text, UUID, ForeignKey
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

class File(BaseDBModel):
    
    __tablename__ = "files"
    
    
    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)  
    time_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    uploader_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, default=1
        )
    uploader = relationship("User", back_populates="files")
    
    