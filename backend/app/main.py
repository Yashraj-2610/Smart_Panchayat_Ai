from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import Base, engine
from .core.config import settings
from .api.endpoints import household, sarpanch, schemes, multilingual

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AI-Powered Panchayat Decision Support System for Smart Village Development"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(household.router, prefix=f"{settings.API_V1_STR}/household", tags=["Family Head Portal"])
app.include_router(sarpanch.router, prefix=f"{settings.API_V1_STR}/sarpanch", tags=["Sarpanch Portal"])
app.include_router(schemes.router, prefix=f"{settings.API_V1_STR}/schemes", tags=["Government Schemes"])
app.include_router(multilingual.router, prefix=f"{settings.API_V1_STR}/i18n", tags=["Multilingual"])

@app.get("/")
def root():
    return {
        "message": "Welcome to Smart Panchayat AI System",
        "version": settings.PROJECT_VERSION,
        "project": settings.PROJECT_NAME
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.PROJECT_VERSION}
