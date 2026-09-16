# 🚀 Deployment Guide - Smart Panchayat AI

## Quick Deploy Options

### Option 1: Railway (Recommended - Free Tier)
Railway offers free deployment with 500 hours/month and $5 free credit.

**Steps:**
1. Install Railway CLI or use Web UI
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. Create a new project
   ```bash
   railway init
   ```

3. Deploy all services
   ```bash
   railway up
   ```

4. Add environment variables in Railway dashboard:
   - `SECRET_KEY` - Your secret key
   - `DATABASE_URL` - Will use SQLite by default

5. Get your public URLs from Railway dashboard

---

### Option 2: Render (Free Tier)
Render offers free web services with automatic deploys from GitHub.

**Steps:**
1. Go to [render.com](https://render.com)
2. Sign up and connect your GitHub repo
3. Create 3 Web Services:

**Backend API:**
- Name: `panchayat-backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python backend/init_db.py && uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Environment: Add `SECRET_KEY`, `DATABASE_URL=sqlite:///./backend/smart_panchayat.db`

**Family Portal:**
- Name: `panchayat-family-portal`
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run frontend/family_portal.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- Environment: Add `API_BASE_URL=https://panchayat-backend.onrender.com/api/v1`

**Sarpanch Dashboard:**
- Name: `panchayat-sarpanch`
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run frontend/sarpanch_dashboard.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- Environment: Add `API_BASE_URL=https://panchayat-backend.onrender.com/api/v1`

---

### Option 3: Fly.io (Free Tier - 3 VMs)

**Steps:**
1. Install Fly CLI:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Or download from https://fly.io/docs/hands-on/install-flyctl/
   ```

2. Login:
   ```bash
   flyctl auth login
   ```

3. Launch app:
   ```bash
   flyctl launch --name smart-panchayat-ai
   ```

4. Deploy:
   ```bash
   flyctl deploy
   ```

---

### Option 4: Docker (Self-Hosted)

**Local Testing:**
```bash
docker-compose up --build
```

**Access:**
- Backend API: http://localhost:8000
- Family Portal: http://localhost:8501
- Sarpanch Dashboard: http://localhost:8502

**Production Deploy on VPS:**
```bash
# Pull and run on your server
git clone https://github.com/Yashraj-2610/Smart_Panchayat_Ai.git
cd Smart_Panchayat_Ai
docker-compose up -d

# Setup reverse proxy (nginx/caddy) for HTTPS
```

---

### Option 5: Vercel + PythonAnywhere

**Frontend on Vercel (after React upgrade):**
- Deploy React app to Vercel
- Set environment variables

**Backend on PythonAnywhere:**
- Free tier supports Flask/FastAPI
- Upload code and configure WSGI

---

## Environment Variables Required

For all deployments, set these:

```env
DATABASE_URL=sqlite:///./backend/smart_panchayat.db
SECRET_KEY=your-production-secret-key-here
VILLAGE_NAME=Alandi Gram Panchayat
DISTRICT=Pune
STATE=Maharashtra
TOTAL_WARDS=6
DEFAULT_LANGUAGE=mr
SUPPORTED_LANGUAGES=en,hi,mr
```

---

## Post-Deployment Checklist

- [ ] Backend health check: `https://your-api.com/health`
- [ ] API docs accessible: `https://your-api.com/docs`
- [ ] Family portal loads correctly
- [ ] Sarpanch dashboard shows demo data
- [ ] Database initialized with wards and schemes
- [ ] All 3 services can communicate
- [ ] CORS configured properly
- [ ] Environment variables set

---

## Monitoring & Maintenance

**Check logs:**
```bash
# Railway
railway logs

# Render
# View in dashboard

# Fly.io
flyctl logs

# Docker
docker-compose logs -f
```

**Update deployment:**
```bash
git push origin main  # Auto-deploys on Render/Railway if configured
```

---

## Cost Estimates (as of 2026)

| Platform | Free Tier | Paid (if scaling) |
|----------|-----------|-------------------|
| Railway | 500 hrs/month + $5 credit | ~$5-20/month |
| Render | 750 hrs/month | $7-25/month |
| Fly.io | 3 VMs free | $2-15/month |
| Docker + VPS | N/A | $5-10/month (DigitalOcean/Linode) |

**Recommended for MVP:** Railway or Render (easiest, free tier sufficient)

---

## Troubleshooting

**Issue:** Services can't communicate
- Check API_BASE_URL is set correctly
- Ensure backend deploys first

**Issue:** Database resets on redeploy
- Use persistent volumes (Render disk, Railway volumes)
- Or upgrade to PostgreSQL

**Issue:** Streamlit shows "Connection error"
- Add `--server.headless true` to start command
- Check port configuration

---

## Next Steps After Deployment

1. ✅ Test all features with demo data
2. 🔐 Set up proper authentication
3. 📊 Migrate to PostgreSQL for production
4. 🎨 Plan React frontend upgrade
5. 🤖 Integrate RAG knowledge base
6. 📱 Make responsive for mobile
7. 🔒 Add SSL/HTTPS
8. 📈 Set up monitoring (Sentry, LogTail)

---

**Need help?** Check platform-specific docs:
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Fly.io Docs](https://fly.io/docs)
