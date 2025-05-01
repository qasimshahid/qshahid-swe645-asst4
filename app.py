#  Qasim Shahid SWE 645 - Assignment 4
# app.py: Main FastAPI application file for handling routes and database interactions.
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, Field, constr
from peewee import *
import json
from datetime import date

# Load database credentials from a secret file
with open('db_secret.json') as f:
    secrets = json.load(f)

# Add a debug print statement to log database connection details
print("Connecting to database with host:", secrets['DB_HOST'], "and port:", secrets['DB_PORT'])

# Database configuration
db = MySQLDatabase(
    secrets['DB_NAME'],
    user=secrets['DB_USER'],
    password=secrets['DB_PASSWORD'],
    host=secrets['DB_HOST'],
    port=secrets['DB_PORT']
)

# Define the Survey model
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

# Initialize FastAPI app
app = FastAPI()

# Create tables
db.connect()
db.create_tables([Survey])

# Pydantic model for request validation
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
    liked_most: constr(max_length=255) = Field(None)
    interest_source: constr(max_length=255) = Field(None)
    recommend_likelihood: constr(max_length=255) = Field(None)
    additional_comments: constr(max_length=1500) = Field(None)

# Routes
# Add validation for survey input fields
@app.post("/api/surveys")
def create_survey(survey: SurveyRequest):
    try:
        validate_survey_input(survey)
        survey_data = survey.dict()
        new_survey = Survey.create(**survey_data)
        return {"id": new_survey.id, "message": "Survey created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/surveys")
def get_all_surveys():
    try:
        surveys = [survey.__data__ for survey in Survey.select()]
        return surveys
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
        existing_survey = Survey.get(Survey.id == id)
        for key, value in survey.dict().items():
            setattr(existing_survey, key, value)
        existing_survey.save()
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

# Add a version endpoint to return version information
@app.get("/api/version")
def get_version_info():
    try:
        version_html = """
        <html>
        <head><title>Python Survey API Version</title></head>
        <body>
        <h1>Survey API Version</h1>
        <p>Current Version: 2.0.0.0</p>
        <p>By Qasim Shahid for SWE 645, Extra Credit Assignment</p>
        </body>
        </html>
        """
        return HTMLResponse(content=version_html, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Validation function for survey input fields
def validate_survey_input(survey: SurveyRequest):
    VALID_LIKED_MOST = ["students", "location", "campus", "atmosphere", "dorm rooms", "sports"]
    VALID_INTEREST_SOURCE = ["friends", "television", "internet", "other"]
    VALID_RECOMMEND_LIKELIHOOD = ["very likely", "likely", "unlikely"]

    if survey.liked_most and survey.liked_most.lower().strip() not in VALID_LIKED_MOST:
        raise HTTPException(status_code=400, detail=f"Invalid value for liked_most. Options are {VALID_LIKED_MOST}. You passed {survey.liked_most}")

    if survey.interest_source and survey.interest_source.lower().strip() not in VALID_INTEREST_SOURCE:
        raise HTTPException(status_code=400, detail=f"Invalid value for interest_source. Options are {VALID_INTEREST_SOURCE}. You passed {survey.interest_source}")

    if survey.recommend_likelihood and survey.recommend_likelihood.lower().strip() not in VALID_RECOMMEND_LIKELIHOOD:
        raise HTTPException(status_code=400, detail=f"Invalid value for recommend_likelihood. Options are {VALID_RECOMMEND_LIKELIHOOD}. You passed {survey.recommend_likelihood}")