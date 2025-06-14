# Copyright 2024-present, Extralit Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings
from abc import abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, List, Optional, Union, overload
from uuid import UUID

from argilla._api._base import ResourceAPI
from argilla._api._client import DEFAULT_HTTP_CONFIG  # noqa: F401
from argilla._api._webhooks import WebhookModel
from argilla._exceptions import ArgillaError, NotFoundError
from argilla._helpers import GenericIterator
from argilla._helpers._resource_repr import ResourceHTMLReprMixin
from argilla._models import DatasetModel, ResourceModel, UserModel, WorkspaceModel

if TYPE_CHECKING:
    from argilla import Dataset, User, Workspace, Webhook
    from argilla.client.core import Argilla

__all__ = ["Users", "Workspaces", "Datasets", "Webhooks"]


class Users(Sequence["User"], ResourceHTMLReprMixin):
    """A collection of users. It can be used to create a new user or to get an existing one."""

    class _Iterator(GenericIterator["User"]):
        pass

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = client.api.users

    @overload
    def __call__(self, username: str) -> Optional["User"]:
        """Get a user by username if exists. Otherwise, returns `None`"""
        ...

    @overload
    def __call__(self, id: Union[UUID, str]) -> Optional["User"]:
        """Get a user by id if exists. Otherwise, returns `None`"""
        ...

    def __call__(self, username: str = None, id: Union[str, UUID] = None) -> Optional["User"]:
        if not (username or id):
            raise ArgillaError("One of 'username' or 'id' must be provided")
        if username and id:
            warnings.warn("Only one of 'username' or 'id' must be provided. Using 'id'")
            username = None

        if id is not None:
            model = _get_model_by_id(self._api, id)
            if model:
                return self._from_model(model)  # noqa
            warnings.warn(f"User with id {id!r} not found.")
        else:
            for model in self._api.list():
                if model.username == username:
                    return self._from_model(model)
            warnings.warn(f"User with username {username!r} not found.")

    def __iter__(self):
        return self._Iterator(self.list())

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "User": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["User"]: ...

    def __getitem__(self, index):
        model = self._api.list()[index]
        return self._from_model(model)

    def __len__(self) -> int:
        return len(self._api.list())

    def add(self, user: "User") -> "User":
        """Add a new user to Argilla.

        Args:
            user: User object.

        Returns:
            User: The created user.
        """
        user._client = self._client
        return user.create()

    @overload
    def list(self) -> List["User"]: ...

    @overload
    def list(self, workspace: "Workspace") -> List["User"]: ...

    def list(self, workspace: Optional["Workspace"] = None) -> List["User"]:
        """List all users."""
        if workspace is not None:
            models = self._api.list_by_workspace_id(workspace.id)
        else:
            models = self._api.list()

        return [self._from_model(model) for model in models]

    ############################
    # Private methods
    ############################

    def _repr_html_(self) -> str:
        return self._represent_as_html(resources=self.list())

    def _from_model(self, model: UserModel) -> "User":
        from argilla.users import User

        return User(client=self._client, _model=model)


class Workspaces(Sequence["Workspace"], ResourceHTMLReprMixin):
    """A collection of workspaces. It can be used to create a new workspace or to get an existing one."""

    class _Iterator(GenericIterator["Workspace"]):
        pass

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = client.api.workspaces

    @overload
    def __call__(self, name: str) -> Optional["Workspace"]:
        """Get a workspace by name if exists. Otherwise, returns `None`"""
        ...

    @overload
    def __call__(self, id: Union[UUID, str]) -> Optional["Workspace"]:
        """Get a workspace by id if exists. Otherwise, returns `None`"""
        ...

    def __call__(self, name: str = None, id: Union[UUID, str] = None) -> Optional["Workspace"]:
        if not (name or id):
            raise ArgillaError("One of 'name' or 'id' must be provided")

        if name and id:
            warnings.warn("Only one of 'name' or 'id' must be provided. Using 'id'")
            name = None

        if id is not None:
            model = _get_model_by_id(self._api, id)
            if model:
                return self._from_model(model)  # noqa
            warnings.warn(f"Workspace with id {id!r} not found")
        else:
            for model in self._api.list():
                if model.name == name:
                    return self._from_model(model)  # noqa
            warnings.warn(f"Workspace with name {name!r} not found.")

    def __iter__(self):
        return self._Iterator(self.list())

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "Workspace": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["Workspace"]: ...

    def __getitem__(self, index) -> "Workspace":
        model = self._api.list()[index]
        return self._from_model(model)

    def __len__(self) -> int:
        return len(self._api.list())

    def add(self, workspace: "Workspace") -> "Workspace":
        """Add a new workspace to the Argilla platform.
        Args:
            workspace: Workspace object.

        Returns:
            Workspace: The created workspace.
        """
        workspace._client = self._client
        return workspace.create()

    def list(self) -> List["Workspace"]:
        return [self._from_model(model) for model in self._api.list()]

    ############################
    # Properties
    ############################

    @property
    def default(self) -> "Workspace":
        """The default workspace."""
        if len(self) == 0:
            raise ArgillaError("There are no workspaces created. Please create a new workspace first")
        return self[0]

    ############################
    # Private methods
    ############################

    def _repr_html_(self) -> str:
        return self._represent_as_html(resources=self.list())

    def _from_model(self, model: WorkspaceModel) -> "Workspace":
        from argilla.workspaces import Workspace

        return Workspace.from_model(client=self._client, model=model)


class Datasets(Sequence["Dataset"], ResourceHTMLReprMixin):
    """A collection of datasets. It can be used to create a new dataset or to get an existing one."""

    class _Iterator(GenericIterator["Dataset"]):
        def __next__(self):
            dataset = super().__next__()
            return dataset.get()

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = client.api.datasets

    @overload
    def __call__(self, name: str, workspace: Optional[Union["Workspace", str]] = None) -> Optional["Dataset"]:
        """Get a dataset by name and workspace if exists. Otherwise, returns `None`"""
        ...

    @overload
    def __call__(self, id: Union[UUID, str]) -> Optional["Dataset"]:
        """Get a dataset by id if exists. Otherwise, returns `None`"""
        ...

    @overload
    def __call__(self, workspace: Union["Workspace", str]) -> List["Dataset"]:
        """Get all datasets for a given workspace."""
        ...

    def __call__(
        self, name: str = None, workspace: Optional[Union["Workspace", str]] = None, id: Union[UUID, str] = None
    ) -> Union[Optional["Dataset"], List["Dataset"]]:
        """
        Get a dataset by name and workspace, by id, or all datasets for a workspace.
        """
        if id is not None and name is None and workspace is None:
            model = _get_model_by_id(self._api, id)
            if model:
                return self._from_model(model)
            warnings.warn(f"Dataset with id {id!r} not found")
            return None

        elif name is not None and id is None:
            workspace_obj = workspace or self._client.workspaces.default
            if isinstance(workspace_obj, str):
                workspace_obj = self._client.workspaces(workspace_obj)

            if workspace_obj is None:
                raise ArgillaError("Workspace not found. Please provide a valid workspace name or id.")

            for dataset in workspace_obj.datasets:
                if dataset.name == name:
                    return dataset.get()
            warnings.warn(f"Dataset with name {name!r} not found in workspace {workspace_obj.name!r}")
            return None

        elif name is None and id is None and workspace is not None:
            workspace_obj = workspace
            if isinstance(workspace_obj, str):
                workspace_obj = self._client.workspaces(workspace_obj)
            return list(workspace_obj.datasets)

        elif name is not None and id is not None:
            warnings.warn("Only one of 'name' or 'id' must be provided. Using 'id'")
            model = _get_model_by_id(self._api, id)
            if model:
                return self._from_model(model)
            warnings.warn(f"Dataset with id {id!r} not found")
            return None

        else:
            raise ArgillaError("One of 'name', 'id', or 'workspace' must be provided")

    def __iter__(self):
        return self._Iterator([self._from_model(model) for model in self._api.list()])

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "Dataset": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["Dataset"]: ...

    def __getitem__(self, index) -> "Dataset":
        model = self._api.list()[index]
        return self._from_model(model).get()

    def __len__(self) -> int:
        return len(self._api.list())

    def add(self, dataset: "Dataset") -> "Dataset":
        """
        Add a new dataset to the Argilla platform

        Args:
            dataset: Dataset object.

        Returns:
            Dataset: The created dataset.
        """
        dataset._client = self._client
        dataset.create()

        return dataset

    def list(self) -> List["Dataset"]:
        return list(self)

    ############################
    # Private methods
    ############################

    def _repr_html_(self) -> str:
        return self._represent_as_html(resources=self.list())

    def _from_model(self, model: DatasetModel) -> "Dataset":
        from argilla.datasets import Dataset

        return Dataset.from_model(model=model, client=self._client)


class Webhooks(Sequence["Webhook"], ResourceHTMLReprMixin):
    """A webhooks class. It can be used to create a new webhook or to get an existing one."""

    class _Iterator(GenericIterator["Webhook"]):
        pass

    def __init__(self, client: "Argilla") -> None:
        self._client = client
        self._api = client.api.webhooks

    def __call__(self, id: Union[UUID, str]) -> Optional["Webhook"]:
        """Get a webhook by id if exists. Otherwise, returns `None`"""

        model = _get_model_by_id(self._api, id)
        if model:
            return self._from_model(model)  # noqa
        warnings.warn(f"Webhook with id {id!r} not found")

    def __iter__(self):
        return self._Iterator(self.list())

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> "Webhook": ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence["Webhook"]: ...

    def __getitem__(self, index) -> "Webhook":
        model = self._api.list()[index]
        return self._from_model(model)

    def __len__(self) -> int:
        return len(self._api.list())

    def add(self, webhook: "Webhook") -> "Webhook":
        """Add a new webhook to the Argilla platform.
        Args:
            webhook: Webhook object.

        Returns:
            Webhook: The created webhook.
        """
        webhook._client = self._client
        return webhook.create()

    def list(self) -> List["Webhook"]:
        return [self._from_model(model) for model in self._api.list()]

    ############################
    # Private methods
    ############################

    def _repr_html_(self) -> str:
        return self._represent_as_html(resources=self.list())

    def _from_model(self, model: WebhookModel) -> "Webhook":
        from argilla.webhooks import Webhook

        return Webhook.from_model(client=self._client, model=model)


def _get_model_by_id(api: ResourceAPI, resource_id: Union[UUID, str]) -> Optional[ResourceModel]:
    """Get a resource model by id if found. Otherwise, `None`."""
    try:
        if not isinstance(resource_id, UUID):
            resource_id = UUID(resource_id)
        return api.get(resource_id)
    except NotFoundError:
        pass
