"""Celery application configuration for Entropic Heavens map processing."""

import logging
import os
from datetime import timedelta

from celery import Celery

LOGGER = logging.getLogger(__name__)


def _phase_2_interval() -> timedelta:
    """Return the configured scheduling interval for the phase 2 task."""
    default_minutes = 60.0
    raw_value = os.getenv("PHASE_2_INTERVAL_MINUTES")
    if raw_value is None:
        return timedelta(minutes=default_minutes)

    try:
        minutes = float(raw_value)
        if minutes <= 0:
            raise ValueError
    except ValueError:
        LOGGER.warning(
            "Invalid PHASE_2_INTERVAL_MINUTES value %r. Falling back to %s minutes.",
            raw_value,
            default_minutes,
        )
        minutes = default_minutes

    return timedelta(minutes=minutes)


celery_app = Celery("enthropic_heavens")
celery_app.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
celery_app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
celery_app.conf.timezone = os.getenv("CELERY_TIMEZONE", "UTC")
celery_app.conf.beat_schedule = {
    "execute-phase-2": {
        "task": "tasks.execute_phase_2",
        "schedule": _phase_2_interval(),
    }
}

# Make sure the module containing the tasks is imported so Celery can register them
try:
    import tasks  # noqa: F401
except ImportError as exc:  # pragma: no cover - defensive logging
    LOGGER.error("Unable to import Celery tasks: %s", exc)

