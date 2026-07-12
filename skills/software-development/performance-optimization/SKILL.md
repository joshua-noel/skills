---
name: performance-optimization
description: Improve measured latency, throughput, memory, bundle size, or resource efficiency without sacrificing correctness or maintainability. Use when a measurable performance target is missed.
license: MIT
metadata:
  category: software-development
  origin: custom-synthesis
  revision: "1.1.0"
---

# Performance Optimization

## Trigger

- Profiling identifies a hot path.
- A user requests optimization with a clear workload.

## Inputs

- Baseline metrics and representative workload
- Profiler/traces
- Correctness tests
- Resource and compatibility constraints

## Procedure

1. Define the metric, workload, percentile, and target before editing.
2. Measure a repeatable baseline and account for warm-up/noise.
3. Profile to identify the dominant cost rather than optimizing intuition.
4. Estimate the ceiling of each candidate optimization.
5. Prefer algorithmic, I/O, allocation, caching, batching, and query improvements before micro-optimizations.
6. Implement one material change at a time.
7. Re-measure under the same workload and verify correctness.
8. Document trade-offs, invalidation rules, and operational impact.

## Output contract

- Before/after benchmark
- Optimized implementation
- Correctness and regression evidence
- Trade-off record

## Quality gates

- Improvement is statistically or operationally meaningful.
- No benchmark-only shortcut.
- Cache correctness and memory bounds are explicit.
- Readability loss is justified by measured value.

## Handoffs and dependencies

- `system-design/scalability-and-reliability`
- `debugging`
- `code-review`
- `operations/deployment-readiness`

## Boundaries

- Do not optimize without a baseline.
- Do not report synthetic gains as production gains.
- Do not remove validation, accessibility, security, or observability for speed.
