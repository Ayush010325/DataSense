from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    name = Column(String(255), index=True)
    task_type = Column(String(50))
    target_column = Column(String(255), nullable=True)
    model_type = Column(String(100))
    feature_columns = Column(JSON)
    preprocessing_config = Column(JSON)
    metrics_json = Column(JSON)
    model_filepath = Column(String(512))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    dataset = relationship("Dataset", back_populates="experiments")
