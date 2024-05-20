# gunicorn_conf.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8000'
loglevel = 'info'
