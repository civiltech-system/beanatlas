# BeanAtlas

**An interactive world map of coffee origins.**
Explore where your coffee comes from — click any origin to discover its flavor profile, altitude, varieties, and processing methods.

🌐 **[beanatlas.net](https://beanatlas.net)**

![BeanAtlas preview](docs/preview.png)

---

## Features

- 🗺️ Interactive world map powered by MapLibre GL JS + OpenStreetMap
- ☕ 20 major coffee-producing countries with detailed profiles
- 📊 Flavor indicators: acidity, bitterness, sweetness, body
- 📱 Responsive design — works on mobile and desktop

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite + TypeScript |
| Styling | Tailwind CSS v4 |
| Map | MapLibre GL JS + OpenStreetMap |
| Backend | FastAPI (Python 3.12) |
| Database | SQLite (local) / PostgreSQL + PostGIS (production) |
| Server | Nginx + systemd on VPS |

---

## Project Structure

```
BeanAtlas/
├── frontend/               # Vue 3 frontend
│   └── src/
│       ├── components/     # MapView, OriginCard, FlavorIndicator
│       ├── views/          # HomeView, OriginsView, OriginDetailView
│       ├── stores/         # Pinia state management
│       ├── api/            # API client
│       └── types/          # TypeScript types
├── backend/                # FastAPI backend
│   └── app/
│       ├── main.py         # App entry point
│       ├── models.py       # SQLAlchemy models
│       ├── schemas.py      # Pydantic schemas
│       ├── seed.py         # Initial data (20 origins)
│       └── routers/        # API routes
└── deploy/                 # Deployment config
    ├── nginx.conf
    ├── api-beanatlas.service
    ├── setup-server.sh     # First-time server setup
    └── deploy.sh           # Deploy script
```

---

## Local Development

### Prerequisites

- Node.js 18+
- Python 3.12+

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# → http://localhost:8000
# → API docs: http://localhost:8000/docs
```

The frontend dev server proxies `/api/*` to `http://localhost:8000`, so both run together without CORS issues.

---

## API

```
GET /api/v1/origins          # List all origins
GET /api/v1/origins/{slug}   # Get origin detail
GET /api/v1/health           # Health check
GET /api/v1/records          # My coffee records (authentication required)
POST /api/v1/records         # Create a coffee record
PUT /api/v1/records/{id}     # Update my coffee record
DELETE /api/v1/records/{id}  # Delete my coffee record
```

## Firebase Authentication setup

BeanAtlas uses Firebase Authentication for email/password accounts. Coffee records remain in the
BeanAtlas SQL database and are scoped to the verified Firebase user ID.

1. Create a project in the [Firebase console](https://console.firebase.google.com/).
2. Add a Web app from **Project settings > General > Your apps** and copy its Firebase config.
3. In **Authentication > Sign-in method**, enable **Email/Password**.
4. In **Authentication > Settings > Authorized domains**, add `beanatlas.net` and
   `www.beanatlas.net`. Add `localhost` separately when local development needs it.
5. Copy `frontend/.env.example` to `frontend/.env.local` and enter the Web app values:

```dotenv
VITE_FIREBASE_API_KEY=...
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=...
VITE_FIREBASE_APP_ID=...
```

Vite embeds these public Web app settings at build time, so set them before `npm run build` on the
production server. They are identifiers, not an Admin credential.

For FastAPI, open **Project settings > Service accounts**, generate a private key, and store the
downloaded JSON outside the repository. Set these variables in the API systemd service:

```ini
Environment="GOOGLE_APPLICATION_CREDENTIALS=/secure/path/firebase-service-account.json"
Environment="FIREBASE_PROJECT_ID=your-project-id"
```

Install the dependency and restart the API:

```bash
cd backend
.venv/bin/pip install -r requirements.txt
sudo systemctl daemon-reload
sudo systemctl restart api-beanatlas
```

Rebuild and publish the frontend after setting its environment variables:

```bash
cd frontend
npm ci
npm run build
```

Never commit the service-account JSON. Firebase Web config values may be public, but configure API
key restrictions and Authentication authorized domains in Google Cloud/Firebase Console.

## Data Sources

Origin data compiled from SCA, ICO, and national coffee boards.
Map tiles © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors.

---

## License

MIT
