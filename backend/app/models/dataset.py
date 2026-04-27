from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), index=True)
    filename = Column(String(255))
    file_path = Column(String(512))
    row_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    columns = relationship("ColumnMetadata", back_populates="dataset", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="dataset", cascade="all, delete-orphan")
