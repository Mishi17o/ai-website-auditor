# AI Website Auditor

**Autonomous AI agent demo** by Mihai Popoviciu – Founder & CEO of ArvixAI.

Scans any website (1-2 pages), uses Gemini 1.5 Flash (free) to deliver a structured, scored report on **SEO, UX, Accessibility, Performance & Content** with actionable suggestions.

### Why this matters for ArvixAI

This is the first public proof that we can build **autonomous AI agents**.  
Next milestones:

- Agent that not only audits but proposes & applies code fixes
- Self-improving loop (agent audits its own output)
- Integration with sovereign AI models for 4D holographic interfaces

### Tech Stack

- Python 3.11+
- Streamlit (UI)
- BeautifulSoup + Requests (crawling)
- Google Gemini 1.5 Flash (free tier)
- Fully modular for easy extension into full agents

### Quick Start

```bash
git clone https://github.com/yourusername/ai-website-auditor.git
cd ai-website-auditor
pip install -r requirements.txt
cp .env.example .env
# → Add your free Gemini key from https://aistudio.google.com/app/apikey
streamlit run app.py
```
