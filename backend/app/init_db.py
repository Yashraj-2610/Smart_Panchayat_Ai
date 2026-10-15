"""
Database Initialization Module
Seeds wards, government schemes, and default users into the database
Includes health check and stats reporting
"""
from .core.database import SessionLocal, engine, Base, get_database_health, get_database_stats
from .models.ward import Ward
from .models.user import User, UserRole
from .core.security import hash_password
from .services.rag_service import RAGService
import logging

logger = logging.getLogger(__name__)


def init_db():
    """Initialize database with default data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Health check
        health = get_database_health()
        if health["connected"]:
            logger.info(f"✓ Database connected ({health.get('tables', [])})")
        else:
            logger.error(f"Database health check failed: {health.get('error')}")
            raise Exception(f"Cannot connect to database: {health.get('error')}")

        # Seed Wards
        existing_wards = db.query(Ward).count()
        if existing_wards == 0:
            logger.info("Seeding wards...")
            wards_data = [
                {"ward_number": 1, "ward_name": "Ward 1 - Central"},
                {"ward_number": 2, "ward_name": "Ward 2 - North"},
                {"ward_number": 3, "ward_name": "Ward 3 - South"},
                {"ward_number": 4, "ward_name": "Ward 4 - East"},
                {"ward_number": 5, "ward_name": "Ward 5 - West"},
                {"ward_number": 6, "ward_name": "Ward 6 - Outskirts"}
            ]

            for ward_data in wards_data:
                ward = Ward(**ward_data)
                db.add(ward)

            db.commit()
            logger.info(f"✓ Seeded {len(wards_data)} wards")
        else:
            logger.info(f"Wards already exist ({existing_wards} wards)")

        # Seed Government Schemes
        logger.info("Seeding government schemes...")
        RAGService.seed_schemes(db)
        logger.info("✓ Government schemes seeded")

        # Log statistics
        stats = get_database_stats()
        logger.info(f"Database stats: {stats}")

        print("\n" + "=" * 50)
        print("Database initialization complete!")
        print("=" * 50)
        print(f"Total Wards: {db.query(Ward).count()}")
        print(f"Total Schemes: {len(RAGService.GOVERNMENT_SCHEMES_DATA)}")

    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    init_db()