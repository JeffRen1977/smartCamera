# 1. Business & Application Layer

Defines customer needs and maps business scenarios to AI model calls.

## Scene Modules

| Directory | Scene | Typical Needs |
|-----------|-------|---------------|
| `assembly_guidance/` | Human-Augmented Assembly | In-process verification, visual SOP, digital traveler |
| `quality_assurance/` | Quality Assurance & Zero-Defect | Micro-defect detection, OCR/OCV, 3D dimension measurement |
| `safety_compliance/` | Safety & Compliance | PPE detection, virtual fence, behavior risk analysis |
| `logistics_automation/` | Logistics & Throughput | Bottleneck analysis, auto sorting, AMR/AGV navigation |

## Adaptive Logic

Customers don't care about hardware brand—only "can it detect hard hat/parts/defects" or "guide assembly steps." This layer maps needs to algorithm library models.
