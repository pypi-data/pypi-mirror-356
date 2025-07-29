# Changelog

All notable changes to this project will be documented in this file.

---

## [2.0.0] - 2025-06-18

### ⚠️ Breaking Changes

- 🔁 **Method Renamed**  
  The `summary(options)` method has been removed and replaced with `comparison(options)`.  
  
  **Before (Python):**
  ```python
  result = client.summary(options)
  ```

  **After (Python):**
  ```python
  result = client.comparison(options)
  ```