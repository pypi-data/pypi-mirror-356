from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Specialization(Base):
    __tablename__ = "specializations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    applications: Mapped[list["Application"]] = relationship(back_populates="specialization")