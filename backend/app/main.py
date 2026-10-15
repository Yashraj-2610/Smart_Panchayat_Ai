from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import event
from .core.database import Base, engine, SessionLocal, get_database_health, get_database_stats
from .core.config import settings
from .core.middleware import RateLimitMiddleware, RequestLoggingMiddleware, add_error_handlers, add_request_id_middleware
from .core.security import hash_password, decode_access_token, create_access_token
from .models.user import User, UserRole
from .api.endpoints import household, sarpanch, schemes, multilingual, auth

# Create database tables
Base.metadata.create_all(bind=engine)

# Enhanced logging with database health at startup
logger = settings.LOG_LEVEL
logger.info(f"Starting Smart Panchayat AI v{settings.PROJECT_VERSION}")
logger.info(f"Environment: {settings.ENVIRONMENT}")
logger.info(f"Database: {settings.DATABASE_URL}")

# Run database health check
try:
    health = get_database_health()
    if health["connected"]:
        logger.info(f"Database healthy ({len(health.get('tables', []))} tables)")
    else:
        logger.warning(f"Database connection issue: {health.get('error')}")
except Exception as e:
    logger.error(f"Database health check failed at startup: {e}")

# Ensure default Sarpanch & Admin accounts exist
def init_default_users():
    db = SessionLocal()
    try:
        # Check if database tables exist
        user_count = db.query(User).count()
        logger.info(f"Current user count: {user_count}")

        if user_count == 0:
            # Initialize default users only if tables exist
            # Use hashed passwords from existing env setup or generate new ones
            import bcrypt
            default_sarpanch_pwd = os.getenv("DEFAULT_SARPANCH_PASSWORD", "sarpanch123")
            default_admin_pwd = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")
            default_resident_pwd = os.getenv("DEFAULT_RESIDENT_PASSWORD", "resident123")

            sarpanch_user = User(
                username="sarpanch",
                email="sarpanch@alandi-panchayat.gov.in",
                hashed_password=hash_password(default_sarpanch_pwd),
                full_name="Dattatray Patil (Sarpanch)",
                role=UserRole.SARPANCH,
                phone_number="+919876543210",
                preferred_language="mr",
                is_active=True
            )
            admin_user = User(
                username="admin",
                email="admin@alandi-panchayat.gov.in",
                hashed_password=hash_password(default_admin_pwd),
                full_name="Panchayat Secretary / Admin",
                role=UserRole.PANCHAYAT_ADMIN,
                phone_number="+919876543211",
                preferred_language="en",
                is_active=True
            )
            family_demo = User(
                username="resident",
                email="resident@alandi.in",
                hashed_password=hash_password(default_resident_pwd),
                full_name="Ramesh Patil (Family Head)",
                role=UserRole.FAMILY_HEAD,
                phone_number="+919876543212",
                preferred_language="mr",
                is_active=True
            )
            db.add_all([sarpanch_user, admin_user, family_demo])
            db.commit()
            logger.info("✓ Default users initialized")
        else:
            logger.info(f"User tables already populated ({user_count} users)")
    except Exception as e:
        logger.error(f"Error initializing default users: {e}")
        db.rollback()
    finally:
        db.close()

# Try to import os at module level
import os

init_default_users()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AI-Powered Panchayat Decision Support System with E2E Encryption & RBAC",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add request ID middleware
add_request_id_middleware(app)

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
)

# Add logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Add global error handlers
add_error_handlers(app)

# Configure CORS middleware
# In development, allow all origins configured in settings
allowed_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]

# Remove wildcard - only allow specified origins in production
# For development with frontend apps, we allow them specifically
origins = [
    "http://localhost:8501",
    "http://localhost:8502",
    "http://localhost:8000",
]

if settings.ENVIRONMENT == "development":
    # Allow all origins in dev mode for easier testing
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


# Health check endpoint
@app.get("/health")
def health_check():
    """Enhanced health check with database status"""
    db_status = "healthy"
    try:
        from .core.database import get_database_health
        db_health = get_database_health()
        if db_health["connected"]:
            # Check table count
            inspector = __import__("sqlalchemy").inspect(engine)
            table_count = len(db_health.get("tables", []))
            db_status = f"healthy ({table_count} tables)"
        else:
            db_status = "unhealthy"
    except Exception:
        db_status = "unreachable"

    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
    }


# Root endpoint
@app.get("/")
def root():
    """Root endpoint with system information"""
    return {
        "message": "Welcome to Smart Panchayat AI System",
        "version": settings.PROJECT_VERSION,
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "database_url_configured": bool(settings.DATABASE_URL),
    }


# Endpoint to check database health (for monitoring)
@app.get("/health/database")
def database_health():
    """Database health endpoint"""
    return get_database_health()

# Endpoint for database statistics
@app.get("/admin/database/stats")
def database_stats_endpoint():
    """Database statistics for admin dashboard"""
    return get_database_stats()

# Seed endpoint with enhanced error handling
@app.post("/seed-database")
def seed_database():
    """Safe endpoint to initialize wards and schemes in the database"""
    from .init_db import init_db
    try:
        init_db()
        return {"status": "success", "message": "Database seeded successfully with wards and schemes"}
    except Exception as e:
        return {"status": "error", "message": f"Database seeding failed: {str(e)}"}

# Demo data endpoint with enhanced error handling
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
