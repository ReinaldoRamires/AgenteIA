# src/models.py
import datetime, enum
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class ProjectStatus(enum.Enum):
    PLANNING = "Planning"; ACTIVE = "Active"; COMPLETED = "Completed"; ON_HOLD = "On Hold"; CANCELLED = "Cancelled"

class TaskMode(enum.Enum):
    AUTO = "Auto"; MANUAL = "Manual"

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    notion_page_id = Column(String, unique=True)
    slug = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    project_type = Column(String)
    country = Column(String)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    notion_page_id = Column(String, unique=True)
    template = Column(String)
    dependencies = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    mode = Column(Enum(TaskMode), default=TaskMode.AUTO)
    percent_done = Column(Float, default=0.0)
    raci = Column(JSON)
    dor = Column(String)
    dod = Column(String)
    estimate = Column(Float) # <-- COLUNA ADICIONADA AQUI
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    project = relationship("Project", back_populates="tasks")

class CacheMarket(Base):
    __tablename__ = 'cache_market'
    id = Column(Integer, primary_key=True); sector = Column(String, nullable=False); country = Column(String, nullable=False); data = Column(JSON); fetched_at = Column(DateTime, default=func.now())

class CacheRegulatory(Base):
    __tablename__ = 'cache_regulatory'
    id = Column(Integer, primary_key=True); jurisdiction = Column(String, nullable=False); data = Column(JSON); fetched_at = Column(DateTime, default=func.now())

class Capacity(Base):
    __tablename__ = 'capacity'
    id = Column(Integer, primary_key=True); role = Column(String, unique=True, nullable=False); person_id = Column(String); hours_per_week = Column(Float, nullable=False); updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

def create_db_and_tables(engine):
    Base.metadata.create_all(engine)