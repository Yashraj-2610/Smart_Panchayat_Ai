from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import Base, engine, SessionLocal
from .core.config import settings
from .core.middleware import RequestLoggingMiddleware, add_error_handlers
from .core.security import hash_password
from .models.user import User, UserRole
from .api.endpoints import household, sarpanch, schemes, multilingual, auth

# Create database tables
Base.metadata.create_all(bind=engine)

# Ensure default Sarpanch & Admin accounts exist
def init_default_users():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            sarpanch_user = User(
                username="sarpanch",
                email="sarpanch@alandi-panchayat.gov.in",
                hashed_password=hash_password("sarpanch123"),
                full_name="Dattatray Patil (Sarpanch)",
                role=UserRole.SARPANCH,
                phone_number="+919876543210",
                preferred_language="mr",
                is_active=True
            )
            admin_user = User(
                username="admin",
                email="admin@alandi-panchayat.gov.in",
                hashed_password=hash_password("admin123"),
                full_name="Panchayat Secretary / Admin",
                role=UserRole.PANCHAYAT_ADMIN,
                phone_number="+919876543211",
                preferred_language="en",
                is_active=True
            )
            family_demo = User(
                username="resident",
                email="resident@alandi.in",
                hashed_password=hash_password("resident123"),
                full_name="Ramesh Patil (Family Head)",
                role=UserRole.FAMILY_HEAD,
                phone_number="+919876543212",
                preferred_language="mr",
                is_active=True
            )
            db.add_all([sarpanch_user, admin_user, family_demo])
            db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()

init_default_users()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AI-Powered Panchayat Decision Support System with E2E Encryption & RBAC",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Add global error handlers
add_error_handlers(app)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication & Privacy"])
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
