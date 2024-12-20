# Copyright 2024-present, Argilla, Inc.
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

from typing import List, Dict, TYPE_CHECKING, Optional, overload, Union, Sequence
from uuid import UUID

from argilla._api._workspaces import WorkspacesAPI
from argilla._helpers import GenericIterator
from argilla._helpers import LoggingMixin
from argilla._models import WorkspaceModel, DocumentModel
from argilla._resource import Resource
from argilla.client import Argilla

if TYPE_CHECKING:
    from argilla.datasets._resource import Dataset
    from argilla.users._resource import User


class Workspace(Resource):
    """Class for interacting with Argilla workspaces. Workspaces are used to organize datasets in the Argilla server.

    Attributes:
        name (str): The name of the workspace.
        id (UUID): The ID of the workspace. This is a unique identifier for the workspace in the server.
        datasets (List[Dataset]): A list of all datasets in the workspace.
        users (WorkspaceUsers): A list of all users in the workspace.
    """

    name: Optional[str]

    _api: "WorkspacesAPI"

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[UUID] = None,
        client: Optional["Argilla"] = None,
    ) -> None:
        """Initializes a Workspace object with a client and a name or id

        Parameters:
            client (Argilla): The client used to interact with Argilla
            name (str): The name of the workspace
            id (UUID): The id of the workspace

        Returns:
            Workspace: The initialized workspace object
        """
        client = client or Argilla._get_default()
        super().__init__(client=client, api=client.api.workspaces)

        self._model = WorkspaceModel(name=name, id=id)

    def add_user(self, user: Union["User", str]) -> "User":
        """Adds a user to the workspace. After adding a user to the workspace, it will have access to the datasets
        in the workspace.

        Args:
            user (Union[User, str]): The user to add to the workspace. Can be a User object or a username.

        Returns:
            User: The user that was added to the workspace
        """
        return self.users.add(user)

    def remove_user(self, user: Union["User", str]) -> "User":
        """Removes a user from the workspace. After removing a user from the workspace, it will no longer have access

        Args:
            user (Union[User, str]): The user to remove from the workspace. Can be a User object or a username.

        Returns:
            User: The user that was removed from the workspace.
        """
        return self.users.delete(user)

    # TODO: Make this method private
    def list_datasets(self) -> List["Dataset"]:
        from argilla.datasets import Dataset

        datasets = self._client.api.datasets.list(self.id)
        self._log_message(f"Got {len(datasets)} datasets for workspace {self.id}")
        return [Dataset.from_model(model=dataset, client=self._client) for dataset in datasets]

    @classmethod
    def from_model(cls, model: WorkspaceModel, client: Argilla) -> "Workspace":
        instance = cls(name=model.name, id=model.id, client=client)
        instance._model = model

        return instance

    ############################
    # Properties
    ############################

    @property
    def name(self) -> Optional[str]:
        return self._model.name

    @name.setter
    def name(self, value: str) -> None:
        self._model.name = value

    @property
    def datasets(self) -> List["Dataset"]:
        """List all datasets in the workspace

        Returns:
            List[Dataset]: A list of all datasets in the workspace
        """
        return self.list_datasets()

    @property
    def users(self) -> "WorkspaceUsers":
        """List all users in the workspace

        Returns:
            WorkspaceUsers: A list of all users in the workspace
        """
        return WorkspaceUsers(workspace=self)

    @property
    def documents(self) -> "WorkspaceDocuments":
        """List all documents in the workspace

        Returns:
            WorkspaceDocuments: Interface to manage documents in the workspace
        """
        return WorkspaceDocuments(workspace=self)

    ############################
    # Private methods
    ############################


class WorkspaceUsers(Sequence["User"], LoggingMixin):
    class _Iterator(GenericIterator["User"]):
        pass

    def __init__(self, workspace: "Workspace") -> None:
        self._workspace = workspace

    @overload
    def add(self, user: "User") -> "User": ...

    @overload
    def add(self, user: str) -> "User": ...

    def add(self, user: Union["User", str]) -> "User":
        if isinstance(user, str):
            return self._add_user_by_username(username=user)
        return user.add_to_workspace(workspace=self._workspace)

    @overload
    def delete(self, user: "User") -> "User": ...

    @overload
    def delete(self, user: str) -> "User": ...

    def delete(self, user: Union["User", str]) -> "User":
        if isinstance(user, str):
            return self._delete_user_by_username(username=user)
        return user.remove_from_workspace(workspace=self._workspace)

    def __iter__(self):
        return self._Iterator(self._list_users())

    def __getitem__(self, index: int) -> "User":
        return self._list_users()[index]

    def __len__(self) -> int:
        return len(self._list_users())

    ####################
    # Private methods
    ####################

    def _list_users(self) -> List["User"]:
        users = self._workspace._client.users.list(workspace=self._workspace)
        self._log_message(f"Got {len(users)} users for workspace {self._workspace.id}")
        return users

    def _delete_user_by_username(self, username: str) -> "User":
        user = self._workspace._client.users(username=username)
        if user is None:
            raise ValueError(f"User {username} does not exist")
        return user.remove_from_workspace(workspace=self._workspace)

    def _add_user_by_username(self, username: str) -> "User":
        user = self._workspace._client.users(username=username)
        if user is None:
            raise ValueError(f"User {username} does not exist")
        return user.add_to_workspace(workspace=self._workspace)

class WorkspaceDocuments(LoggingMixin):
    """Interface for managing documents in a workspace."""

    def __init__(self, workspace: "Workspace") -> None:
        self._workspace = workspace

    def add(self, file_path: str, reference: Optional[str] = None,
            pmid: Optional[str] = None, doi: Optional[str] = None, id: Optional[UUID]= None) -> "DocumentModel":
        """Add a document to the workspace.

        Args:
            file_path: Path to a local PDF file or an URL
            reference: Reference text for the document
            pmid: PubMed ID if applicable
            doi: DOI if applicable

        Returns:
            DocumentModel: The created document
        """
        doc = DocumentModel.from_file(
            str(file_path),
            reference=reference,
            pmid=pmid,
            doi=doi,
            workspace_id=self._workspace.id,
            id=id
        )

        created_doc = self._workspace._client.api.documents.create(doc)
        self._log_message(f"Added document {created_doc.file_name} to workspace {self._workspace.name}")
        return created_doc

    def get(self, document_id: Union[str, UUID]) -> Optional["DocumentModel"]:
        """Get a document by ID.

        Args:
            document_id: ID of the document to retrieve

        Returns:
            DocumentModel or None: The document if found
        """
        docs = self.list()
        for doc in docs:
            if str(doc.id) == str(document_id):
                return doc
        return None

    def delete(self, document: Union["DocumentModel", str, UUID]) -> None:
        """Delete a document from the workspace.

        Args:
            document: Document, document ID or document UUID to delete
        """
        if isinstance(document, (str, UUID)):
            doc_id = document
        else:
            doc_id = document.id

        self._workspace._client.api.documents.delete(document_id=UUID(str(doc_id)))
        self._log_message(f"Deleted document {doc_id} from workspace {self._workspace.name}")

    def list(self) -> List["DocumentModel"]:
        """List all documents in the workspace.

        Returns:
            List[DocumentModel]: List of documents in the workspace
        """
        docs = self._workspace._client.api.documents.list(workspace_id=self._workspace.id)
        self._log_message(f"Got {len(docs)} documents for workspace {self._workspace.name}")
        return docs
