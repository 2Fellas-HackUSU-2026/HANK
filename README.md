# HANK

HANK (Hazard Assessment and Navigation Kit) is a lightweight web app built for the **2026 USU Hackathon**.  
It helps users generate:

- action steps for a job workflow,
- hazards related to each action, and
- practical controls to reduce risk.

The app uses FastAPI for the backend/UI serving and OpenAI structured outputs for hazard/control generation.

## What It Does

1. User enters a job/ occupational field topic (for example: `Excavation`).
2. User adds an action step (for example: `Subgrade excavation`).
3. HANK generates hazards for that action.
4. HANK generates controls for each hazard.
5. Results are saved to local JSON storage.

## Tech Stack

- Python 3
- FastAPI + Uvicorn
- Jinja2 templates + vanilla JavaScript
- OpenAI Python SDK (`chat.completions.parse` + Pydantic response models)
- Local JSON persistence (`data/actions_storage.json`)

## Project Structure

```text
HANK/
├── API/
│   ├── app.py
│   └── routes/
│       ├── backend_routes.py
│       └── frontend_routes.py
├── agent/
│   └── agent.py
├── config/
│   ├── .env
│   └── .env-example
├── data/
│   └── actions_storage.json
├── static/
│   └── images/HANK.png
├── templates/
│   ├── index.html
│   └── actions.html
├── tools/
│   ├── backend_route_tools.py
│   └── save_data.py
├── main.py
└── requirements.txt
```

## Prerequisites

- Python 3.10+ (3.11 recommended)
- An OpenAI API key

## Local Setup

```bash
# 1) Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure environment variables
cp config/.env-example config/.env
# then edit config/.env and set OPEN_AI_KEY
```

## Run the App

```bash
python main.py
```

Server starts on:

`http://localhost:8001`

Pages:

- `GET /` -> topic input page
- `GET /actions` -> hazard assessment workflow

## API Endpoints

All endpoints below are `POST`.

- `/api/set-user-topic?topic=<topic>`
- `/api/add-action-step?action=<action>`
- `/api/add-hazard?topic=<topic>&action=<action>`
- `/api/add-control?topic=<topic>&action=<action>&hazard=<hazard>`

Example:

```bash
curl -X POST "http://localhost:8001/api/add-hazard?topic=Vacuum%20Excavation&action=Subgrade%20excavation"
```

## Data Model (Persisted JSON)

Data is stored in `data/actions_storage.json` using this structure:

```json
[
  {
    "action": "Subgrade excavation",
    "hazards": [
      {
        "hazard": "Cave-ins",
        "controls": [
          "Use trench boxes",
          "Inspect excavation daily"
        ]
      }
    ]
  }
]
```

`tools/save_data.py` normalizes malformed entries and merges duplicate actions/hazards/controls.

## Known Limitations

- Persistence is file-based (local JSON), not a database.
- No authentication or multi-user separation yet.

## Troubleshooting

- `API Error` in terminal:
  - Verify `config/.env` exists and includes a valid `OPEN_AI_KEY`.
- Empty/invalid JSON behavior:
  - `load_actions()` safely falls back to an empty list if JSON is invalid.
- Frontend not loading styles/images:
  - Ensure `app.mount("/static", StaticFiles(directory="static"), name="static")` is unchanged.

## Hackathon Context

This project was created during the **2026 USU Hackathon** as a fast, practical safety assistant prototype.
