from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
import os
from dotenv import load_dotenv

# Schema is what will be in the request and or reponse
from schema import ReportFile as SchemaReportFile
from schema import Comment as CommentSchema
# Model is what will be in the database (Or Database Shape)
from models import ReportFile as ModelReportFile
from models import Comments as CommentModel

load_dotenv('.env')

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "Hello World"}


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
