import uuid
from enum import Enum
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .user import Base

class ProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    images = Column(ARRAY(String), nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default=ProductStatus.pending.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    category = relationship("Category", backref="products")
    seller = relationship("User", backref="products")
