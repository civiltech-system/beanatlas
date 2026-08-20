# Firebase Authentication implementation handoff

## Workspace to open

Open `/Users/ct002/IdeaProjects/BeanAtlas` as the Codex workspace so both repositories are writable:

- `beanatlas/` — public application repository
- `beanatlas-private/` — private deployment repository

## Secret environment file

The Firebase Web configuration is already stored at:

```text
beanatlas-private/.secret/.env.local
```

Do not print or copy its values into source files, logs, chat, or Git. It currently defines:

```text
VITE_FIREBASE_API_KEY
VITE_FIREBASE_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID
VITE_FIREBASE_STORAGE_BUCKET
VITE_FIREBASE_MESSAGING_SENDER_ID
VITE_FIREBASE_APP_ID
```

Change its filesystem mode to `600`. `beanatlas-private/.gitignore` already ignores `.env` and
`.env.*`; files under `.secret/` are also ignored.

## Next deployment change

Update `beanatlas-private/deploy/deploy.sh` to:

1. Resolve `beanatlas-private/.secret/.env.local` relative to the script.
2. Fail without displaying values if the file or any of the six variables above is missing.
3. Load it with `set -a`, `source`, `set +a` before running the frontend build.
4. Run the existing `npm run build`; Vite embeds `VITE_FIREBASE_*` at build time.
5. Continue using the existing rsync deployment for `frontend/dist` and the backend.

The frontend `.env.local` does not need to be copied to the VPS because it is build-time
configuration. Never publish `.env.local` under the Nginx document root.

## Backend Firebase Admin configuration still required

The FastAPI implementation verifies Firebase ID tokens using `firebase-admin`. The VPS also needs a
Firebase Admin service-account JSON stored outside both repositories. Configure the systemd service
with:

```ini
Environment="GOOGLE_APPLICATION_CREDENTIALS=/secure/path/firebase-service-account.json"
Environment="FIREBASE_PROJECT_ID=the-same-firebase-project-id"
```

Do not put the service-account JSON content in the frontend `.env.local`.

## Implementation status in `beanatlas`

The current working tree contains uncommitted Firebase Authentication and coffee-record changes:

- Email/password registration, login, logout, and auth route guards
- Firebase Web SDK configuration from `VITE_FIREBASE_*`
- Authenticated coffee record create/list/update/delete UI
- FastAPI Firebase ID-token verification
- User-owned `coffee_record` SQLAlchemy model and CRUD API
- Firebase setup documentation and dependency updates

Validation already completed:

- `npm run build --prefix frontend` passes
- Python compile check passes
- Coffee-record service integration test passes with Firebase verification stubbed

The real Firebase login cannot be tested until the Web config is loaded during the build and the
VPS has Firebase Admin credentials.
