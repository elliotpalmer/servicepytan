# ServicePytan Package Review: Recommendations

This document outlines recommendations for improving the `servicepytan` Python package, based on a review of its codebase, documentation, and test coverage.

## 1. Code Enhancements

*   **1.1. `auth.py` - `servicepytan_connect` Simplification:**
    *   **Observation:** The `servicepytan_connect` function has multiple ways to load credentials (direct parameters, environment variables, JSON config file). While flexible, this can make the order of precedence and debugging slightly complex.
    *   **Recommendation:** Consider simplifying the logic if possible. If not, enhance the docstrings and documentation to clearly explain the credential loading hierarchy and provide clear examples for each method.

*   **1.2. `auth.py` - Verify `SERVICETITAN_APP_ID` Usage:**
    *   **Observation:** A comment in `auth.py` (`# AFAICT, app_id is never used in the rest of the code, so it isn't necessary`) suggests `SERVICETITAN_APP_ID` might be unused.
    *   **Recommendation:** Verify if `SERVICETITAN_APP_ID` is indeed used. If not, remove it from `AUTH_VARIABLES`, the `servicepytan_connect` parameters, configuration examples, and documentation to simplify setup for users. If it is used or planned for future use, ensure its purpose is clearly documented.

*   **1.3. `utils.py` - Configuration for `check_default_options`:**
    *   **Observation:** The `check_default_options` function has a `TODO` comment about reading default `pageSize` from a configuration file.
    *   **Recommendation:** Implement this TODO. Allow users to configure default `pageSize` (and potentially other common request options) via the main connection/configuration object.

*   **1.4. `reports.py` - `timezone` in `Report.__init__`:**
    *   **Observation:** The line `self.timezone = get_timezone_by_file(conn)` is commented out in the `Report` class `__init__` method.
    *   **Recommendation:** Determine if timezone information is relevant for reports. If yes, uncomment the line and ensure timezone handling is correctly implemented for report parameters (like dates). If no, remove the commented-out line.

*   **1.5. Consider a `requests.Session` Object:**
    *   **Observation:** The library makes multiple HTTP requests.
    *   **Recommendation:** Consider using a `requests.Session` object, initialized in `servicepytan_connect` and passed to request-making functions. This can improve performance by reusing TCP connections and can also be used to persist certain headers across requests if needed.

*   **1.6. Logging Review:**
    *   **Observation:** Logging is used, but error logging in `utils.py` (e.g., `request_json`) logs the full URL, headers, and payload on error.
    *   **Recommendation:** Review logging levels and messages. Ensure that sensitive information (like API keys in headers or sensitive parts of payloads) is not logged by default, or only at a verbose `DEBUG` level. For standard error logging, consider logging only non-sensitive parts of the request that are essential for debugging.

*   **1.7. Python Version Support & Dependencies:**
    *   **Observation:** The code uses f-strings (Python 3.6+) and `StrEnum` (Python 3.11+ or requires a backport like `enum-compat`).
    *   **Recommendation:**
        *   Clearly state the supported Python versions in `setup.py` (using `python_requires`) and in the documentation.
        *   If compatibility with Python versions older than 3.11 is desired, replace `StrEnum` with `enum.Enum` and string values, or add a conditional dependency on `enum-compat` or a similar library for older versions.

## 2. Error Handling

*   **2.1. Custom Exceptions:**
    *   **Observation:** The library primarily relies on `requests.HTTPError` for API errors.
    *   **Recommendation:** Define a hierarchy of custom exceptions (e.g., `ServicePytanError` as a base, with `AuthenticationError`, `ApiError`, `ReportError`, `InvalidParameterError` inheriting from it). These exceptions can wrap the original `requests.HTTPError` (for API errors) or provide more context for other issues. This allows users to implement more granular error handling.

*   **2.2. Input Validation:**
    *   **Observation:** There's limited explicit input validation before API calls.
    *   **Recommendation:** Add more validation for inputs such as endpoint names, required report parameters, ID formats, etc. Raise specific custom exceptions (e.g., `InvalidParameterError`) if validation fails, providing clear error messages to the user before an API call is made.

*   **2.3. `request_json_with_retry` Configuration:**
    *   **Observation:** The retry mechanism in `request_json_with_retry` (for HTTP 429 errors) has a fixed behavior.
    *   **Recommendation:** While the current implementation is good, consider making the retry behavior (number of retries, backoff strategy) configurable via the connection object for advanced users. At a minimum, clearly document its current fixed behavior (e.g., how it extracts the sleep time from the ServiceTitan error response).

## 3. Testing (Major Area)

*   **3.1. Comprehensive Unit Tests:**
    *   **Observation:** The current test suite (`tests/test_servicepytan.py`) is minimal and primarily tests the CLI. Core library functionality is untested.
    *   **Recommendation:** This is the most critical area for improvement. Implement a comprehensive suite of unit tests covering all modules (`auth.py`, `requests.py`, `data.py`, `reports.py`, `utils.py`, `_dates.py`).
        *   Use mocking libraries (`unittest.mock`, `pytest-mock`) extensively to isolate units of code and simulate API responses without making actual network calls.
        *   Test success paths, failure paths (e.g., API error responses, invalid inputs), and edge cases for all public functions and methods.
        *   Examples: Test `Endpoint.get_all` pagination logic, `Report.get_all_data` timeout and data aggregation, `_dates.py` date conversions with various inputs and timezones, `auth.py` credential loading from different sources.

*   **3.2. Test Structure:**
    *   **Recommendation:** Organize tests into multiple files within the `tests/` directory, mirroring the package structure (e.g., `tests/test_auth.py`, `tests/test_requests.py`, etc.) for better maintainability.

*   **3.3. Integration Tests (Optional but Recommended):**
    *   **Recommendation:** Consider creating a separate suite of integration tests. These tests would make limited, controlled calls to a live ServiceTitan test/sandbox environment (if available).
        *   These tests should be clearly distinguished from unit tests (e.g., using pytest markers) and potentially run separately (e.g., only in CI environments with appropriate credentials configured).

*   **3.4. Test Coverage Tool:**
    *   **Recommendation:** Integrate a test coverage tool (e.g., `coverage.py` with `pytest-cov`). Aim for a high level of test coverage and consider using it to identify untested code paths.

## 4. Documentation

*   **4.1. Complete `docs/configuration.md`:**
    *   **Observation:** This file is currently marked "Under Construction."
    *   **Recommendation:** Fully document all configuration options. This includes:
        *   Detailed explanation of the `servicepytan_config.json` file structure and each field.
        *   How to use environment variables for configuration.
        *   Parameters for the `servicepytan.auth.servicepytan_connect()` function and their precedence.
        *   Any other global settings (e.g., default pageSize if implemented per recommendation 1.3).

*   **4.2. Revamp `docs/reference.md` into an API Reference:**
    *   **Observation:** `docs/reference.md` currently contains notes for developers of the library itself (how to build docs, publish to PyPI).
    *   **Recommendation:**
        *   Transform this section into a proper API reference guide for users of the library.
        *   Ensure all public modules, classes, methods, and functions have comprehensive, well-formatted docstrings (e.g., using Google or NumPy style, as Sphinx Napoleon is apparently used).
        *   Use Sphinx autodoc to generate this API reference from the docstrings. Link it prominently from `docs/index.rst`.
        *   Move the current content of `docs/reference.md` to a `CONTRIBUTING.md` file or a "Developer Guide" section within the documentation.

*   **4.3. Docstring Quality and Completeness:**
    *   **Recommendation:** Conduct a thorough review of all docstrings in the codebase. Ensure they are clear, complete, accurate, and consistently formatted. Document parameters (including types), return values (including types), and any exceptions raised.

*   **4.4. Consistency in Examples and Terminology:**
    *   **Observation:** Minor inconsistencies, e.g., `config_file_path` used as a parameter name in an example for `get_report_categories`, while the function definition in `reports.py` expects `conn`.
    *   **Recommendation:** Ensure consistent use of terminology and parameter names throughout all documentation, examples, and docstrings. The `conn` object, once created, should generally be passed to library functions/methods that need authentication or configuration.

*   **4.5. CLI Documentation:**
    *   **Observation:** The CLI (`cli.py`) is minimally tested and not extensively documented for end-users.
    *   **Recommendation:** If the CLI is intended as a user-facing tool, expand its documentation. Provide examples of its commands and options.

*   **4.6. Add "Best Practices" or "Advanced Usage" Section:**
    *   **Recommendation:** Create a new documentation section that covers:
        *   Tips for efficient data retrieval (e.g., using specific filters, understanding pagination).
        *   Guidance on handling ServiceTitan API rate limits (supplementing the automatic retry for 429 errors).
        *   When to use the `DataService` convenience class versus the more general `Endpoint` class.

## 5. Dependencies

*   **5.1. Review Dependencies:**
    *   **Recommendation:** Periodically review dependencies in `setup.py` (`install_requires`) and `requirements_dev.txt`.
        *   Ensure all listed dependencies are still actively used.
        *   Keep versions reasonably up-to-date for security and functionality, while avoiding overly restrictive pins unless necessary for specific compatibility reasons.
        *   As mentioned in 1.7, address the `StrEnum` Python version compatibility.

## 6. Minor Code Corrections & Refinements

*   **6.1. `utils.py` - `get_timezone_by_file` Bug:**
    *   **Observation:** In `servicepytan/utils.py`, the `get_timezone_by_file` function uses `config['SERVICETITAN_TIMEZONE']` when it should likely be `conn['SERVICETITAN_TIMEZONE']` to align with how `conn` is used as the dictionary holding auth/config details.
    *   **Recommendation:** Correct this line:
        ```python
        # In servicepytan/utils.py, function get_timezone_by_file
        # Change:
        # if "SERVICETITAN_TIMEZONE" in conn:
        #   timezone = config['SERVICETITAN_TIMEZONE'] 
        # To:
        if "SERVICETITAN_TIMEZONE" in conn and conn["SERVICETITAN_TIMEZONE"]: # Also check if not empty
          timezone = conn['SERVICETITAN_TIMEZONE']
        ```
        (Added a check for `conn["SERVICETITAN_TIMEZONE"]` being non-empty as well, assuming empty string means default to UTC).

*   **6.2. `reports.py` - `get_report_categories` and `get_report_list` Parameters:**
    *   **Observation:** In `docs/examples.md`, `get_report_categories` and `get_report_list` are shown called with a `config_file_path` argument and also `conn=st_conn`. The function definitions in `reports.py` only define `conn=None`.
    *   **Recommendation:** Standardize on passing the `conn` object. Remove `config_file_path` from these function calls in examples and rely on the `conn` object (which is already initialized with config). The functions themselves in `reports.py` correctly only accept `conn`. The example calls should be:
        ```python
        # categories = get_report_categories(config_file_path, conn=st_conn) # Old
        categories = get_report_categories(conn=st_conn) # Corrected

        # category_report_list = get_report_list("operations", config_file_path, conn=st_conn) # Old
        category_report_list = get_report_list("operations", conn=st_conn) # Corrected
        ```

This concludes the recommendations. Implementing these changes should significantly enhance the robustness, usability, and maintainability of the `servicepytan` library.
