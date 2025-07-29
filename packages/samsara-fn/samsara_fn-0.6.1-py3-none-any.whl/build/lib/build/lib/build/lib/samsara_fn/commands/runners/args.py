from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class RunArgs:
    """Arguments for run command."""

    run_command: Literal["manual", "alertAction", "schedule"]
    func_name: str
    parametersOverride: Optional[str] = None
    alertPayload: Optional[str] = None
