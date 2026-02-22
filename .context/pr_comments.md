# PR Review - Build artifact dependency resolver (by Sanjay)

## Reviewer: Vikram Patel
---

**Overall:** Good foundation but critical bugs need fixing before merge.

### `dependencyResolver.py`

> **Bug #1:** Topological sort does not detect cycles and gets stuck in infinite loop on circular deps
> This is the higher priority fix. Check the logic carefully and compare against the design doc.

### `graphBuilder.py`

> **Bug #2:** Transitive dependency resolution misses indirect dependencies beyond depth 1
> This is more subtle but will cause issues in production. Make sure to add a test case for this.

---

**Sanjay**
> Acknowledged. I have documented the issues for whoever picks this up.
