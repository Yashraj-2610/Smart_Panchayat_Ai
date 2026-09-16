#!/bin/bash
# Startup script for production deployment

echo "🚀 Starting Smart Panchayat AI System..."

# Wait for database to be ready (if using external DB)
sleep 2

# Initialize database if not exists
echo "📊 Initializing database..."
python backend/init_db.py

# Seed demo data if DATABASE is empty
echo "🌱 Checking for demo data..."
python backend/seed_demo_data.py || echo "⚠️  Demo data seeding skipped"

echo "✅ Startup complete!"

# Start the application based on SERVICE_TYPE env variable
if [ "$SERVICE_TYPE" = "backend" ]; then
    echo "🔧 Starting Backend API..."
    uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
elif [ "$SERVICE_TYPE" = "family-portal" ]; then
    echo "👨‍👩‍👧 Starting Family Portal..."
    streamlit run frontend/family_portal.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
elif [ "$SERVICE_TYPE" = "sarpanch-dashboard" ]; then
    echo "🏛️ Starting Sarpanch Dashboard..."
    streamlit run frontend/sarpanch_dashboard.py --server.port 8502 --server.address 0.0.0.0 --server.headless true
else
    echo "❌ Unknown SERVICE_TYPE: $SERVICE_TYPE"
    exit 1
fi
