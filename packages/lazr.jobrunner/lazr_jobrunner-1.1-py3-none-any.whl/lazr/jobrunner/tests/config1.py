import os

import oops

from lazr.jobrunner.tests.simple_config import *  # noqa: F401,F403

task_annotations = {
    "run_file_job": {
        "file_job_dir": os.environ.get("FILE_JOB_DIR", ""),
        "oops_config": oops.Config(),
    }
}
