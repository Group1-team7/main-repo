# Demo Script

## Setup

1. Start the backend:
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd web
   npm install
   npm run dev
   ```

## Walkthrough

1. Open `http://localhost:3000`.
2. Paste `data/sample_contracts/contract_002.txt`.
3. Click Analyze.
4. Point out clause count, detected risk cards, citation placeholders, and disclaimer.
5. Ask scoped chat: `List the top risks`.
6. Ask refused chat: `Should I sign this?`

## Demo Notes

- TODO[PERSON-4]: Replace this with final screen-by-screen narration.
- Say clearly that source snippets are placeholders until PERSON-1 manually verifies official Jordanian sources.
- Do not describe any clause as illegal.
