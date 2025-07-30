import os

import oops

broker_url = "amqp://"
result_backend = "rpc://"
imports = ("lazr.jobrunner.tests.test_celerytask",)
worker_concurrency = 1
task_annotations = {
    "run_file_job": {
        "file_job_dir": os.environ.get("FILE_JOB_DIR", ""),
        "oops_config": oops.Config(),
    }
}
# Do not prefetch job data.
# See http://ask.github.com/celery/userguide/optimizing.html
worker_prefetch_multiplier = 1
task_acks_late = True
