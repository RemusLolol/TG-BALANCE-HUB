from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    services = relationship("Service", back_populates="user", cascade="all, delete-orphan")


class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String, nullable=False)
    connection_type = Column(String, nullable=False)  # api, oauth, email
    credentials = Column(JSON, nullable=False)  # Зашифрованные данные
    is_active = Column(Boolean, default=True)
    check_interval = Column(Integer, default=3600)  # секунды
    created_at = Column(DateTime, default=datetime.utcnow)
    last_check = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="services")
    balances = relationship("BalanceHistory", back_populates="service", cascade="all, delete-orphan")


class BalanceHistory(Base):
    __tablename__ = "balance_history"
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    balance = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="OK")
    checked_at = Column(DateTime, default=datetime.utcnow)
    
    service = relationship("Service", back_populates="balances")
