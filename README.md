# Enthropic Heavens Map Editor

This repository contains the tooling used to process turn data for Enthropic Heavens.
The workflow is split into phases, and phase 2 is responsible for producing updated
political and exploration maps based on the latest player state.

## Automated phase 2 execution

Phase 2 can now be executed automatically through a Celery worker and scheduler.
The Celery task `tasks.execute_phase_2` wraps the existing `phase_2` function from
`main.py` and reads its turn number from either the task arguments or the
`PHASE_2_TURN` environment variable. The scheduling interval is configurable via
`PHASE_2_INTERVAL_MINUTES` (defaults to once per hour).

Environment variables recognised by the Celery processes:

| Variable | Description |
| --- | --- |
| `PHASE_2_TURN` | Turn identifier passed to the `phase_2` function when the scheduled task runs. |
| `PHASE_2_INTERVAL_MINUTES` | Frequency, in minutes, between automatic executions (defaults to `60`). |
| `CELERY_BROKER_URL` | Broker connection string (defaults to `redis://redis:6379/0`). |
| `CELERY_RESULT_BACKEND` | Result backend connection string (defaults to `redis://redis:6379/0`). |
| `CELERY_TIMEZONE` | Timezone used by Celery beat (defaults to `UTC`). |

You can also manually trigger the task from a Python shell:

```python
from tasks import execute_phase_2
execute_phase_2.delay(turn=31)
```

If no explicit turn is supplied, ensure `PHASE_2_TURN` is exported in the
environment before invoking the task or starting the Celery services.

## Dockerised workflow

A Docker image and Compose configuration are provided to simplify running the
Celery worker, scheduler, and Redis broker.

1. Copy the sample environment file and adjust it for your campaign:
   ```bash
   cp .env.example .env
   # edit .env to set the correct PHASE_2_TURN value
   ```
2. Ensure the required data files exist locally. The application expects to read
   from `databases/Player_DB.pickle` (and potentially other files in that
   directory). Mount or copy the latest database dumps into `./databases` before
   starting the services.
3. Build and start the stack:
   ```bash
   docker compose up --build
   ```

The compose file defines three services:

- `redis` – lightweight Redis instance serving as the Celery broker/backend.
- `celery-worker` – processes queued tasks and runs `phase_2` when invoked.
- `celery-beat` – schedules `execute_phase_2` based on `PHASE_2_INTERVAL_MINUTES`.

Generated map images are written to the `maps/` directory, which is mounted to
the host for convenience.

To trigger a one-off execution without waiting for the schedule you can run:

```bash
docker compose run --rm celery-worker celery -A celery_app.celery_app call tasks.execute_phase_2 --args='[31]'
```

Stop the stack when finished:

```bash
docker compose down
```

## Development notes

- Requirements are listed in `requirements.txt` and installed automatically when
  building the Docker image.
- The Celery configuration lives in `celery_app.py` with the associated tasks in
  `tasks.py`.
- Local outputs are written to `maps/` (ignored by git except for the placeholder
  `.gitignore`). Add your own database dumps to `databases/` – the directory is
  tracked with an empty `.gitkeep` file to make it available by default.
