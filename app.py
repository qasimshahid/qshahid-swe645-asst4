from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import constr
from peewee import *
from datetime import date
import json

# Load secrets
with open('db_secret.json') as f:
    secrets = json.load(f)

print(f"Connecting to database with host: {secrets['DB_HOST']} and port: {secrets['DB_PORT']}")

# MySQL DB
db = MySQLDatabase(
    secrets['DB_NAME'],
    user=secrets['DB_USER'],
    password=secrets['DB_PASSWORD'],
    host=secrets['DB_HOST'],
    port=secrets['DB_PORT']
)

# Peewee ORM model
class Survey(Model):
    first_name = CharField()
    last_name = CharField()
    street_address = CharField()
    city = CharField()
    state = CharField()
    zip = CharField()
    telephone = CharField()
    email = CharField()
    date_of_survey = DateField()
    liked_most = CharField(null=True)
    interest_source = CharField(null=True)
    recommend_likelihood = CharField(null=True)
    additional_comments = TextField(null=True)

    class Meta:
        database = db

# Pydantic v2 request model
class SurveyRequest(BaseModel):
    first_name: constr(min_length=1, max_length=255) = Field(..., description="First name is required")
    last_name: constr(min_length=1, max_length=255) = Field(..., description="Last name is required")
    street_address: constr(min_length=1, max_length=255) = Field(..., description="Street address is required")
    city: constr(min_length=1, max_length=255) = Field(..., description="City is required")
    state: constr(min_length=1, max_length=255) = Field(..., description="State is required")
    zip: constr(min_length=1, max_length=20) = Field(..., description="ZIP code is required")
    telephone: constr(min_length=1, max_length=20) = Field(..., description="Telephone number is required")
    email: EmailStr = Field(..., description="Email must be valid")
    date_of_survey: date = Field(..., description="Date of survey is required")
    liked_most: constr(max_length=255) | None = Field(None)
    interest_source: constr(max_length=255) | None = Field(None)
    recommend_likelihood: constr(max_length=255) | None = Field(None)
    additional_comments: constr(max_length=1500) | None = Field(None)

# FastAPI app
app = FastAPI()
db.connect()
db.create_tables([Survey])

# Routes
@app.post("/api/surveys")
def create_survey(survey: SurveyRequest):
    try:
        validate_survey_input(survey)
        new_survey = Survey.create(**survey.model_dump())
        return {"id": new_survey.id, "message": "Survey created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/surveys")
def get_all_surveys():
    try:
        return [s.__data__ for s in Survey.select()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/surveys/{id}")
def get_survey_by_id(id: int):
    try:
        survey = Survey.get(Survey.id == id)
        return survey.__data__
    except Survey.DoesNotExist:
        raise HTTPException(status_code=404, detail="Survey not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/surveys/{id}")
def update_survey(id: int, survey: SurveyRequest):
    try:
        validate_survey_input(survey)
        existing = Survey.get(Survey.id == id)
        for k, v in survey.model_dump().items():
            setattr(existing, k, v)
        existing.save()
        return {"message": "Survey updated successfully"}
    except Survey.DoesNotExist:
        raise HTTPException(status_code=404, detail="Survey not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/surveys/{id}")
def delete_survey(id: int):
    try:
        survey = Survey.get(Survey.id == id)
        survey.delete_instance()
        return {"message": "Survey deleted successfully"}
    except Survey.DoesNotExist:
        raise HTTPException(status_code=404, detail="Survey not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/version")
def get_version_info():
    return HTMLResponse(
        content="""
        <html><head><title>Survey API</title></head><body>
        <h1>Survey API Version</h1>
        <p>Version: 2.0.0.0</p>
        <p>Author: Qasim Shahid - SWE 645</p>
        </body></html>
        """,
        status_code=200
    )

# Manual validations
def validate_survey_input(survey: SurveyRequest):
    VALID_LIKED = ["students", "location", "campus", "atmosphere", "dorm rooms", "sports"]
    VALID_INTEREST = ["friends", "television", "internet", "other"]
    VALID_RECOMMEND = ["very likely", "likely", "unlikely"]

    if survey.liked_most and survey.liked_most.lower().strip() not in VALID_LIKED:
        raise HTTPException(400, f"Invalid liked_most. Must be one of {VALID_LIKED}")

    if survey.interest_source and survey.interest_source.lower().strip() not in VALID_INTEREST:
        raise HTTPException(400, f"Invalid interest_source. Must be one of {VALID_INTEREST}")

    if survey.recommend_likelihood and survey.recommend_likelihood.lower().strip() not in VALID_RECOMMEND:
        raise HTTPException(400, f"Invalid recommend_likelihood. Must be one of {VALID_RECOMMEND}")
