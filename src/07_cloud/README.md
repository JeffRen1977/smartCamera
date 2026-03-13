# 7. Cloud Platform Monitoring & Management

Control center for edge devices—device monitoring, model OTA, effect detection.

## Modules

| Directory | Function |
|-----------|----------|
| `agent/` | Edge Agent: heartbeat, metrics, OTA receive |
| `backend/` | Cloud backend: API, deploy engine, monitoring, effect analysis |
| `dashboard/` | Monitoring dashboard: Grafana, etc. |

## Core Capabilities

- **Device monitoring**: Online status, resource usage, inference FPS
- **Model auto rollout**: OTA push new models, gray release and rollback
- **Effect auto detection**: Confidence distribution, latency, false/miss alerts
