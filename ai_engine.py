import os
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types  

# ────────────────────────────────────────────────
#   Load API key reliably
# ────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

print(f"[ENV] Looking for .env at: {env_path}")
print(f"[ENV] File exists? {env_path.exists()}")
print(f"[ENV] File readable? {os.access(env_path, os.R_OK) if env_path.exists() else False}")

loaded = load_dotenv(env_path, override=True)
print(f"[ENV] load_dotenv() success: {loaded}")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print(f"[ENV] GEMINI_API_KEY loaded successfully (length: {len(GEMINI_API_KEY)})")
else:
    print("[ENV] GEMINI_API_KEY NOT FOUND in environment")
    print("[ENV] Raw os.environ check:", 'GEMINI_API_KEY' in os.environ)

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("[GENAI] Successfully configured")
else:
    print("[ERROR] No valid GEMINI_API_KEY → report generation will fail")

def generate_audit_report(crawled_data: dict) -> dict:
    if not GEMINI_API_KEY:
        return {
            "overall_score": 0,
            "categories": {
                "Error": {
                    "score": 0,
                    "issues": ["Gemini API key missing"],
                    "suggestions": ["Verify .env → GEMINI_API_KEY=your_key_here (no spaces/quotes)"]
                }
            }
        }

    try:
        model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=types.GenerationConfig(  
        response_mime_type="application/json",
        temperature=0.2,
    )
)

        prompt = f"""You are a senior web auditor.
Analyze this website snapshot and return **ONLY** valid JSON matching this structure:

{{
  "overall_score": <int 0-100>,
  "categories": {{
    "SEO": {{"score": <0-100>, "issues": ["str"], "suggestions": ["str"]}},
    "UX": {{"score": <0-100>, "issues": ["str"], "suggestions": ["str"]}},
    "Accessibility": {{"score": <0-100>, "issues": ["str"], "suggestions": ["str"]}},
    "Performance": {{"score": <0-100>, "issues": ["str"], "suggestions": ["str"]}},
    "Content": {{"score": <0-100>, "issues": ["str"], "suggestions": ["str"]}}
  }}
}}

Website data:
{json.dumps(crawled_data, indent=2, ensure_ascii=False)}

Rules: Return pure JSON only — no markdown, no explanations, no backticks.
"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean common wrappers
        if text.startswith("```json"):
            text = text[7:].rsplit("```", 1)[0].strip()
        elif text.startswith("```"):
            text = text[3:].rsplit("```", 1)[0].strip()

        parsed = json.loads(text)
        print("[GENAI] Successfully parsed JSON response")
        return parsed

    except Exception as e:
        print(f"[GENAI ERROR] {type(e).__name__}: {str(e)}")
        return {
            "overall_score": 0,
            "categories": {
                "Error": {
                    "score": 0,
                    "issues": [str(e)],
                    "suggestions": ["Check terminal logs, key validity, free tier quota"]
                }
            }
        }