from fastapi import FastAPI, UploadFile, File, Form
from typing import Annotated

from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.orm import load_only
import os
from dotenv import load_dotenv

# Schema is what will be in the request and or reponse
from schema import ReportFile as SchemaReportFile
from schema import Comment as CommentSchema
from schema import Category as CategorySchema
from schema import Upload as UploadFileSchema
from schema import ReportSummary as ReportSummarySchema
from schema import ForNutritionReport as ForNutritionReportSchema
# Model is what will be in the database (Or Database Shape)
from models import ReportFile as ModelReportFile
from models import Comments as CommentModel
from models import Categories as CategoryModel
from models import Uploads as UploadFileModel
from models import ReportSummary as ReportSummaryModel
from models import ForNutritionReport as ForNutritionReportModel

# get is when you want to get data from the database (or list)
# post is when you want to add data to the database (or create)
# put is when you want to update data in the database (or edit)
# delete is when you want to delete data from the database (or remove)

load_dotenv('.env')

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "Api is healthy (Up and Running)"}


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


@app.get("/upload", response_model=list[UploadFileSchema])
async def get_uploads():
    query = db.session.query().with_entities(UploadFileModel.id, UploadFileModel.name, UploadFileModel.category,
                                             UploadFileModel.description, UploadFileModel.original_file_name,
                                             UploadFileModel.user)
    uploads = query.all()
    return uploads


@app.delete("/upload/{id}")
async def delete_upload(id: int):
    upload = db.session.query(UploadFileModel).get(id)
    db.session.delete(upload)
    db.session.commit()
    return {"message": "Upload Deleted"}


# Report Summary Section
@app.get("/report_summary")
async def get_report_summary():
    reports = db.session.query(ReportSummaryModel).filter(ReportSummaryModel.deleted != 1).all()
    return reports


@app.post('/report_summary')
async def create_report_summary(report: ReportSummarySchema):
    db_report = ReportSummaryModel(name=report.name, category=report.category, record_owner_id=report.record_owner_id,
                                   document_key=report.document_key, document_html_path=report.document_html_path,
                                   document_pdf_path=report.document_pdf_path, user=report.user)
    db.session.add(db_report)
    db.session.commit()
    return db_report


@app.delete('/report_summary/{id}')
async def delete_report_summary(id: int):
    report = db.session.query(ReportSummaryModel).get(id)
    report.deleted = 1
    db.session.commit()
    return {"message": "Report Deleted"}


# Nutrition Report Section

@app.get("/report/nutrition")
async def generate_nutrition_report():
    reports = db.session.query(ForNutritionReportModel).filter(ForNutritionReportModel.deleted != 1).all()
    return reports


@app.get("/report/nutrition/{id}")
async def get_nutrition_report_by_id(id: int):
    report = db.session.query(ForNutritionReportModel).get(id)
    return report


@app.post('/report/nutrition')
async def generate_nutrition_report(report: ForNutritionReportSchema):
    db_report = ForNutritionReportModel(name=report.name, machineParam=report.machineParam,
                                        demographicParam=report.demographicParam, description=report.description,
                                        user=report.user)
    db.session.add(db_report)
    db.session.commit()
    return db_report


@app.delete('/report/nutrition/{id}')
async def delete_nutrition_report(id: int):
    report = db.session.query(ForNutritionReportModel).get(id)
    report.deleted = 1
    db.session.commit()
    return {"message": "Report Deleted"}
