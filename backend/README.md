# Smart Panchayat AI - Backend

Backend API for Smart Panchayat Decision Support System

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database:
```bash
cd backend
python init_db.py
```

3. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Family Head Portal
- `POST /api/v1/household/register` - Register household
- `POST /api/v1/household/{id}/members` - Add family member
- `POST /api/v1/household/{id}/issues` - Report issue

### Sarpanch Portal
- `GET /api/v1/sarpanch/dashboard/overview` - Dashboard data
- `GET /api/v1/sarpanch/analytics/population` - Population analytics
- `POST /api/v1/sarpanch/ai/analyze` - Run multi-agent analysis
- `POST /api/v1/sarpanch/ai/recommendations/generate` - Generate AI recommendations

### Government Schemes
- `GET /api/v1/schemes/` - List all schemes
- `GET /api/v1/schemes/search?query=water` - Search schemes (RAG)

### Multilingual
- `GET /api/v1/i18n/languages` - Supported languages
- `GET /api/v1/i18n/translate/{key}?lang=mr` - Translate UI labels
