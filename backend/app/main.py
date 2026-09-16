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

@app.post("/seed-database")
def seed_database():
    """Safe endpoint to initialize wards and schemes in the database"""
    from .init_db import init_db
    try:
        init_db()
        return {"status": "success", "message": "Database seeded successfully with wards and schemes"}
    except Exception as e:
        return {"status": "error", "message": f"Database seeding failed: {str(e)}"}

@app.post("/seed-demo-data")
def seed_demo_data():
    """Safe endpoint to populate demo households, families, and issues"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    try:
        from seed_demo_data import generate_demo_data
        generate_demo_data()
        return {
            "status": "success",
            "message": "Demo data seeded: 30 households, 100+ family members, 10+ village issues with AI recommendations"
        }
    except Exception as e:
        return {"status": "error", "message": f"Demo data seeding failed: {str(e)}"}
