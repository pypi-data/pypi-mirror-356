import os

import oops

broker_url = "amqp://"
result_backend = "rpc://"
imports = ("lazr.jobrunner.tests.test_celerytask",)
worker_concurrency = 1
task_queues = {
    "standard": {"routing_key": "job.standard"},
    "standard_slow": {"routing_key": "job.standard.slow"},
}
task_default_queue = "standard"
task_create_missing_queues = False
task_annotations = {
    "run_file_job": {
        "file_job_dir": os.environ.get("FILE_JOB_DIR", ""),
        "oops_config": oops.Config(),
    }
}
