# 1. Business & Application Layer

Defines customer needs and maps business scenarios to AI model calls.

## Scene Modules

| Directory | Scene | Typical Needs |
|-----------|-------|---------------|
| `defect_detection/` | Industrial defect detection | Millisecond reject, surface scratch/crack detection |
| `ppe_monitoring/` | Safety & PPE monitoring | Hard hat, safety vest, restricted zone |
| `predictive_maintenance/` | Predictive maintenance | Audio+vision, bearing/equipment anomaly |
| `amr_navigation/` | AMR/AGV navigation | SLAM, obstacle avoidance, semantic segmentation, depth |

## Adaptive Logic

Customers don't care about hardware brand—only "can it detect hard hat/parts/defects." This layer maps needs to algorithm library models.
