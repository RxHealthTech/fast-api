from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    rating = Column(Float)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship('Author')


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class ReportFile(Base):
    __tablename__ = 'reportFile'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment = Column(String)
    user = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    description = Column(String)
    user = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Uploads(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    original_file_name = Column(String)
    original_file_content = Column(String)
    user = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class ReportSummary(Base):
    __tablename__ = 'report_summary'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    record_owner_id = Column(Integer)  # id of the record owner (i.e. ForNutritionReport.id)
    document_key = Column(String)
    document_html_path = Column(String)
    document_pdf_path = Column(String)
    user = Column(String)
    deleted = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class ForNutritionReport(Base):
    __tablename__ = 'for_nutrition_report'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    machineParam = Column(Integer)  # upload id for machine param
    demographicParam = Column(Integer)  # upload id for demographic param
    description = Column(String)
    user = Column(String)
    deleted = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
