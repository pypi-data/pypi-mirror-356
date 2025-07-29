from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional


class TaskModel(BaseModel):
    name: str
    task: str
    params: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[str] = Field(default_factory=list)

    # How many times to retry if task raises (default: 0 = no retries)
    retries: int = Field(default=0, ge=0)

    # Seconds ot wait between retries (default: 0 = no delay)
    retry_delay: float = Field(default=0.0, ge=0.0)

    # Max seconds to wait for this task to complete (0 or None = no timeout)
    timeout: Optional[float] = Field(default=None, ge=0.0)

    # If True, pipeline continues even if this task ultimately fails
    ignore_failure: bool = Field(default=False)

    # Jinja2 expression controlling whether to run this task
    run_if: Optional[str] = Field(default=None)

    # Jinja2 expression controlling whether "not" to run this task
    run_unless: Optional[str] = Field(default=None)

    # If this task fails, all tasks depending on it will be skipped
    skip_downstream_on_failure: bool = Field(default=False)

    # Per-task environment variables (templates rendered against context)
    env: Dict[str, Any] = Field(default_factory=dict)

    # New resource-limits
    cpu_time: Optional[int] = Field(
        default=None,
        ge=1,
        description="Maximum CPU-seconds for this task (UNIX only)."
    )
    memory: Optional[int] = Field(
        default=None,
        ge=1,
        description="Maximum address-space (bytes) for this task (UNIX only)."
    )

    # Group name for resource-based throttling
    resource_tag: Optional[str] = Field(default=None)

    # Max simultaneous tasks with the same resource_tag
    max_concurrency: Optional[int] = Field(default=None, ge=1)

    # Optional branch name this task belongs to
    branch: Optional[str] = Field(
        default=None,
        description="If set, this task runs only when pipeline.branches[branch] evaluated true",
    )

    # ---- Rate-limiting ----
    rate_limit: Optional[float] = Field(
        default=None, ge=0.0,
        description="Maximum number of calls per second."
    )
    rate_limit_key: Optional[str] = Field(
        default=None,
        description="Grouping key for shared rate limiting (defaults to task name)."
    )

    class Config:
        # Accept the alias key in input
        allow_population_by_field_name = True
        allow_population_by_alias = True


class Pipeline(BaseModel):
    # named branch conditions
    branches: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapping branch-name → Jinja2 expression controlling that branch"
    )
    tasks: List[TaskModel]

    @field_validator('tasks', mode='before')
    def check_tasks_not_empty(cls, v):
        if not v:
            raise ValueError("Pipeline must contain at least one task")
        return v

    @field_validator('tasks')
    def validate_branch_names(cls, tasks, info):
        branch_defs = info.data.get("branches", {})
        for t in tasks:
            if t.branch and t.branch not in branch_defs:
                raise ValueError(f"Task '{t.name}' references undefined branch '{t.branch}'")
        return tasks
