from pathlib import Path
from typing import Any, ContextManager, Generator, Iterable, Self, TypeAlias

from anystore.store.virtual import VirtualIO
from banal import ensure_dict
from followthemoney import model
from followthemoney.proxy import EntityProxy
from ftmq.util import get_dehydrated_proxy
from ftmstore.loader import BulkLoader
from procrastinate.app import App
from pydantic import BaseModel, ConfigDict

from openaleph_procrastinate import helpers


class EntityFileReference(BaseModel):
    """
    A file reference (via `content_hash`) to a servicelayer file from an entity
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    dataset: str
    content_hash: str
    entity: EntityProxy

    def open(self: Self) -> ContextManager[VirtualIO]:
        """
        Open the file attached to this job
        """
        return helpers.open_file(self.dataset, self.content_hash)

    def get_localpath(self: Self) -> ContextManager[Path]:
        """
        Get a temporary path for the file attached to this job
        """
        return helpers.get_localpath(self.dataset, self.content_hash)


class Job(BaseModel):
    """
    A job with arbitrary payload
    """

    queue: str
    task: str
    payload: dict[str, Any]

    @property
    def context(self) -> dict[str, Any]:
        """Get the context from the payload if any"""
        return ensure_dict(self.payload.get("context")) or {}

    def defer(self: Self, app: App) -> None:
        """Defer this job"""
        data = self.model_dump(mode="json")
        app.configure_task(name=self.task, queue=self.queue).defer(**data)


class DatasetJob(Job):
    """
    A job with arbitrary payload bound to a `dataset`.
    The payload always contains an iterable of serialized `EntityProxy` objects
    in the `entities` key. It may contain other payload context data in the
    `context` key.

    There are helpers for accessing archive files or loading entities.
    """

    dataset: str

    def get_writer(self: Self) -> ContextManager[BulkLoader]:
        """Get the writer for the dataset of the current job"""
        return helpers.entity_writer(self.dataset)

    def get_entities(self) -> Generator[EntityProxy, None, None]:
        """
        Get the entities from the payload
        """
        assert "entities" in self.payload, "No entities in payload"
        for data in self.payload["entities"]:
            yield model.get_proxy(data)

    def load_entities(self: Self) -> Generator[EntityProxy, None, None]:
        """Load the entities from the store to refresh it to the latest data"""
        assert "entities" in self.payload, "No entities in payload"
        for data in self.payload["entities"]:
            yield helpers.load_entity(self.dataset, data["id"])

    # Helpers for file jobs that access the servicelayer archive

    def get_file_references(self) -> Generator[EntityFileReference, None, None]:
        """
        Get file references per entity from this job

        Example:
            ```python
            # process temporary file paths
            for reference in job.get_file_references():
                with reference.get_local_path() as path:
                    subprocess.run(["command", "-i", str(path)])
                # temporary path will be cleaned up when leaving context

            # process temporary file handlers
            for reference in job.get_file_references():
                with reference.open() as handler:
                    do_something(handler.read())
                # temporary path will be cleaned up when leaving context
            ```

        Yields:
            The file references
        """
        for entity in self.get_entities():
            for content_hash in entity.get("contentHash", quiet=True):
                yield EntityFileReference(
                    dataset=self.dataset, entity=entity, content_hash=content_hash
                )

    # Helpers for creating entity jobs

    @classmethod
    def from_entities(
        cls,
        dataset: str,
        queue: str,
        task: str,
        entities: Iterable[EntityProxy],
        dehydrate: bool | None = False,
        **context: Any,
    ) -> Self:
        """
        Make a job to process entities for a dataset

        Args:
            dataset: Name of the dataset
            queue: Name of the queue
            task: Python module path of the task
            entities: Entities
            dehydrate: Reduce entity payload to only a reference (tasks should
                re-fetch these entities from the store)
            context: Job context
        """
        if dehydrate:
            entities = map(get_dehydrated_proxy, entities)
        return cls(
            dataset=dataset,
            queue=queue,
            task=task,
            payload={
                "entities": [e.to_full_dict() for e in entities],
                "context": ensure_dict(context),
            },
        )

    @classmethod
    def from_entity(
        cls,
        dataset: str,
        queue: str,
        task: str,
        entity: EntityProxy,
        dehydrate: bool | None = False,
        **context: Any,
    ) -> Self:
        """
        Make a job to process an entity for a dataset

        Args:
            dataset: Name of the dataset
            queue: Name of the queue
            task: Python module path of the task
            entity: The entity proxy
            dehydrate: Reduce entity payload to only a reference (tasks should
                re-fetch these entities from the store)
            context: Job context
        """
        return cls.from_entities(
            dataset=dataset,
            queue=queue,
            task=task,
            entities=[entity],
            dehydrate=dehydrate,
            **context,
        )


AnyJob: TypeAlias = Job | DatasetJob
Defers: TypeAlias = None | Generator[AnyJob, None, None]
