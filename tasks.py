"""Celery tasks for running the map editor phases."""

import os
from typing import Optional

from celery.utils.log import get_task_logger

from celery_app import celery_app
from main import phase_2

LOGGER = get_task_logger(__name__)


def _resolve_turn(turn: Optional[int]) -> int:
    """Return the turn number to run the phase 2 calculations for."""
    if turn is not None:
        try:
            return int(turn)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid turn value provided: {turn!r}") from exc

    env_value = os.getenv("PHASE_2_TURN")
    if env_value is None:
        raise RuntimeError(
            "PHASE_2_TURN environment variable is not set and no turn argument was provided."
        )

    try:
        return int(env_value)
    except ValueError as exc:  # pragma: no cover - defensive, hard to trigger in tests
        raise ValueError(
            f"Unable to convert PHASE_2_TURN value {env_value!r} to an integer."
        ) from exc


@celery_app.task(name="tasks.execute_phase_2")
def execute_phase_2(turn: Optional[int] = None) -> dict:
    """Execute the second processing phase, producing the updated political maps."""
    resolved_turn = _resolve_turn(turn)
    LOGGER.info("Starting phase 2 calculations for turn %s", resolved_turn)
    phase_2(resolved_turn)
    LOGGER.info("Completed phase 2 calculations for turn %s", resolved_turn)
    return {"turn": resolved_turn}

