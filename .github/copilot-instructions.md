# Copilot Instructions for SaaS CRM Codebase

## Overview
This monorepo contains a SaaS CRM system with two main components:
- **Backend**: FastAPI app (Python) in `backend/`
- **Frontend**: React app (JavaScript, Reshaped.so UI) in `frontend/`

## Architecture
- **Backend**
  - Entrypoint: `backend/app/main.py` (FastAPI)
  - Modular structure: `sales/`, `marketing/`, `support/` under `backend/app/`
  - Each module is a Python package with its own API endpoints and logic
  - Run with: `uvicorn app.main:app --reload` from `backend/`
- **Frontend**
  - Entrypoint: `frontend/src/index.js`
  - Modular structure: `sales/`, `marketing/`, `support/` under `frontend/src/modules/`
  - Uses [Reshaped.so](https://reshaped.so) for UI components
  - Run with: `npm start` from `frontend/`

## Developer Workflows
- **Backend**
  - Install dependencies: `pip install -r requirements.txt`
  - Start dev server: `uvicorn app.main:app --reload`
  - Add new modules under `app/` as Python packages
- **Frontend**
  - Install dependencies: `npm install`
  - Start dev server: `npm start`
  - Add new modules under `src/modules/` as folders with a main dashboard component

## Conventions & Patterns
- **Module boundaries** are strictly enforced: no cross-imports between `sales`, `marketing`, `support` modules
- **API endpoints** are defined per module in backend; keep RESTful conventions
- **Frontend modules** mirror backend modules for feature alignment
- **UI**: Use Reshaped.so components for all new UI in frontend
- **No monolithic files**: keep logic split by module and feature

## Integration Points
- **Frontend-backend communication**: via REST API endpoints defined in backend modules
- **No direct database access from frontend**
- **Shared module names**: keep naming consistent between frontend and backend for clarity

## Examples
- To add a new feature to Sales:
  - Backend: add to `backend/app/sales/`
  - Frontend: add to `frontend/src/modules/sales/`

## References
- See `backend/README.md` and `frontend/README.md` for more details on each part

---

*Update this file if you introduce new modules, change conventions, or add major integration points.*
