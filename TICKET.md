# PLATFORM-2955: Fix build artifact dependency resolver

**Status:** In Progress · **Priority:** High
**Sprint:** Sprint 29 · **Story Points:** 5
**Reporter:** Suresh Kumar (DevOps Lead) · **Assignee:** You (Intern)
**Due:** End of sprint (Friday)
**Labels:** `backend`, `python`, `ci-cd`, `graph`
**Task Type:** Bug Fix

---

## Description

The build dependency resolver uses topological sort to determine build order. It has two bugs causing builds to fail or execute in the wrong order. Bugs are marked with `# BUG:` comments.

## Acceptance Criteria

- [ ] Bug #1 fixed: Cycle detection is inverted — reports cycles for valid DAGs and misses actual cycles
- [ ] Bug #2 fixed: Build order is reversed — dependencies build AFTER dependents
- [ ] All unit tests pass
