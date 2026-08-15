# Setup

Steps to turn a copy of this template into a working project.

## 1. Create the repository

Use GitHub's **Use this template** button rather than cloning - this will gives you a
fresh history with no link back to the template.

## 2. Rename the project

In `README.md` update: 

- `[Project name]`

In `README.md` abd `SETUP.md` update: 

- all instances of `<project>`

In `pyproject.toml`, update:

- `name` - your project's name
- `description`

The `poetry.lock` remains valid after this change (the lock hash is computed
from dependency-relevant fields only). Confirm with:

```zsh
poetry check --lock
```

## 3. Create your local environment file

```zsh
cp .env.example .env
```

Replace the placeholder `SECRET_KEY` with a real value:

```zsh
python3 -c "import secrets; print(secrets.token_hex(32))"
```

`.env` is git-ignored - never commit it. The placeholder works for a first
run, but forms (CSRF) sign tokens with this key, so set a real one before
doing anything you care about.

## 4. Install dependencies

```zsh
poetry install
```

Note: plain `poetry install`, **not** `poetry install --only main` - the
latter is the Dockerfile's variant, which skips the dev tools (pytest, Ruff).

## 5. Verify

Each of these should pass on a fresh setup:

```zsh
poetry run pytest          # 1 passed - the /health contract test
poetry run ruff check .    # clean
docker build -t <project> .
docker run -p 8000:8000 --rm <project>
```

Then, from another terminal:

```zsh
curl -i http://localhost:8000/health    # 200, {"status":"ok"}
```

And in a browser: load http://localhost:8000/, submit the form - a redirect
to `/first-page/` proves the whole chain (CSRF → session cookie → state
machine → route lookup).

## 6. Make it yours

Starting points, in the order you'll likely touch them:

- `content/content.yaml` - page content (YAML-driven content is the pattern;
  see `lib/content.py`)
- `constants.py` + `lib/state_machine.py` - routes and the transitions
  between them
- `routes.py`, `templates/`, `forms/` - views, markup, forms
- `static/main.css` - design tokens are structured as primitives → semantic
  aliases; fill in your own values

Keep `/health` dependency-free: it answers "can this process serve HTTP?",
nothing more.

## Deployment

Deliberately not included. This template covers local development only;
deployment (platform choice, registry, secrets management) is a per-project
decision. `gtvj/choices` has a worked App Platform + DOCR example in its
`docs/DEPLOY.md`.
