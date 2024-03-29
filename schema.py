from pydantic import BaseModel


class Book(BaseModel):
    title: str
    rating: int
    author_id: int

    class Config:
        from_attributes = True


class Author(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class ReportFile(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class Comment(BaseModel):
    comment: str
    user: str

    class Config:
        from_attributes = True


class Category(BaseModel):
    category: str
    description: str
    user: str

    class Config:
        from_attributes = True


class Upload(BaseModel):
    id: int
    name: str
    category: str
    description: str
    original_file_name: str
    user: str

    class Config:
        from_attributes = True


class ReportSummary(BaseModel):
    name: str
    category: str
    record_owner_id: int
    document_key: str
    document_html_path: str
    document_pdf_path: str
    user: str

    class Config:
        from_attributes = True


class ForNutritionReport(BaseModel):
    name: str
    machineParam: int
    demographicParam: int
    description: str
    user: str

    class Config:
        from_attributes = True
