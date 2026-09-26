# FirstGear — KAM Induction Website + Chatbot (Streamlit)

Streamlit rebuild of the FirstGear prototype for Team 8's ALP: a Day 1-15
induction journey for new Key Account Managers at Padmini VNA, with an AI
chatbot that answers only from the FirstGear Knowledge Base.

This rebuild replaces the earlier single-file Claude artifact (which is
untouched and still live) with a real Python/Streamlit app whose chatbot
calls the Anthropic API for real, against the same knowledge base.

## What's built

- **Induction engine** — Days 1-15 from §8.1, each with content (from
  `data/knowledge_base/`), a session-attendance step, and a 5-question
  knowledge check (80% to pass, retake allowed). Days unlock in sequence.
- **Days 11-14 account brief** — a simple form the KAM fills in and saves.
- **Day-15 assessment** — 20 questions scored by pillar (Governance 25%,
  People 20%, Process 30%, Product 25%), banded Green/Amber/Red per §8.3.
- **Chatbot** — on every screen, aware of the KAM's current day/pillar,
  answers only from the knowledge base, cites sources, flags illustrative
  content, and declines pricing/commitment questions (explains the Day 6
  approver instead). Calls the real Anthropic API.
- **Dashboard** — Mentor/Manager/HR view of every KAM's day, completion,
  scores and Day-15 band.
- **Demo login** — role + shared password (`firstgear`); see
  `modules/data_store.py` for the demo accounts (Riya on Day 7, Arjun on
  Day 15, plus Mentor/Manager/HR).

## Not in this build (planned for Review-3)

Days 16-30 workflow, a real vector-search/RAG pipeline (the chatbot currently
sends the whole knowledge base as context — fine at this corpus size, not
scalable), calendar integration, live CRM data, AI role-play scenarios.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and paste your Anthropic API key

streamlit run app.py
```

## Deploying on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the repo,
   set the main file to `app.py`.
3. In the app's **Settings → Secrets**, paste:
   ```
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
4. Every push to the connected branch redeploys automatically.

## Demo script (from 00_Build_Spec.md)

1. Log in as **Riya Sharma** (password `firstgear`) → Day 7 (RFQ) is today.
2. Open the Day 7 module → read → mark session attended.
3. Ask the chatbot: *"What should I do after receiving an RFQ?"* → cited steps.
4. Ask: *"How much hotel allowance do I get in Pune as an Assistant Manager?"*
   → ₹5,000, cited from the HR Manual.
5. Ask: *"Can I give Aravalli a 5% discount?"* → declines, explains the
   Business Head/CFO approval per the Day 6 matrix.
6. Ask something not covered → says so, suggests who to ask.
7. Take the Day 7 check → pass → Day 8 unlocks.
8. Log out, log in as **Arjun Mehta** (Day 15) → take the readiness
   assessment → pillar scores and band.
9. Log out, log in as **Harit Bhasin** or **Dev Shetty** → see both KAMs'
   progress, scores and bands on the dashboard.

## Notes on the demo-progress store

`data/progress.json` is a small JSON file acting as a shared "database" for
the demo — it's what lets the Mentor/Manager/HR dashboard see the KAMs'
live progress across logins. It's gitignored and regenerates with default
demo data on first run. This is an interim approach for the prototype; a
real deployment would use a proper database.

## Knowledge base

See `data/knowledge_base/00_README_Source_Map.md` for what's real
(`[Source: ...]`), industry-standard, or `[Illustrative - Team 8]` — sample
content invented to fill gaps for the prototype and not Padmini VNA's actual
process, numbers or customers.
