"""
Synthetic Demo Data Generator for Smart Panchayat AI System
Populates realistic village data for demonstration:
- 6 Wards
- 25+ Households across all wards
- 100+ Family members with diverse demographics
- 15+ Realistic village issues (water, roads, health, education)
- AI Recommendations with RAG matched schemes
"""
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.ward import Ward
from app.models.household import Household, HouseholdType
from app.models.family_member import FamilyMember, Gender, EducationLevel
from app.models.issue import Issue, IssueCategory, IssueStatus, IssuePriority
from app.services.rag_service import RAGService
from app.services.decision_service import DecisionSupportService

FIRST_NAMES_MALE = ["Ramesh", "Suresh", "Ganesh", "Santosh", "Vijay", "Anil", "Prakash", "Sachin", "Rahul", "Dattatray", "Tukaram", "Pandurang"]
FIRST_NAMES_FEMALE = ["Sunita", "Savita", "Anita", "Shobha", "Pooja", "Laxmi", "Asha", "Mangal", "Suman", "Rani", "Rekha", "Usha"]
LAST_NAMES = ["Patil", "Deshmukh", "Shinde", "Jadhav", "Pawar", "Kadam", "Chavan", "Gaekwad", "Bhosale", "More", "Kulkarni", "Joshi"]

OCCUPATIONS = ["Farmer", "Agricultural Labourer", "Small Business Owner", "Teacher", "Driver", "Mason", "Shopkeeper", "Unemployed"]

SAMPLE_ISSUES = [
    ("Water", "Drinking water pipeline leak in main chowk", "Main pipeline broken for 3 days leading to severe water shortage for 25 families.", 25, IssuePriority.CRITICAL),
    ("Water", "Low water pressure in Ward 4", "Borewell motor failing, water reaches only 1 hour per day.", 15, IssuePriority.HIGH),
    ("Road & Infrastructure", "Potholes on Main Mandir Road", "Road completely damaged after monsoon, difficult for ambulances and two-wheelers.", 40, IssuePriority.HIGH),
    ("Sanitation", "Open drainage overflow near primary school", "Stagnant water breeding mosquitoes, risk of dengue and malaria for school children.", 50, IssuePriority.CRITICAL),
    ("Health", "Shortage of primary medicines at sub-center", "Fever, cold, and diabetes medicines out of stock for 2 weeks.", 30, IssuePriority.HIGH),
    ("Education", "Shortage of science teachers and lab equipment in ZP school", "High school students lack practical science classes.", 60, IssuePriority.MEDIUM),
    ("Electricity", "Frequent power cuts during irrigation hours", "Farmers facing 8-hour load shedding during crop watering cycles.", 35, IssuePriority.HIGH),
    ("Agriculture", "Fertilizer distribution delay at cooperative society", "Urea and DAP stock delayed during peak sowing season.", 45, IssuePriority.MEDIUM),
    ("Road & Infrastructure", "Street lights not working in Ward 6 outskirts", "Darkness creating safety issues for women and night commuters.", 20, IssuePriority.MEDIUM),
    ("Water", "Contaminated drinking water from community well", "Muddy water coming from well, 4 children reported diarrhea.", 18, IssuePriority.CRITICAL)
]

def generate_demo_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Clearing old demo data...")
        db.query(FamilyMember).delete()
        db.query(Issue).delete()
        db.query(Household).delete()
        db.query(Ward).delete()
        db.commit()

        print("1. Creating Wards...")
        wards = []
        for i in range(1, 7):
            w = Ward(ward_number=i, ward_name=f"Ward {i} - Section {chr(64+i)}", population=0, total_households=0)
            db.add(w)
            wards.append(w)
        db.commit()

        # Reload wards with IDs
        wards = db.query(Ward).all()

        print("2. Seeding Government Schemes...")
        RAGService.seed_schemes(db)

        print("3. Generating Households & Family Members...")
        households = []
        member_id_counter = 1000

        for i in range(1, 30):
            ward = random.choice(wards)
            is_male_head = random.random() > 0.3
            head_first = random.choice(FIRST_NAMES_MALE if is_male_head else FIRST_NAMES_FEMALE)
            last_name = random.choice(LAST_NAMES)
            head_name = f"{head_first} {last_name}"
            head_age = random.randint(30, 68)
            head_gender = "Male" if is_male_head else "Female"
            head_occ = random.choice(OCCUPATIONS)
            hh_type = random.choices([HouseholdType.APL, HouseholdType.BPL, HouseholdType.ANTODAYA], weights=[0.5, 0.4, 0.1])[0]

            hh = Household(
                household_id=f"HH-W{ward.ward_number}-{1000+i}",
                head_name=head_name,
                head_age=head_age,
                head_gender=head_gender,
                head_occupation=head_occ,
                contact_number=f"+91{random.randint(7000000000, 9999999999)}",
                address=f"House No. {random.randint(1, 200)}, Near {random.choice(['Temple', 'School', 'Chowk', 'Gram Panchayat', 'Water Tank'])}, Ward {ward.ward_number}",
                ward_id=ward.id,
                household_type=hh_type,
                annual_income=random.randint(30000, 150000),
                ration_card_number=f"RC-MH-{random.randint(100000, 999999)}",
                total_members=0
            )
            db.add(hh)
            db.flush()

            # Add Head as member
            head_member = FamilyMember(
                household_id=hh.id,
                full_name=head_name,
                age=head_age,
                gender=Gender.MALE if head_gender == "Male" else Gender.FEMALE,
                relation_to_head="Self (Head)",
                aadhar_number=str(random.randint(100000000000, 999999999999)),
                education_level=random.choice(list(EducationLevel)),
                occupation=head_occ,
                is_employed=head_occ != "Unemployed",
                is_student=False,
                has_health_issues=random.random() < 0.15
            )
            db.add(head_member)
            hh.total_members += 1
            ward.population += 1

            # Add 2 to 5 additional family members
            num_other_members = random.randint(2, 5)

            # Add spouse
            spouse_first = random.choice(FIRST_NAMES_FEMALE if is_male_head else FIRST_NAMES_MALE)
            spouse_gender = Gender.FEMALE if is_male_head else Gender.MALE
            spouse_member = FamilyMember(
                household_id=hh.id,
                full_name=f"{spouse_first} {last_name}",
                age=head_age - random.randint(1, 5),
                gender=spouse_gender,
                relation_to_head="Spouse",
                aadhar_number=str(random.randint(100000000000, 999999999999)),
                education_level=random.choice(list(EducationLevel)),
                occupation="Homemaker" if spouse_gender == Gender.FEMALE else "Farmer",
                is_employed=random.random() > 0.5,
                is_student=False,
                has_health_issues=random.random() < 0.15
            )
            db.add(spouse_member)
            hh.total_members += 1
            ward.population += 1

            # Add children
            for c in range(num_other_members - 1):
                child_gender = random.choice([Gender.MALE, Gender.FEMALE])
                child_first = random.choice(FIRST_NAMES_MALE if child_gender == Gender.MALE else FIRST_NAMES_FEMALE)
                child_age = random.randint(3, 22)
                is_stud = child_age >= 5 and child_age <= 21

                child = FamilyMember(
                    household_id=hh.id,
                    full_name=f"{child_first} {last_name}",
                    age=child_age,
                    gender=child_gender,
                    relation_to_head="Son" if child_gender == Gender.MALE else "Daughter",
                    aadhar_number=str(random.randint(100000000000, 999999999999)),
                    education_level=EducationLevel.PRIMARY if child_age < 12 else (EducationLevel.SECONDARY if child_age < 16 else EducationLevel.HIGHER_SECONDARY),
                    occupation="Student" if is_stud else ("None" if child_age < 5 else "Labourer"),
                    is_employed=False,
                    is_student=is_stud,
                    has_health_issues=random.random() < 0.05
                )
                db.add(child)
                hh.total_members += 1
                ward.population += 1

            ward.total_households += 1
            households.append(hh)

        db.commit()
        print(f"✓ Generated {len(households)} Households and {db.query(FamilyMember).count()} Members across 6 Wards")

        print("4. Generating Sample Village Issues...")
        for cat, title, desc, affected, prio in SAMPLE_ISSUES:
            hh = random.choice(households)
            issue = Issue(
                issue_id=f"{cat[:3].upper()}-{random.randint(1000, 9999)}",
                household_id=hh.id,
                category=getattr(IssueCategory, cat.upper().replace(" & ", "_").replace(" ", "_"), IssueCategory.OTHER),
                title=title,
                description=desc,
                status=IssueStatus.SUBMITTED,
                priority=prio,
                affected_count=affected,
                language="en"
            )
            db.add(issue)
        db.commit()
        print(f"✓ Created {len(SAMPLE_ISSUES)} Village Issues")

        print("5. Generating AI Decision Recommendations...")
        recs = DecisionSupportService.generate_recommendations_for_all_issues(db)
        print(f"✓ Generated {len(recs)} AI Recommendations with explainable evidence and RAG schemes")

        print("\n=======================================================")
        print("🎉 SYNTHETIC DEMO DATA GENERATION COMPLETED SUCCESSFULLY!")
        print("=======================================================")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_demo_data()
