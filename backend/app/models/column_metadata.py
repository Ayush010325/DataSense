from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class ColumnMetadata(Base):
    __tablename__ = "columns_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    column_name = Column(String(255))
    data_type = Column(String(50))
    missing_count = Column(Integer, default=0)
    missing_ratio = Column(Float, default=0.0)
    unique_count = Column(Integer, default=0)
    is_nullable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    dataset = relationship("Dataset", back_populates="columns")
