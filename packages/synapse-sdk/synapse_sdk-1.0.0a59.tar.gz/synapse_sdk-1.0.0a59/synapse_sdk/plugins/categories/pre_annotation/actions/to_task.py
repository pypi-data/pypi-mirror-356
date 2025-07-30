import json
from datetime import datetime
from enum import Enum
from typing import Annotated

import requests
from pydantic import AfterValidator, BaseModel, field_validator
from pydantic_core import PydanticCustomError

from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod
from synapse_sdk.plugins.models import Run
from synapse_sdk.utils.pydantic.validators import non_blank


class AnnotationMethod(str, Enum):
    FILE = 'file'
    INFERENCE = 'inference'


class AnnotateTaskDataStatus(str, Enum):
    SUCCESS = 'success'
    FAILED = 'failed'


class ToTaskRun(Run):
    class AnnotateTaskDataLog(BaseModel):
        """Log model for annotate task data."""

        task_info: str | None
        status: AnnotateTaskDataStatus
        created: str

    class MetricsRecord(BaseModel):
        """Metrics record model."""

        stand_by: int
        failed: int
        success: int

    def log_annotate_task_data(self, task_info: dict, status: AnnotateTaskDataStatus):
        """Log annotate task data."""
        now = datetime.now().isoformat()
        self.log(
            'annotate_task_data',
            self.AnnotateTaskDataLog(task_info=json.dumps(task_info), status=status, created=now).model_dump(),
        )

    def log_metrics(self, record: MetricsRecord, category: str):
        """Log FileToTask metrics.

        Args:
            record (MetricsRecord): The metrics record to log.
            category (str): The category of the metrics.
        """
        record = self.MetricsRecord.model_validate(record)
        self.set_metrics(value=record.dict(), category=category)


class ToTaskParams(BaseModel):
    """ToTask action parameters.

    Args:
        name (str): The name of the action.
        description (str | None): The description of the action.
        project (int): The project ID.
        task_filter (dict): The filter of tasks.
        method (AnnotationMethod): The method of annotation.
        target_specification_name (str | None): The name of the target specification.
        pre_processor (int | None): The pre processor ID.
        pre_processor_params (dict): The params of the pre processor.
    """

    name: Annotated[str, AfterValidator(non_blank)]
    description: str | None = None
    project: int
    task_filter: dict
    method: AnnotationMethod | None = None
    target_specification_name: str | None = None
    pre_processor: int | None = None
    pre_processor_params: dict

    @field_validator('project', mode='before')
    @classmethod
    def check_project_exists(cls, value: str, info) -> str:
        """Validate synapse-backend project exists."""
        if not value:
            return value

        action = info.context['action']
        client = action.client
        try:
            client.get_project(value)
        except ClientError:
            raise PydanticCustomError('client_error', 'Error occurred while checking project exists.')
        return value


@register_action
class ToTaskAction(Action):
    """ToTask action class.

    * Annotate data to tasks.
    """

    name = 'to_task'
    category = PluginCategory.PRE_ANNOTATION
    method = RunMethod.JOB
    run_class = ToTaskRun
    progress_categories = {
        'annotate_task_data': {
            'proportion': 100,
        },
    }
    metrics_categories = {'annotate_task_data'}

    def start(self):
        """Start file_to_task action.

        * Generate tasks.
        * Annotate data to tasks.
        """

        # entrypoint = self.entrypoint(self.run)
        client = self.run.client
        # project_id = self.params['project']
        # project = client.get_project(project_id)
        # data_collection_id = project['dataset']
        # data_collection = client.get_dataset(data_collection_id)

        # Generate tasks if provided project is empty.
        task_ids_query_params = {
            'project': self.params['project'],
            'fields': 'id',
        }
        if self.params.get('task_filter'):
            task_ids_query_params.update(self.params['task_filter'])
        task_ids_generator, task_ids_count = client.list_tasks(params=task_ids_query_params, list_all=True)
        task_ids = [item['id'] for item in task_ids_generator]

        # If no tasks found, break the job.
        if not task_ids_count:
            self.run.log_message('Tasks to annotate not found.')
            self.run.end_log()

        # Annotate data to tasks.
        task_data_annotation_type = self.params['task_data_annotation_type']
        if task_data_annotation_type == AnnotationMethod.FILE:
            self._handle_annotate_data_from_files(task_ids)
        elif task_data_annotation_type == AnnotationMethod.INFERENCE:
            self._handle_annotate_data_with_inference(task_ids)

        return {}

    def _handle_annotate_data_from_files(self, task_ids: list[int]):
        """Handle annotate data from files to tasks.

        Args:
            task_ids (list[int]): List of task IDs to annotate data to.
        """
        client = self.run.client
        if not (target_task_data_specification_code := self.params.get('target_task_data_specification_code')):
            self.run.log_message('Target task data specification code not found.')
            self.run.end_log()
        task_params = {
            'fields': 'id,data,data_unit',
            'expand': 'data_unit',
        }
        for task_id in task_ids:
            task = client.get_task(task_id, params=task_params)
            data_file = task['data_unit']['files'].get(target_task_data_specification_code)
            if not data_file:
                self.run.log_message(f'File specification not found for task {task_id}')
                self.run.log_annotate_task_data(
                    {'task_id': task_id, 'error': 'File specification not found'}, AnnotateTaskDataStatus.FAILED
                )
                continue
            url = data_file.get('url')
            if not url:
                self.run.log_message(f'URL not found for task {task_id}')
                self.run.log_annotate_task_data(
                    {'task_id': task_id, 'error': 'URL not found'}, AnnotateTaskDataStatus.FAILED
                )
                continue

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for 4XX/5XX responses
                data = json.loads(response.content)
                client.patch_task(task_id, data={'data': data})

                # Log success
                self.run.log_annotate_task_data({'task_id': task_id, 'url': url}, AnnotateTaskDataStatus.SUCCESS)
            except Exception as e:
                self.run.log_message(f'Failed to get content from URL for task {task_id}: {str(e)}')
                self.run.log_annotate_task_data(
                    {'task_id': task_id, 'url': url, 'error': str(e)}, AnnotateTaskDataStatus.FAILED
                )
                continue

    def _handle_annotate_data_with_inference(self, task_ids: list[int]):
        """Handle annotate data with inference to tasks.

        Args:
            task_ids (list[int]): List of task IDs to annotate data to.
        """
        self.run.log_message('Pre annotation with inference is not supported.')
        self.run.end_log()
