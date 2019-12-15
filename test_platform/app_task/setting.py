import os
from test_platform.settings import BASE_DIR

EXTEND_DIR = os.path.join(BASE_DIR, "app_task", "extend")
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RUN = os.path.join(EXTEND_DIR, "task_run.py")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")
