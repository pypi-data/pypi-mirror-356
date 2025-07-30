from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

class AdditionalInfo(Base):
    __tablename__ = "additional_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    registration_address: Mapped[str] = mapped_column(String(255), nullable=False)
    actual_address: Mapped[str] = mapped_column(String(255), nullable=False)
    extra_phones: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    privileges: Mapped[str] = mapped_column(nullable=False)
    military_service: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="additional_info")