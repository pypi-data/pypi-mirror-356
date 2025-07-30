from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Date
from datetime import date as py_date

class PassportData(Base):
    __tablename__ = "passport_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    passport_series_number: Mapped[str] = mapped_column(String(20))
    issue_date: Mapped[py_date] = mapped_column(Date)
    issuing_authority: Mapped[str] = mapped_column(String(100))
    authority_code: Mapped[str] = mapped_column(String(10))
    place_of_birth: Mapped[str] = mapped_column(String(150))
    date_of_birth: Mapped[py_date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(10))
    nationality: Mapped[str] = mapped_column(String(50))

    user: Mapped["User"] = relationship(back_populates="passport_data")