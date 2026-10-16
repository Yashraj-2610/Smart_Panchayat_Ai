#!/usr/bin/env python3
"""
Presentation Builder Script — Review II (Smart Panchayat AI)
Maps repo deliverables (commit 5d26000) to SY_Project_Review_II_Template.pptx
No external .env edits; all data from repo / synthetic demo data.

Attribution required:
Co-Authored-By: Claude Code <noreply@anthropic.com>
🤖 Generated with [Claude Code](https://claude.com/claude-code)
"""
import os

TEMPLATE = "/c/Users/yashr/Downloads/Minor Project/SY_Project_Review_II_Template.pptx"
REPO = "https://github.com/Yashraj-2610/Smart_Panchayat_Ai"
COMMIT = "5d26000"

SLIDES = [
    ("1. Cover", "Smart Panchayat AI — AI-Powered Decision Support\nMinor Project Review II | Oct 2026\nAlandi Gram Panchayat, Pune, Maharashtra"),
    ("2. Problem", "Village-level data gap; no real-time analytics for panchayat decisions.\nSensitive PII (Aadhaar/phone) requires E2E encryption + role-based access.\nNeed: multi-agent analysis + government scheme matching."),
    ("3. Objectives", "• Multi-agent AI (Pop / Water / Health / Edu / Infra / Predictive)\n• Role privacy: Family Head → System Admin (4 levels)\n• Scheme matching + multilingual (en/hi/mr) + audit logging"),
    ("4. Architecture", "FastAPI + Streamlit | SQLAlchemy ORM | JWT + bcrypt | Fernet E2E\nMiddleware: rate limit, request-ID, structured errors, DB health\nPrivacy layer: PRIVACY_LEVELS + OPERATION_PERMISSIONS (backend + frontend)"),
    ("5. Phase 1", "DB migration • pytest framework • rate-limiting middleware • structured error responses\nCommit 1cb5c70 • No .env edits — all defaults in code"),
    ("6. Phase 2", "6 AI agents with confidence scoring + trend analysis + scheme matching\nNew predictive agent • enhanced security • audit logging\nCommit 53d7ea6"),
    ("7. Phase 3", "GIS ward-map component (Plotly) + voice STT/TTS interface\nMobile-ready design deferred to future\nCommit 92f4005"),
    ("8. Phase 4", "Professional UI (Inter font, cards, badges) • landing page with role tabs\nPrivacy/access layer: privacy.py + styles.py + landing_page.py\nLaunch-ready (demo/synthetic data)\nCommit 5d26000"),
    ("9. Privacy & Access", "PRIVACY_LEVELS: PUBLIC(1) → INTERNAL(2) → CONFIDENTIAL(3) → RESTRICTED(4)\nROLE_ACCESS: Family Head / Panchayat Admin / Sarpanch / System Admin\nField masking (Aadhaar/phone/email/income) + audit middleware"),
    ("10. Results / Demo", "Sarpanch dashboard (5 tabs) vs Family Head (4 tabs)\nRole badges + privacy badges (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED)\nSynthetic data — real government API integration future work"),
    ("11. Conclusion", "Repo: github.com/Yashraj-2610/Smart_Panchayat_Ai (main = origin/main)\nRender deploy ready (render.yaml) • Review 2 submitted • Mobile deferred\nCo-Authored-By: Claude Code <noreply@anthropic.com>"),
]

OUTPUT = "presentation/review_II_smart_panchayat.md"

def build():
    with open(OUTPUT, "w") as f:
        f.write("# Smart Panchayat AI — Review II Presentation\n")
        f.write(f"Template: {TEMPLATE}\n")
        f.write(f"Repo: {REPO} @ {COMMIT}\n")
        f.write(f"Generated: 2026-10-16\n")
        f.write("\n---\n")
        for idx, (title, body) in enumerate(SLIDES, 1):
            f.write(f"\n## Slide {idx}: {title}\n\n{body}\n")
        f.write("\n---\n")
        f.write("**Attribution:**\n")
        f.write("Co-Authored-By: Claude Code <noreply@anthropic.com>\n")
        f.write("🤖 Generated with [Claude Code](https://claude.com/claude-code)\n")
    print(f"Built: {OUTPUT} ({len(SLIDES)} slides)")

if __name__ == "__main__":
    build()
