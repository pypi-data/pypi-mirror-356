import time

from .classification_model import ClassificationModel
from .datasource import Datasource
from .job import Job, Status


def test_job_creation(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    assert job.id is not None
    assert job.type == "EVALUATE_MODEL"
    assert job.status in [Status.DISPATCHED, Status.PROCESSING]
    assert job.created_at is not None
    assert job.updated_at is not None
    assert job.refreshed_at is not None
    assert len(Job.query(limit=5, type="EVALUATE_MODEL")) >= 1


def test_job_result(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    result = job.result(show_progress=False)
    assert result is not None
    assert job.status == Status.COMPLETED
    assert job.steps_completed is not None
    assert job.steps_completed == job.steps_total


def test_job_wait(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    job.wait(show_progress=False)
    assert job.status == Status.COMPLETED
    assert job.steps_completed is not None
    assert job.steps_completed == job.steps_total
    assert job.value is not None


def test_job_refresh(classification_model: ClassificationModel, datasource: Datasource):
    job = classification_model.evaluate(datasource, background=True)
    last_refreshed_at = job.refreshed_at
    # accessing the status attribute should refresh the job after the refresh interval
    Job.set_config(refresh_interval=1)
    time.sleep(1)
    job.status
    assert job.refreshed_at > last_refreshed_at
    last_refreshed_at = job.refreshed_at
    # calling refresh() should immediately refresh the job
    job.refresh()
    assert job.refreshed_at > last_refreshed_at
