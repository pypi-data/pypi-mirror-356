from __future__ import annotations

from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    Iterator,
    List,
    Optional,
    Sequence,
    TypeVar,
    Dict,
    Type,
)
from pydantic import BaseModel, Field, ConfigDict
from .agent_protocol import AsyncAgentProtocol
from .plugins import ValidationPlugin


StepInT = TypeVar("StepInT")
StepOutT = TypeVar("StepOutT")
NewOutT = TypeVar("NewOutT")


# BranchKey type alias for ConditionalStep
BranchKey = Any


class StepConfig(BaseModel):
    """Configuration options for a pipeline step."""

    max_retries: int = 1
    timeout_s: float | None = None


class Step(BaseModel, Generic[StepInT, StepOutT]):
    """Represents a single step in a pipeline."""

    name: str
    agent: Any | None = Field(default=None)
    config: StepConfig = Field(default_factory=StepConfig)
    plugins: List[tuple[ValidationPlugin, int]] = Field(default_factory=list)
    failure_handlers: List[Callable[[], None]] = Field(default_factory=list)

    model_config: ClassVar[ConfigDict] = {
        "arbitrary_types_allowed": True,
    }

    def __init__(
        self,
        name: str,
        agent: Optional[AsyncAgentProtocol[StepInT, StepOutT]] = None,
        plugins: Optional[List[ValidationPlugin | tuple[ValidationPlugin, int]]] = None,
        on_failure: Optional[List[Callable[[], None]]] = None,
        **config: Any,
    ) -> None:
        plugin_list: List[tuple[ValidationPlugin, int]] = []
        if plugins:
            for p in plugins:
                if isinstance(p, tuple):
                    plugin_list.append(p)
                else:
                    plugin_list.append((p, 0))

        super().__init__(
            name=name,
            agent=agent,
            config=StepConfig(**config),
            plugins=plugin_list,
            failure_handlers=on_failure or [],
        )

    def __rshift__(
        self, other: "Step[StepOutT, NewOutT]" | "Pipeline[StepOutT, NewOutT]"
    ) -> "Pipeline[StepInT, NewOutT]":
        if isinstance(other, Step):
            return Pipeline.from_step(self) >> other
        if isinstance(other, Pipeline):
            return Pipeline.from_step(self) >> other
        raise TypeError("Can only chain Step with Step or Pipeline")

    @classmethod
    def review(cls, agent: AsyncAgentProtocol[Any, Any], **config: Any) -> "Step[Any, Any]":
        """Construct a review step using the provided agent."""
        return cls("review", agent, **config)

    @classmethod
    def solution(cls, agent: AsyncAgentProtocol[Any, Any], **config: Any) -> "Step[Any, Any]":
        """Construct a solution step using the provided agent."""
        return cls("solution", agent, **config)

    @classmethod
    def validate_step(cls, agent: AsyncAgentProtocol[Any, Any], **config: Any) -> "Step[Any, Any]":
        """Construct a validation step using the provided agent."""
        return cls("validate", agent, **config)

    @classmethod
    def human_in_the_loop(
        cls,
        name: str,
        message_for_user: str | None = None,
        input_schema: Type[BaseModel] | None = None,
    ) -> "HumanInTheLoopStep":
        """Create a step that pauses execution for human input."""
        return HumanInTheLoopStep(
            name=name,
            message_for_user=message_for_user,
            input_schema=input_schema,
        )

    def add_plugin(self, plugin: ValidationPlugin, priority: int = 0) -> "Step[StepInT, StepOutT]":
        """Add a validation plugin to this step."""
        self.plugins.append((plugin, priority))
        return self

    def on_failure(self, handler: Callable[[], None]) -> "Step[StepInT, StepOutT]":
        """Add a failure handler to this step."""
        self.failure_handlers.append(handler)
        return self

    @classmethod
    def loop_until(
        cls,
        name: str,
        loop_body_pipeline: "Pipeline[Any, Any]",
        exit_condition_callable: Callable[[Any, Optional[BaseModel]], bool],
        max_loops: int = 5,
        initial_input_to_loop_body_mapper: Optional[
            Callable[[Any, Optional[BaseModel]], Any]
        ] = None,
        iteration_input_mapper: Optional[Callable[[Any, Optional[BaseModel], int], Any]] = None,
        loop_output_mapper: Optional[Callable[[Any, Optional[BaseModel]], Any]] = None,
        **config_kwargs: Any,
    ) -> "LoopStep":
        """Factory method to create a :class:`LoopStep`."""
        from .pipeline_dsl import LoopStep

        return LoopStep(
            name=name,
            loop_body_pipeline=loop_body_pipeline,
            exit_condition_callable=exit_condition_callable,
            max_loops=max_loops,
            initial_input_to_loop_body_mapper=initial_input_to_loop_body_mapper,
            iteration_input_mapper=iteration_input_mapper,
            loop_output_mapper=loop_output_mapper,
            **config_kwargs,
        )

    @classmethod
    def branch_on(
        cls,
        name: str,
        condition_callable: Callable[[Any, Optional[BaseModel]], BranchKey],
        branches: Dict[BranchKey, "Pipeline[Any, Any]"],
        default_branch_pipeline: Optional["Pipeline[Any, Any]"] = None,
        branch_input_mapper: Optional[Callable[[Any, Optional[BaseModel]], Any]] = None,
        branch_output_mapper: Optional[Callable[[Any, BranchKey, Optional[BaseModel]], Any]] = None,
        **config_kwargs: Any,
    ) -> "ConditionalStep":
        """Factory method to create a :class:`ConditionalStep`."""
        from .pipeline_dsl import ConditionalStep

        return ConditionalStep(
            name=name,
            condition_callable=condition_callable,
            branches=branches,
            default_branch_pipeline=default_branch_pipeline,
            branch_input_mapper=branch_input_mapper,
            branch_output_mapper=branch_output_mapper,
            **config_kwargs,
        )


class HumanInTheLoopStep(Step[Any, Any]):
    """A step that pauses the pipeline for human input."""

    message_for_user: str | None = Field(default=None)
    input_schema: Type[BaseModel] | None = Field(default=None)

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        *,
        name: str,
        message_for_user: str | None = None,
        input_schema: Type[BaseModel] | None = None,
        **config: Any,
    ) -> None:
        super().__init__(
            name=name,
            agent=None,
            config=StepConfig(**config),
            plugins=[],
            failure_handlers=[],
        )
        object.__setattr__(self, "message_for_user", message_for_user)
        object.__setattr__(self, "input_schema", input_schema)


class LoopStep(Step[Any, Any]):
    """A specialized step that executes a pipeline in a loop."""

    loop_body_pipeline: "Pipeline[Any, Any]" = Field(
        description="The pipeline to execute in each iteration."
    )
    exit_condition_callable: Callable[[Any, Optional[BaseModel]], bool] = Field(
        description=(
            "Callable that takes (last_body_output, pipeline_context) and returns True to exit loop."
        )
    )
    max_loops: int = Field(default=5, gt=0, description="Maximum number of iterations.")

    initial_input_to_loop_body_mapper: Optional[Callable[[Any, Optional[BaseModel]], Any]] = Field(
        default=None,
        description=("Callable to map LoopStep's input to the first iteration's body input."),
    )
    iteration_input_mapper: Optional[Callable[[Any, Optional[BaseModel], int], Any]] = Field(
        default=None,
        description=("Callable to map previous iteration's body output to next iteration's input."),
    )
    loop_output_mapper: Optional[Callable[[Any, Optional[BaseModel]], Any]] = Field(
        default=None,
        description=("Callable to map the final successful output to the LoopStep's output."),
    )

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        *,
        name: str,
        loop_body_pipeline: "Pipeline[Any, Any]",
        exit_condition_callable: Callable[[Any, Optional[BaseModel]], bool],
        max_loops: int = 5,
        initial_input_to_loop_body_mapper: Optional[
            Callable[[Any, Optional[BaseModel]], Any]
        ] = None,
        iteration_input_mapper: Optional[Callable[[Any, Optional[BaseModel], int], Any]] = None,
        loop_output_mapper: Optional[Callable[[Any, Optional[BaseModel]], Any]] = None,
        **config_kwargs: Any,
    ) -> None:
        if max_loops <= 0:
            raise ValueError("max_loops must be a positive integer.")

        BaseModel.__init__(
            self,
            name=name,
            agent=None,
            config=StepConfig(**config_kwargs),
            plugins=[],
            failure_handlers=[],
            loop_body_pipeline=loop_body_pipeline,
            exit_condition_callable=exit_condition_callable,
            max_loops=max_loops,
            initial_input_to_loop_body_mapper=initial_input_to_loop_body_mapper,
            iteration_input_mapper=iteration_input_mapper,
            loop_output_mapper=loop_output_mapper,
        )


class ConditionalStep(Step[Any, Any]):
    """A step that selects and executes a branch pipeline based on a condition."""

    condition_callable: Callable[[Any, Optional[BaseModel]], BranchKey] = Field(
        description=("Callable that returns a key to select a branch.")
    )
    branches: Dict[BranchKey, "Pipeline[Any, Any]"] = Field(
        description="Mapping of branch keys to sub-pipelines."
    )
    default_branch_pipeline: Optional["Pipeline[Any, Any]"] = Field(
        default=None,
        description="Pipeline to execute when no branch key matches.",
    )

    branch_input_mapper: Optional[Callable[[Any, Optional[BaseModel]], Any]] = Field(
        default=None,
        description="Maps ConditionalStep input to branch input.",
    )
    branch_output_mapper: Optional[Callable[[Any, BranchKey, Optional[BaseModel]], Any]] = Field(
        default=None,
        description="Maps branch output to ConditionalStep output.",
    )

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        *,
        name: str,
        condition_callable: Callable[[Any, Optional[BaseModel]], BranchKey],
        branches: Dict[BranchKey, "Pipeline[Any, Any]"],
        default_branch_pipeline: Optional["Pipeline[Any, Any]"] = None,
        branch_input_mapper: Optional[Callable[[Any, Optional[BaseModel]], Any]] = None,
        branch_output_mapper: Optional[Callable[[Any, BranchKey, Optional[BaseModel]], Any]] = None,
        **config_kwargs: Any,
    ) -> None:
        if not branches:
            raise ValueError("'branches' dictionary cannot be empty.")

        BaseModel.__init__(
            self,
            name=name,
            agent=None,
            config=StepConfig(**config_kwargs),
            plugins=[],
            failure_handlers=[],
            condition_callable=condition_callable,
            branches=branches,
            default_branch_pipeline=default_branch_pipeline,
            branch_input_mapper=branch_input_mapper,
            branch_output_mapper=branch_output_mapper,
        )


PipeInT = TypeVar("PipeInT")
PipeOutT = TypeVar("PipeOutT")
NewPipeOutT = TypeVar("NewPipeOutT")


class Pipeline(BaseModel, Generic[PipeInT, PipeOutT]):
    """A sequential pipeline of steps."""

    steps: Sequence[Step[Any, Any]]

    model_config: ClassVar[ConfigDict] = {
        "arbitrary_types_allowed": True,
    }

    @classmethod
    def from_step(cls, step: Step[PipeInT, PipeOutT]) -> "Pipeline[PipeInT, PipeOutT]":
        return cls.model_construct(steps=[step])

    def __rshift__(
        self, other: Step[PipeOutT, NewPipeOutT] | "Pipeline[PipeOutT, NewPipeOutT]"
    ) -> "Pipeline[PipeInT, NewPipeOutT]":
        if isinstance(other, Step):
            new_steps = list(self.steps) + [other]
            return Pipeline[PipeInT, NewPipeOutT](steps=new_steps)
        if isinstance(other, Pipeline):
            new_steps = list(self.steps) + list(other.steps)
            return Pipeline[PipeInT, NewPipeOutT](steps=new_steps)
        raise TypeError("Can only chain Pipeline with Step or Pipeline")

    def iter_steps(self) -> Iterator[Step[Any, Any]]:
        return iter(self.steps)


# Explicit exports
__all__ = [
    "Step",
    "Pipeline",
    "StepConfig",
    "LoopStep",
    "ConditionalStep",
    "HumanInTheLoopStep",
    "BranchKey",
]
