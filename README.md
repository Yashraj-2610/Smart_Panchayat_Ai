# Smart Panchayat AI - AI-Powered Decision Support System for Village Development

**MIT Academy of Engineering, Alandi, Pune**  
**Department:** CSE (AI & ML)  
**Course:** Minor Project - I (2311291L)  
**Problem Statement:** Project No. 27 - AI-Powered Panchayat Decision Support System for Smart Village Development  
**Faculty Guide:** Mrs. Anita Shingade

---

## 🎯 Project Overview

The Smart Panchayat AI System is a comprehensive decision support platform that helps Gram Panchayats collect structured village data, identify development problems, prioritize needs, and make evidence-based decisions using AI technology.

### Key Features

- **Family Head Portal**: Household registration, member management, issue reporting
- **Sarpanch Dashboard**: Village analytics, population statistics, ward-wise insights
- **Multi-Agent AI System**: Specialized agents for Health, Education, Water, Infrastructure, Agriculture
- **RAG Knowledge Base**: Government scheme retrieval and recommendation matching
- **Multilingual Support**: English, Hindi, and Marathi interfaces
- **Explainable AI**: Transparent recommendations with evidence and reasoning
- **Auto-calculated Demographics**: Population derived from registered members

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  Family Head     │         │    Sarpanch      │         │
│  │  Portal (UI)     │         │   Dashboard (UI) │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend API Layer                       │
│         FastAPI REST Endpoints + Business Logic              │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Multi-Agent AI System                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Population│  │  Water   │  │  Health  │  │Education │  │
│  │  Agent   │  │  Agent   │  │  Agent   │  │  Agent   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐ │
│  │Infra-    │  │ Priority │  │    AI Orchestrator       │ │
│  │structure │  │  Agent   │  │                          │ │
│  └──────────┘  └──────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              RAG Knowledge Base (Schemes)                    │
│    Semantic retrieval of government schemes & policies       │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Database Layer (SQLite)                    │
│  Households | Members | Issues | Recommendations | Schemes  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
smart-panchayat-ai/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── base_agent.py          # Base agent class
│   │   │   ├── population_agent.py    # Demographics analysis
│   │   │   ├── water_agent.py         # Water & sanitation
│   │   │   ├── health_agent.py        # Health indicators
│   │   │   ├── education_agent.py     # Education metrics
│   │   │   ├── infrastructure_agent.py # Infrastructure analysis
│   │   │   ├── priority_agent.py      # Priority scoring
│   │   │   └── orchestrator.py        # Multi-agent coordinator
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── household.py       # Family Head Portal APIs
│   │   │   │   ├── sarpanch.py        # Sarpanch Portal APIs
│   │   │   │   ├── schemes.py         # Government schemes RAG
│   │   │   │   └── multilingual.py    # i18n endpoints
│   │   │   └── schemas.py             # Pydantic models
│   │   ├── core/
│   │   │   ├── config.py              # Settings & configuration
│   │   │   └── database.py            # SQLAlchemy setup
│   │   ├── models/                    # Database ORM models
│   │   │   ├── household.py
│   │   │   ├── family_member.py
│   │   │   ├── issue.py
│   │   │   ├── recommendation.py
│   │   │   ├── ward.py
│   │   │   ├── scheme.py
│   │   │   └── user.py
│   │   ├── services/                  # Business logic
│   │   │   ├── household_service.py
│   │   │   ├── issue_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── decision_service.py
│   │   │   ├── rag_service.py
│   │   │   └── multilingual_service.py
│   │   └── main.py                    # FastAPI app
│   ├── init_db.py                     # Database initialization
│   ├── seed_demo_data.py              # Demo data generator
│   └── README.md
├── frontend/
│   ├── family_portal.py               # Streamlit Family Portal
│   └── sarpanch_dashboard.py          # Streamlit Sarpanch Dashboard
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9+
- pip package manager

### Installation Steps

1. **Clone/Download the project**
```bash
cd C:\Users\yashr\Downloads\AI\smart-panchayat-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize the database**
```bash
cd backend
python init_db.py
```

4. **Seed demo data (Optional but recommended)**
```bash
python seed_demo_data.py
```

5. **Start the Backend API Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **In a new terminal, start Family Head Portal**
```bash
cd frontend
streamlit run family_portal.py --server.port 8501
```

7. **In another terminal, start Sarpanch Dashboard**
```bash
cd frontend
streamlit run sarpanch_dashboard.py --server.port 8502
```

### Access the Applications

- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Family Head Portal**: http://localhost:8501
- **Sarpanch Dashboard**: http://localhost:8502

---

## 🐳 Docker Deployment

### Run with Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Deploy to Cloud Platforms

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides on:
- **Railway** (Free tier, 1-click deploy)
- **Render** (Free tier, automatic deploys)
- **Fly.io** (Free tier, 3 VMs)
- **VPS / Custom Server** (Docker setup)


---

## 🎓 Academic Deliverables

### Course Outcomes Addressed

- **CO1**: Designed solution for real-world Gram Panchayat decision-making problems
- **CO2**: Planned project with timeline, tech stack selection, and resource estimation
- **CO3**: Applied professional ethics in data privacy, security, and responsible AI
- **CO4**: Integrated multiple design ideas (multi-agent AI, RAG, multilingual, analytics)
- **CO5**: Demonstrated teamwork and coordinated implementation

### Project Review - I Evaluation (10 Marks)

✅ **Problem Statement & Objectives** (2/2): Clear real-world problem with measurable objectives  
✅ **Literature Review** (2/2): Reviewed existing Panchayat systems, AI decision support, multi-agent architectures  
✅ **System Architecture** (2/2): Complete architecture diagram with all modules and data flow  
✅ **Dataset/Tool Selection** (2/2): Justified use of FastAPI, Streamlit, SQLAlchemy, multi-agent framework  
✅ **Implementation Plan** (2/2): Phased roadmap with realistic timeline and coordinated delivery

---

## 🤖 Multi-Agent AI System

### Specialized Agents

1. **Population & Demography Agent**: Analyzes household registration, age distribution, ward imbalances
2. **Water Agent**: Monitors water supply issues, sanitation concerns, affected households
3. **Health Agent**: Tracks health issues, disease risks, healthcare access
4. **Education Agent**: Monitors school enrollment, dropout rates, literacy
5. **Infrastructure Agent**: Analyzes roads, electricity, public facilities
6. **Priority Agent**: Scores and ranks issues based on severity, domain weights, affected count

### Orchestrator Workflow

```python
orchestrator = MultiAgentOrchestrator()
analysis = orchestrator.run_analysis(db)

# Returns:
# - agent_results: Findings from each specialized agent
# - priority_analysis: Ranked list of issues by priority score
# - recommendations: Actionable next steps
# - summary: Human-readable executive summary
```

---

## 📚 RAG Knowledge Base

Government schemes database with semantic retrieval:

- **Jal Jeevan Mission** (Water)
- **Swachh Bharat Mission** (Sanitation)
- **Ayushman Bharat** (Health)
- **PM-KISAN** (Agriculture)
- **PMAY-Gramin** (Housing)
- **PMGSY** (Roads)
- **Samagra Shiksha** (Education)
- **State-level schemes** (Maharashtra)

Search Example:
```python
schemes = RAGService.retrieve_relevant_schemes(
    query="water pipeline leak affecting 25 families",
    domain="Water",
    top_k=3
)
```

---

## 🌐 Multilingual Support

Supported Languages:
- **English (en)**
- **Hindi (hi) - हिंदी**
- **Marathi (mr) - मराठी**

UI labels, navigation, and system messages are translated. AI-generated recommendations can be displayed in the user's preferred language.

---

## 📊 Key Metrics & Analytics

### Population Analytics
- Total households and population (auto-calculated)
- Gender distribution
- Age groups (children, adults, senior citizens)
- Literacy rate, employment rate
- BPL/APL/Antodaya classification

### Ward Analytics
- Ward-wise population and household count
- Issue density per ward
- High-priority issues by location

### Issue Analytics
- Issues by category (Water, Health, Education, etc.)
- Issues by priority (Low, Medium, High, Critical)
- Resolution status tracking

---

## 🔐 Security & Privacy

- **Role-based access control**: Family Head, Sarpanch, Admin roles
- **Data validation**: Input sanitization at API level
- **Audit logging**: All critical actions logged with timestamp
- **Synthetic data**: Demo uses generated data, not real citizen information
- **GDPR/Privacy considerations**: Data retention policies, consent mechanisms

---

## 🎯 Future Enhancements

1. **GIS Integration**: Village maps with geospatial ward boundaries
2. **Mobile App**: Offline-first mobile application for low-connectivity areas
3. **Voice Interface**: Speech input/output for accessibility
4. **Integration with DigiLocker**: Aadhar-based authentication
5. **Predictive Analytics**: Forecast water demand, agricultural risks, infrastructure needs
6. **Blockchain**: Immutable audit trail for fund allocation transparency

---

## 📖 References

1. Ministry of Panchayati Raj, Government of India - e-Governance initiatives
2. National Rural Development & Panchayat Raj Institute (NIRDPR)
3. Digital India Programme - Smart Villages
4. Maharashtra State e-Governance guidelines
5. Multi-Agent Systems for Decision Support (Academic literature)

---

## 👥 Project Team

**Group 15**  
MIT Academy of Engineering, Alandi, Pune  
Department of Computer Science & Engineering (AI & ML)  
Academic Year: 2026

**Faculty Guide:** Mrs. Anita Shingade

---

## 📄 License

This is an academic project developed for educational purposes as part of Minor Project - I course.

---

## 🙏 Acknowledgments

Special thanks to:
- Mrs. Anita Shingade (Faculty Guide)
- MIT Academy of Engineering, Alandi
- Department of CSE (AI & ML)
- Review Panel Members for valuable feedback
