from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=False)
    direction_id: Mapped[int] = mapped_column(ForeignKey("directions.id"), nullable=False)
    specialization_id: Mapped[int] = mapped_column(ForeignKey("specializations.id"), nullable=False)
    study_form_id: Mapped[int] = mapped_column(ForeignKey("study_forms.id"), nullable=False)
    funding_type: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default='pending')

    user: Mapped["User"] = relationship(back_populates="applications")
    faculty: Mapped["Faculty"] = relationship(back_populates="applications")
    direction: Mapped["Direction"] = relationship(back_populates="applications")
    specialization: Mapped["Specialization"] = relationship(back_populates="applications")
    study_form: Mapped["StudyForm"] = relationship(back_populates="applications")