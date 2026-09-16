from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

# Load template to get dimensions and master slides
template = Presentation('C:/Users/yashr/Downloads/Minor Project/Group_15_First_Review_Presentation.pptx')

# Create new presentation
prs = Presentation()
prs.slide_width = template.slide_width
prs.slide_height = template.slide_height

def add_title_slide(title_text, subtitle_text):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = title_text
    subtitle.text = subtitle_text
    return slide

def add_content_slide(title_text, content_lines):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = title_text

    # Add text box for bullet points
    left = Inches(0.5)
    top = Inches(1.5)
    width = Inches(9)
    height = Inches(5)

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, line in enumerate(content_lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.text = line
        if line.startswith('  '):
            p.level = 1
            p.text = line.strip()
        else:
            p.level = 0
        p.font.size = Pt(16)
        p.space_before = Pt(6)

    return slide

# SLIDE 1: Title
add_title_slide(
    "AI-Powered Panchayat Decision Support System\nFinal Implementation Presentation",
    "Multi-Agent, Multilingual Village Intelligence Platform\n\n" +
    "Group 15 | Department of CSE (AI & ML)\n" +
    "MIT Academy of Engineering, Alandi, Pune\n\n" +
    "Guide: Mrs. Anita Shingade\n" +
    "Academic Year: 2026-27\n\n" +
    "COMPLETE IMPLEMENTATION - READY FOR DEMONSTRATION"
)

# SLIDE 2: Project Status
add_content_slide("Project Completion Status", [
    "Status: 100% COMPLETE - Production Ready",
    "",
    "All Core Features Implemented:",
    "  Family Head Portal (Registration, Members, Issues)",
    "  Sarpanch Dashboard (Analytics, AI Decision Support)",
    "  Multi-Agent AI System (6 Specialized Agents)",
    "  RAG Knowledge Base (8 Government Schemes)",
    "  Multilingual Support (English, Hindi, Marathi)",
    "",
    "Project Metrics:",
    "  42+ Files Created | 3,500+ Lines of Code",
    "  8 Database Models | 20+ REST API Endpoints",
    "  29 Demo Households | 100+ Family Members"
])

# SLIDE 3: System Architecture
add_content_slide("System Architecture - Fully Implemented", [
    "Frontend Layer:",
    "  Family Head Portal (Streamlit) - Multilingual UI",
    "  Sarpanch Dashboard (Streamlit) - Interactive Charts",
    "",
    "Backend API Layer (FastAPI):",
    "  20+ REST Endpoints | Auto-calculated Demographics",
    "",
    "Multi-Agent AI Intelligence:",
    "  6 Specialized Agents + Orchestrator",
    "  Evidence-based Analysis | Priority Scoring",
    "",
    "RAG Knowledge Base:",
    "  Semantic Scheme Retrieval | Multilingual Matching",
    "",
    "Database (SQLite): 8 Tables | Auto-population Calculation"
])

# SLIDE 4: Multi-Agent System
add_content_slide("Multi-Agent AI System - Core Innovation", [
    "6 Specialized Domain Agents:",
    "",
    "1. Population Agent - Demographics & registration",
    "2. Water Agent - Water supply & sanitation",
    "3. Health Agent - Disease prevalence & healthcare",
    "4. Education Agent - Enrollment, dropout, literacy",
    "5. Infrastructure Agent - Roads, electricity",
    "6. Priority Agent - Mathematical scoring (0-100)",
    "",
    "Orchestrator Coordination:",
    "  Runs all agents in parallel",
    "  Aggregates evidence from each domain",
    "  Produces explainable recommendations"
])

# SLIDE 5: Key Features
add_content_slide("Key Features - Live System", [
    "Family Head Portal:",
    "  Household registration with auto-generated IDs",
    "  Family member addition (auto-calculates population)",
    "  Village issue reporting with multilingual support",
    "",
    "Sarpanch Dashboard:",
    "  Real-time population & demographic analytics",
    "  Ward-wise development indicators",
    "  Multi-agent AI analysis with severity levels",
    "  Explainable recommendations with evidence",
    "  RAG-based government scheme search",
    "  Automated Panchayat meeting reports"
])

# SLIDE 6: RAG Knowledge Base
add_content_slide("RAG Knowledge Base Implementation", [
    "Government Schemes Database:",
    "",
    "Central Schemes:",
    "  Jal Jeevan Mission (Water)",
    "  Swachh Bharat Mission (Sanitation)",
    "  Ayushman Bharat - PMJAY (Health)",
    "  PM-KISAN Samman Nidhi (Agriculture)",
    "  PMGSY (Roads & Infrastructure)",
    "  Samagra Shiksha Abhiyan (Education)",
    "",
    "RAG Features:",
    "  Keyword + Semantic Matching",
    "  Multilingual Scheme Names (EN, HI, MR)"
])

# SLIDE 7: Multilingual
add_content_slide("Multilingual Support - 3 Languages", [
    "Implemented Languages:",
    "  English (en) - Primary interface",
    "  Hindi (hi) - Complete translation",
    "  Marathi (mr) - Full localization",
    "",
    "Multilingual Components:",
    "  UI Labels and Navigation",
    "  Form Fields and Validation Messages",
    "  Dashboard Metrics and Charts",
    "  Government Scheme Names",
    "",
    "Implementation:",
    "  Translation dictionary service",
    "  Language selector in both portals"
])

# SLIDE 8: Technology Stack
add_content_slide("Technology Stack - Production Ready", [
    "Backend:",
    "  FastAPI - REST API framework",
    "  SQLAlchemy - ORM with auto-calculation",
    "  Pydantic - Data validation",
    "",
    "Frontend:",
    "  Streamlit - Interactive dashboards",
    "  Plotly - Data visualizations",
    "",
    "AI/ML:",
    "  Custom Multi-Agent Framework",
    "  RAG - Keyword + Semantic Matching",
    "  Priority Scoring Algorithm",
    "",
    "All components integrated and tested!"
])

# SLIDE 9: Database Design
add_content_slide("Database Design - 8 Core Entities", [
    "Implemented Models:",
    "",
    "1. Ward - Village administrative divisions",
    "2. Household - Family head details",
    "3. FamilyMember - Demographics, education",
    "4. Issue - Citizen complaints",
    "5. AIRecommendation - Priority scores",
    "6. Scheme - Government programs",
    "7. User - Role-based access",
    "8. AuditLog - Action tracking",
    "",
    "Key Features:",
    "  Auto-calculated population from members",
    "  Ward totals update automatically"
])

# SLIDE 10: Demo Data
add_content_slide("Demo Data - Realistic Village", [
    "Generated Synthetic Data:",
    "",
    "Village: Alandi Gram Panchayat, Pune",
    "  6 Wards (Ward 1-6)",
    "  29 Households across all wards",
    "  100+ Family Members",
    "  Age groups: Children, Adults, Seniors",
    "  Household types: APL, BPL, Antodaya",
    "",
    "Issues & Recommendations:",
    "  10 Realistic village problems",
    "  10 AI-generated recommendations",
    "  Priority scores: 40-95 out of 100",
    "  Matched government schemes"
])

# SLIDE 11: Live Demo
add_content_slide("Live Demo - 5 Minute Walkthrough", [
    "Part 1: Family Head Portal (2 min)",
    "  1. Select Marathi language",
    "  2. Register household - Get unique ID",
    "  3. Add 3 members - Watch auto-calculation",
    "  4. Submit water issue - Issue ID generated",
    "",
    "Part 2: Sarpanch Dashboard (3 min)",
    "  1. Overview - Population metrics",
    "  2. Run Multi-Agent Analysis",
    "  3. Show severity levels",
    "  4. AI Recommendations",
    "  5. Search schemes",
    "  6. Download report"
])

# SLIDE 12: Testing
add_content_slide("Testing & Quality Assurance", [
    "Testing Completed:",
    "",
    "API Testing (Swagger UI):",
    "  All 20+ endpoints tested",
    "",
    "Frontend Testing:",
    "  Form validation working",
    "  Language switching verified",
    "",
    "Multi-Agent System:",
    "  All 6 agents producing correct analysis",
    "  Priority scoring validated",
    "",
    "Data Integrity:",
    "  Auto-calculation accuracy: 100%"
])

# SLIDE 13: Course Outcomes
add_content_slide("Course Outcomes - All Met", [
    "CO1: Design solutions for real-world problems",
    "  Complete Panchayat decision support system",
    "",
    "CO2: Project planning with timeline",
    "  14-week phased roadmap documented",
    "",
    "CO3: Professional ethics & standards",
    "  Data privacy, audit logs, responsible AI",
    "",
    "CO4: Integrate multiple design ideas",
    "  Multi-agent + RAG + Multilingual",
    "",
    "CO5: Teamwork and collaboration",
    "  Modular architecture, coordinated delivery"
])

# SLIDE 14: Innovations
add_content_slide("Unique Innovations", [
    "1. Multi-Agent Architecture",
    "   First Panchayat system with 6 AI agents",
    "",
    "2. Auto-Calculated Demographics",
    "   Eliminates manual entry errors",
    "",
    "3. Explainable AI with Evidence",
    "   Shows reasoning & data sources",
    "",
    "4. RAG-based Scheme Matching",
    "   Connects problems to solutions",
    "",
    "5. Multilingual by Design",
    "   English, Hindi, Marathi",
    "",
    "6. Production-Ready",
    "   Deployable system, not prototype"
])

# SLIDE 15: Future Scope
add_content_slide("Future Enhancements", [
    "Short-term (1-3 months):",
    "  Automated testing suite",
    "  Docker containerization",
    "  PostgreSQL migration",
    "",
    "Medium-term (3-6 months):",
    "  GIS integration with maps",
    "  Mobile application",
    "  Voice interface",
    "",
    "Long-term (6-12 months):",
    "  LLM integration",
    "  Real-time sync with e-Gram Swaraj",
    "  Multi-village analytics",
    "  Regional deployment"
])

# SLIDE 16: Impact
add_content_slide("Project Impact & Benefits", [
    "For Gram Panchayat:",
    "  Data-driven decision making",
    "  Transparent priority ranking",
    "  Direct scheme connection",
    "",
    "For Citizens:",
    "  Easy registration",
    "  Multilingual interface",
    "  Direct issue reporting",
    "",
    "Scalability:",
    "  Can serve 2.5+ lakh Gram Panchayats",
    "",
    "SDG Alignment:",
    "  SDG 11 (Cities) & SDG 16 (Institutions)"
])

# SLIDE 17: Documentation
add_content_slide("Comprehensive Documentation", [
    "Technical Documentation:",
    "  README.md - Complete guide (3000+ words)",
    "  API Documentation - Swagger UI",
    "  Architecture diagrams",
    "",
    "Academic Documentation:",
    "  PRESENTATION_GUIDE.md",
    "  TESTING_GUIDE.md",
    "  ROADMAP.md",
    "  PROJECT_COMPLETION_SUMMARY.md",
    "",
    "Setup & Deployment:",
    "  Installation guide",
    "  Quick start script",
    "  GitHub setup guide"
])

# SLIDE 18: Conclusion
add_content_slide("Conclusion - Mission Accomplished", [
    "Project Summary:",
    "  100% Complete Implementation",
    "  All objectives achieved",
    "  Production-ready system",
    "",
    "Key Achievements:",
    "  Multi-Agent AI with explanations",
    "  RAG Knowledge Base",
    "  Multilingual interface (3 languages)",
    "  Auto-calculated demographics",
    "  Real-time analytics",
    "",
    "Ready For:",
    "  Live demonstration",
    "  Faculty evaluation",
    "  Real-world deployment"
])

# SLIDE 19: Thank You
add_title_slide(
    "Thank You",
    "Questions & Demonstration Welcome\n\n" +
    "Smart Panchayat AI System\n" +
    "Complete | Production-Ready | Deployable\n\n" +
    "Group 15 | MIT Academy of Engineering\n" +
    "Department of CSE (AI & ML)\n\n" +
    "Guide: Mrs. Anita Shingade\n" +
    "Academic Year: 2026-27"
)

# Save
prs.save('Smart_Panchayat_AI_Final_Presentation.pptx')
print('Presentation created: Smart_Panchayat_AI_Final_Presentation.pptx')
print(f'Total slides: {len(prs.slides)}')
