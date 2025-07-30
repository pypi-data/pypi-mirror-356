"""Dataclasses and functionality for task request details/messages."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
import typing
from typing import Optional, TypeVar

import msgpack

from bitfount import config
from bitfount.federated.types import SerializedProtocol
from bitfount.types import _JSONDict

T = TypeVar("T", bound="_DataclassSerializerMixin")


@dataclass
class _DataclassSerializerMixin:
    """MixIn class for dataclasses that enable easy `msgpack` (de)serialization."""

    def to_dict(self) -> _JSONDict:
        """Returns dataclass as a dictionary."""
        # remove key,value pair if value is None
        return dataclasses.asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )

    @classmethod
    def from_dict(cls: type[T], d: _JSONDict) -> T:
        """Creates dataclass from dictionary."""
        # Extract the types of instance fields for this dataclass
        field_types = typing.get_type_hints(cls)
        field_types = {
            k: v
            for k, v in field_types.items()
            if k in {f.name for f in dataclasses.fields(cls)}
        }

        # Create sub-dataclasses if needed
        for name, klass in field_types.items():
            if hasattr(klass, "from_dict"):
                d[name] = klass.from_dict(d[name])

        return cls(**d)

    def serialize(self) -> bytes:
        """Serializes dataclass to bytes."""
        return msgpack.dumps(self.to_dict())

    @classmethod
    def deserialize(cls: type[T], data: bytes) -> T:
        """Deserializes dataclass from bytes."""
        return cls.from_dict(msgpack.loads(data))


@dataclass
class _TaskRequest(_DataclassSerializerMixin):
    """The full task request to be sent to the pod."""

    serialized_protocol: SerializedProtocol
    pod_identifiers: list[str]
    aes_key: bytes


@dataclass
class _EncryptedTaskRequest(_DataclassSerializerMixin):
    """Encrypted task request."""

    encrypted_request: bytes


@dataclass
class _SignedEncryptedTaskRequest(_DataclassSerializerMixin):
    """Encrypted and signed task request."""

    encrypted_request: bytes
    signature: bytes


@dataclass
class _TaskRequestMessage(_DataclassSerializerMixin):
    """Task request message to be sent to pod."""

    serialized_protocol: SerializedProtocol
    auth_type: str
    request: bytes
    project_id: Optional[str] = None
    run_on_new_data_only: bool = False
    batched_execution: Optional[bool] = None
    key_id: Optional[str] = None
    test_run: bool = False

    def __post_init__(self) -> None:
        if self.batched_execution is None:
            self.batched_execution = config.settings.default_batched_execution
