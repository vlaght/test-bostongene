from enum import Enum as PythonEnum

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text, func

from models.database import Base


class ProcessingStatus(str, PythonEnum):
    pending = 'pending'  # Ожидает обработки
    working = 'working'  # В обработке
    failing = 'failing'  # Ошибка
    success = 'success'  # Обработан


class File(Base):
    __tablename__ = 'File'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    log = Column(Text, nullable=True)
    md5 = Column(String(32), nullable=True)
    status = Column(
        Enum(ProcessingStatus, name='processing_status'),
        server_default=ProcessingStatus.pending,
        nullable=False,
    )
    path = Column(String(250), nullable=False)
    size = Column(Integer, nullable=False)
    created_dt = Column(DateTime, nullable=False, default=func.now())
    updated_dt = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
