from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class StudyForm(Base):
    __tablename__ = "study_forms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    applications: Mapped[list["Application"]] = relationship(back_populates="study_form")