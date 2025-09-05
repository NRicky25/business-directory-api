from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl, EmailStr

app = FastAPI(title= "Business Directory API", version="1.0.0")

# Pydantic Models

class Business(BaseModel):
    name: str
    address: str
    website: HttpUrl
    email: EmailStr

class CreateBusiness(Business):
    name: str
    address: str
    website: HttpUrl
    email: EmailStr


# Database
BUSINESSES: List[Business] = [
    Business(
        name="Tech Solutions",
        address="123 Tech Lane, Silicon Valley, CA",
        website="https://www.techsolutions.com",
        email="support@techsolutions.com",
    ),
    Business(
        name="Green Grocers",
        address="456 Market St, Springfield, IL",
        website="https://www.greengrocers.com",
        email="hello@greengrocers.com",
    ),
]

@app.get("/", summary="API Health Check")
def root():
    return {"message": "Business Directory API is running."}

@app.get("/businesses/", response_model=List[Business], summary="Get All Businesses")
def list_businesses():
    return BUSINESSES

@app.post("/businesses/", 
          response_model=Business,
          status_code=status.HTTP_201_CREATED,
          summary="Create a New Business",
)
def create_business(business: CreateBusiness):
    if any(b.name.lower() == business.name.lower() for b in BUSINESSES):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Business with this name already exists.",
        )
    BUSINESSES.append(Business(**business.model_dump()))
    return business