# Apple Notes App (Vanilla JS)

A lightweight Apple Notes-style web app.

## Features
- Create notes
- Edit title and content
- Search notes
- Delete notes
- Auto-save to `localStorage`

## Run locally
```bash
cd apple-notes-app
python3 -m http.server 8000
```
Then open <http://localhost:8000>.

## Publish publicly (GitHub Pages)
This repository includes a workflow that deploys `apple-notes-app/` to GitHub Pages when you push changes.

### One-time setup
1. Push this repository to GitHub.
2. In GitHub: **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Push to `main`, `master`, or `work` branch (or run the workflow manually).

### Public URL
After deployment, your public app URL will be:

`https://<your-github-username>.github.io/<your-repo-name>/`
