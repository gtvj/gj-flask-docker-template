> [!IMPORTANT]  
> Don't clone this template repository. Choose "Use this template" instead.
> Why? Because there are [helpful differences](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) when using this approach

# [Project name]

Built from [gtvj/gj-flask-docker-template](https://github.com/gtvj/gj-flask-docker-template):
Flask with blueprint-based routes, YAML-driven content, a state machine for
page transitions, managed with Poetry and containerised with Docker.

New clone? See [SETUP.md](SETUP.md) first.

## Requirements

- Docker - for the containerised workflow (recommended), **or**
- Python 3.11+ and Poetry - for local development and tooling

## Local development with Docker

Build the image:

```zsh
docker build -t <project> .
```

Run it:

```zsh
docker run -p 8000:8000 --rm <project>
```

Open http://localhost:8000/.

### With auto-reload

Bind-mounts the local source so the app restarts when files change:

```zsh
docker run -p 8000:8000 --rm \
  -v "$(pwd):/app" \
  -e TEMPLATES_AUTO_RELOAD=1 \
  <project> gunicorn --reload app:app
```

Two things to know about reload:

- `--reload` watches **Python files only**. `TEMPLATES_AUTO_RELOAD=1` covers
  templates (Flask otherwise caches them once compiled). CSS and YAML content
  are re-read per request anyway.
- Changing dependencies still requires a rebuild.

<details>
<summary>Development without Docker</summary>

Requires Python 3.11+ (the Python that ships with macOS is older and won't
satisfy the project's constraint).

```zsh
poetry install
poetry run flask --app app:create_app --debug run
```

Open http://127.0.0.1:5000/. Flask's `--debug` gives you reload and the
interactive debugger; no gunicorn involved.

</details>

## Development commands

```zsh
poetry run ruff format .   # format
poetry run ruff check .    # lint
poetry run pytest          # tests
```

## Health check

`GET /health` returns `{"status": "ok"}` - dependency-free by design, it
answers "can this process serve HTTP?" and nothing more. Keep template
renders and service calls out of it; it's covered by a test that pins the
contract.

## Logs

gunicorn writes boot/errors *and* per-request access logs to
stdout/stderr (`accesslog = "-"` in `gunicorn.conf.py`), so:

```zsh
docker logs -f <container>   # or just watch the foreground terminal
```

If you're debugging "the app does nothing", the access log line
(`"POST / HTTP/1.1" 200` vs `302`) is usually the first thing to check.