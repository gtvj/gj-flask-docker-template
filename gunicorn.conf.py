import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
accesslog = "-"

# gthread: the main thread accepts connections, a thread pool handles
# requests — an idle/speculative browser connection no longer blocks
# everything. This is why sync (the default) fell over locally.
worker_class = "gthread"
threads = 4
workers = 2