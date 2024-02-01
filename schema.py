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
