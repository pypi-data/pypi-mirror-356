"""Completion Models."""

from __future__ import annotations

import copy
import datetime
from collections.abc import Iterable, Sequence
from typing import Literal, TypeAlias

from corvic import eorm, system, transfer
from corvic.emodel._base_model import OrgWideStandardModel
from corvic.emodel._proto_orm_convert import (
    completion_model_delete_orms,
    completion_model_orm_to_proto,
    completion_model_proto_to_orm,
)
from corvic.result import InvalidArgumentError, NotFoundError, Ok
from corvic_generated.model.v1alpha import models_pb2
from corvic_generated.orm.v1 import completion_model_pb2

CompletionModelID: TypeAlias = eorm.CompletionModelID
OrgID: TypeAlias = eorm.OrgID


class CompletionModel(
    OrgWideStandardModel[
        CompletionModelID, models_pb2.CompletionModel, eorm.CompletionModel
    ],
):
    """Completion Models."""

    @classmethod
    def orm_class(cls):
        return eorm.CompletionModel

    @classmethod
    def id_class(cls):
        return CompletionModelID

    @classmethod
    def orm_to_proto(cls, orm_obj: eorm.CompletionModel) -> models_pb2.CompletionModel:
        return completion_model_orm_to_proto(orm_obj)

    @classmethod
    def proto_to_orm(
        cls, proto_obj: models_pb2.CompletionModel, session: eorm.Session
    ) -> Ok[eorm.CompletionModel] | InvalidArgumentError:
        return completion_model_proto_to_orm(proto_obj, session)

    @classmethod
    def delete_by_ids(
        cls, ids: Sequence[CompletionModelID], session: eorm.Session
    ) -> Ok[None] | InvalidArgumentError:
        return completion_model_delete_orms(ids, session)

    @property
    def name(self) -> str:
        return self.proto_self.name

    @property
    def provider(self) -> Literal["openai-generic", "azure-openai"] | None:
        match self.proto_self.parameters.WhichOneof("params"):
            case "azure_openai_parameters":
                return "azure-openai"
            case "generic_openai_parameters":
                return "openai-generic"
            case _:
                return None

    @property
    def parameters(
        self,
    ) -> (
        completion_model_pb2.AzureOpenAIParameters
        | completion_model_pb2.GenericOpenAIParameters
        | None
    ):
        match self.provider:
            case "azure-openai":
                return self.azure_openai_parameters
            case "openai-generic":
                return self.generic_openai_parameters
            case None:
                return None

    @property
    def azure_openai_parameters(
        self,
    ) -> completion_model_pb2.AzureOpenAIParameters | None:
        if self.proto_self.parameters.HasField("azure_openai_parameters"):
            return self.proto_self.parameters.azure_openai_parameters
        return None

    @property
    def generic_openai_parameters(
        self,
    ) -> completion_model_pb2.GenericOpenAIParameters | None:
        if self.proto_self.parameters.HasField("generic_openai_parameters"):
            return self.proto_self.parameters.generic_openai_parameters
        return None

    @property
    def secret_api_key(self) -> str:
        return self.proto_self.secret_api_key

    @property
    def description(self) -> str:
        return self.proto_self.description

    @property
    def last_validation_time(self) -> datetime.datetime | None:
        return transfer.non_empty_timestamp_to_datetime(
            self.proto_self.last_validation_time
        )

    @property
    def last_successful_validation(self) -> datetime.datetime | None:
        return transfer.non_empty_timestamp_to_datetime(
            self.proto_self.last_successful_validation
        )

    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str,
        parameters: completion_model_pb2.CompletionModelParameters,
        secret_api_key: str,
        client: system.Client,
    ):
        return cls(
            proto_self=models_pb2.CompletionModel(
                name=name,
                description=description,
                parameters=parameters,
                secret_api_key=secret_api_key,
            ),
            client=client,
        )

    @classmethod
    def list(
        cls,
        *,
        limit: int | None = None,
        created_before: datetime.datetime | None = None,
        ids: Iterable[CompletionModelID] | None = None,
        existing_session: eorm.Session | None = None,
        client: system.Client,
    ) -> Ok[list[CompletionModel]] | NotFoundError | InvalidArgumentError:
        """List completion models."""
        match cls.list_as_proto(
            limit=limit,
            created_before=created_before,
            ids=ids,
            existing_session=existing_session,
            client=client,
        ):
            case NotFoundError() | InvalidArgumentError() as err:
                return err
            case Ok(protos):
                return Ok(
                    [
                        cls.from_proto(
                            proto=proto,
                            client=client,
                        )
                        for proto in protos
                    ]
                )

    @classmethod
    def from_proto(
        cls,
        *,
        proto: models_pb2.CompletionModel,
        client: system.Client,
    ) -> CompletionModel:
        return cls(
            proto_self=proto,
            client=client,
        )

    @classmethod
    def from_id(
        cls,
        *,
        completion_model_id: CompletionModelID,
        session: eorm.Session | None = None,
        client: system.Client,
    ) -> Ok[CompletionModel] | NotFoundError:
        return cls.load_proto_for(
            obj_id=completion_model_id,
            client=client,
            existing_session=session,
        ).map(
            lambda proto_self: cls.from_proto(
                proto=proto_self,
                client=client,
            )
        )

    def with_name(self, name: str) -> CompletionModel:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.name = name
        return CompletionModel(
            proto_self=proto_self,
            client=self.client,
        )

    def with_description(self, description: str) -> CompletionModel:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.description = description
        return CompletionModel(
            proto_self=proto_self,
            client=self.client,
        )

    def with_parameters(
        self, parameters: completion_model_pb2.CompletionModelParameters
    ) -> CompletionModel:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.parameters.CopyFrom(parameters)
        return CompletionModel(
            proto_self=proto_self,
            client=self.client,
        )

    def with_secret_api_key(self, secret_api_key: str) -> CompletionModel:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.secret_api_key = secret_api_key
        return CompletionModel(
            proto_self=proto_self,
            client=self.client,
        )

    def with_last_validation_time(
        self, last_validation_time: datetime.datetime
    ) -> CompletionModel:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.last_validation_time.FromDatetime(last_validation_time)
        return CompletionModel(
            proto_self=proto_self,
            client=self.client,
        )

    def with_last_successful_validation(
        self, last_successful_validation: datetime.datetime
    ) -> CompletionModel:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.last_successful_validation.FromDatetime(last_successful_validation)
        return CompletionModel(
            proto_self=proto_self,
            client=self.client,
        )
