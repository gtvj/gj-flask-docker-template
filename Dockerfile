# Start from a minimal Debian-based image with Python 3.11 preinstalled.
# "-slim" omits extras (man pages, build tooling) to keep the image small.
FROM python:3.11-slim

# Don't write .pyc bytecode files - wasted effort in a disposable container.
ENV PYTHONDONTWRITEBYTECODE=1
# Flush stdout/stderr immediately so logs appear in `docker logs` in real time.
ENV PYTHONUNBUFFERED=1
# Pin Poetry's version so the build is reproducible.
ENV POETRY_VERSION=2.4.1
# Install packages into the system environment, not a nested virtualenv -
# the container itself is the isolation boundary, so a venv would add nothing.
ENV POETRY_VIRTUALENVS_CREATE=false
# Never prompt for input during the build; fail instead.
ENV POETRY_NO_INTERACTION=1

# Install Poetry itself, via pip. --no-cache-dir avoids leaving pip's download
# cache behind in this layer, keeping the image smaller.
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Set /app as the working directory (created if it doesn't exist).
# Every COPY, RUN and CMD after this runs relative to /app.
WORKDIR /app

# Copy ONLY the dependency manifests first. Docker caches each layer, so as long
# as these two files are unchanged, the install step below is reused from cache -
# editing your application code won't trigger a dependency reinstall.
COPY pyproject.toml poetry.lock ./

# Install the locked runtime dependencies. --only main skips the dev group
# (pytest, ruff), which you don't need inside the running image.
RUN poetry install --only main

# Copy the rest of the source. It goes last because it changes most often;
# a code edit then only invalidates this cheap layer, not the install above.
COPY . .

# Document the port the app listens on. NOTE: this does NOT publish the port -
# you still need `docker run -p 8000:8000` (or Compose) to reach it from the host.
EXPOSE 8000

# The command run when the CONTAINER STARTS (not during the build). gunicorn
# serves the WSGI callable `app` from app.py (your module-level app = create_app()).
# Binding to 0.0.0.0 rather than 127.0.0.1 is what makes it reachable from outside.
# Port set in gunicorn.conf.py to retrive environment variable or fallback to 8000
CMD ["gunicorn", "app:app"]
