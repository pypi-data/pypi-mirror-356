from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptRequest")


@_attrs_define
class PromptRequest:
    """Serializer for the Prompt model.

    Attributes:
        name (str):
        prompt_text (str):
        organization (UUID):
        category (Union[Unset, str]): Primary category for grouping prompts (e.g., Evasion, Harmful Content).
        tags (Union[Unset, Any]): Optional JSON list of tags for classification (e.g., ["PII", "Malware"])
        evaluation_criteria (Union[Unset, str]): Description of how success/failure should be judged for this specific
            prompt.
        expected_tool_calls (Union[Unset, Any]): JSON list of expected tool calls, e.g., [{"tool_name": "...",
            "tool_input": {...}}]
        expected_output_pattern (Union[Unset, str]): Optional regex pattern to match against the final response.
        reference_output (Union[Unset, str]): Optional ideal/reference final output text.
        owner (Union[None, Unset, int]):
    """

    name: str
    prompt_text: str
    organization: UUID
    category: Union[Unset, str] = UNSET
    tags: Union[Unset, Any] = UNSET
    evaluation_criteria: Union[Unset, str] = UNSET
    expected_tool_calls: Union[Unset, Any] = UNSET
    expected_output_pattern: Union[Unset, str] = UNSET
    reference_output: Union[Unset, str] = UNSET
    owner: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        prompt_text = self.prompt_text

        organization = str(self.organization)

        category = self.category

        tags = self.tags

        evaluation_criteria = self.evaluation_criteria

        expected_tool_calls = self.expected_tool_calls

        expected_output_pattern = self.expected_output_pattern

        reference_output = self.reference_output

        owner: Union[None, Unset, int]
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "prompt_text": prompt_text,
                "organization": organization,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category
        if tags is not UNSET:
            field_dict["tags"] = tags
        if evaluation_criteria is not UNSET:
            field_dict["evaluation_criteria"] = evaluation_criteria
        if expected_tool_calls is not UNSET:
            field_dict["expected_tool_calls"] = expected_tool_calls
        if expected_output_pattern is not UNSET:
            field_dict["expected_output_pattern"] = expected_output_pattern
        if reference_output is not UNSET:
            field_dict["reference_output"] = reference_output
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        prompt_text = d.pop("prompt_text")

        organization = UUID(d.pop("organization"))

        category = d.pop("category", UNSET)

        tags = d.pop("tags", UNSET)

        evaluation_criteria = d.pop("evaluation_criteria", UNSET)

        expected_tool_calls = d.pop("expected_tool_calls", UNSET)

        expected_output_pattern = d.pop("expected_output_pattern", UNSET)

        reference_output = d.pop("reference_output", UNSET)

        def _parse_owner(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        owner = _parse_owner(d.pop("owner", UNSET))

        prompt_request = cls(
            name=name,
            prompt_text=prompt_text,
            organization=organization,
            category=category,
            tags=tags,
            evaluation_criteria=evaluation_criteria,
            expected_tool_calls=expected_tool_calls,
            expected_output_pattern=expected_output_pattern,
            reference_output=reference_output,
            owner=owner,
        )

        prompt_request.additional_properties = d
        return prompt_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
