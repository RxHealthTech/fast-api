from fastapi import FastAPI, UploadFile, File, Form
from typing import Annotated

from fastapi_sqlalchemy import DBSessionMiddleware, db
import os
from dotenv import load_dotenv

# Schema is what will be in the request and or reponse
from schema import ReportFile as SchemaReportFile
from schema import Comment as CommentSchema
from schema import Category as CategorySchema
# Model is what will be in the database (Or Database Shape)
from models import ReportFile as ModelReportFile
from models import Comments as CommentModel
from models import Categories as CategoryModel
from models import Uploads as UploadFileModel

# get is when you want to get data from the database (or list)
# post is when you want to add data to the database (or create)
# put is when you want to update data in the database (or edit)
# delete is when you want to delete data from the database (or remove)

load_dotenv('.env')

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"message": "Api is healthy (Up and Running)"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/report_files')
async def report_files():
    report_files = db.session.query(ModelReportFile).all()
    return report_files


# report_files by Id
@app.get('/report_files/{id}')
async def report_file_by_id(id: int):
    report_file = db.session.query(ModelReportFile).get(id)
    return report_file


@app.post('/report_files', response_model=SchemaReportFile)
async def report_files(report_file: SchemaReportFile):
    db_report_file = ModelReportFile(name=report_file.name, description=report_file.description)
    db.session.add(db_report_file)
    db.session.commit()
    return db_report_file


@app.post("/comment")
async def comment(comment: CommentSchema):
    db_comment = CommentModel(comment=comment.comment, user=comment.user)
    db.session.add(db_comment)
    db.session.commit()
    return db_comment


@app.get("/comments")
async def comments():
    comments = db.session.query(CommentModel).all()
    return comments


@app.delete("/comments/{id}")
async def delete_comment(id: int):
    comment = db.session.query(CommentModel).get(id)
    db.session.delete(comment)
    db.session.commit()
    return {"message": "Comment Deleted"}


@app.post("/category")
async def category(cat: CategorySchema):
    db_category = CategoryModel(category=cat.category, user=cat.user, description=cat.description)
    db.session.add(db_category)
    db.session.commit()
    return db_category


@app.get("/category")
async def get_category():
    categories = db.session.query(CategoryModel).all()
    return categories


@app.delete("/category/{id}")
async def delete_category(id: int):
    category = db.session.query(CategoryModel).get(id)
    db.session.delete(category)
    db.session.commit()
    return {"message": "Category Deleted"}


@app.post("/upload")
async def upload_file(file: UploadFile, name: Annotated[str, Form()], description: Annotated[str, Form()],
                      category: Annotated[str, Form()], user: Annotated[str, Form()]):
    contents = await file.read()
    encoded_file = contents.decode("utf-8")
    db_upload = UploadFileModel(name=name, description=description, category=category, original_file_name=file.filename,
                                user=user, original_file_content=encoded_file)
    db.session.add(db_upload)
    db.session.commit()
    return db_upload
