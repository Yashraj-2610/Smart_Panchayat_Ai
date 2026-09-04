"""
Database Initialization Script
Seeds wards and government schemes into the database
Run this after starting the server for the first time
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models.ward import Ward
from app.services.rag_service import RAGService

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Seed Wards
        existing_wards = db.query(Ward).count()
        if existing_wards == 0:
            print("Seeding wards...")
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
            print(f"✓ Seeded {len(wards_data)} wards")
        else:
            print(f"Wards already exist ({existing_wards} wards)")

        # Seed Government Schemes
        print("Seeding government schemes...")
        RAGService.seed_schemes(db)
        print("✓ Government schemes seeded")

        print("\nDatabase initialization complete!")
        print(f"Total Wards: {db.query(Ward).count()}")
        print(f"Total Schemes: {len(RAGService.GOVERNMENT_SCHEMES_DATA)}")

    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing Smart Panchayat Database...")
    init_db()
