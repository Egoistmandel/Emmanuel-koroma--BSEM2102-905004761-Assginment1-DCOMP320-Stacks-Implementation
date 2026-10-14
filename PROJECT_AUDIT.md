# Project Audit and Compliance Review

Project: Stack-Based Mathematical Expression Evaluator Using Python  
Course: DCOMP320 — Data Structures and Algorithm Analysis  
Student: Emmanuel Koroma  
Student ID: 905004761  
Programme: BSEM2102

## Requirement compliance checklist

| Requirement. | Source in the assignment. | Existing implementation. | Verification method. | Status. | Action taken. |
|---|---|---|---|---|---|
| Implement a stack-based evaluator for mathematical expressions. | Assignment brief and project master prompt. | `main.py` defines a custom `Stack` and evaluates infix expressions through tokenisation, shunting-yard conversion, and postfix evaluation. | Run `py main.py` and inspect `output.txt`; confirm console summary and final outputs. | PASS | No functional change required beyond final validation and documentation cleanup. |
| Correct `Stack` class with `push()`, `pop()`, and `peek()`. | Assignment requirement + project specification. | `Stack.push()`, `Stack.pop()`, and `Stack.peek()` are implemented and use LIFO list storage. | Unit tests for stack operations pass. | PASS | Verified and retained. |
| Safe empty-stack behaviour. | Assignment requirement on stack correctness and defensive implementation. | `pop()` and `peek()` raise `IndexError` when empty; `is_empty()` reports the current state. | Unit tests confirm exceptions on empty stack. | PASS | Retained and documented. |
| Expression tokenizer with correct token recognition. | Requirement to process numeric and operator tokens. | `tokenise()` identifies digits, decimals, operators, parentheses, and whitespace, and rejects invalid characters. | Automated tests and manual validation of tokenization cases. | PASS | Improved robustness for malformed numeric input and whitespace handling. |
| Infix-to-postfix conversion. | Assignment requirement and current architecture. | `infix_to_postfix()` uses the shunting-yard algorithm with precedence and parentheses handling. | Unit tests for precedence and parentheses pass. | PASS | Confirmed and documented. |
| Postfix evaluation using a stack. | Assignment requirement. | `evaluate_postfix()` uses a second stack and validates missing operands, excess operands, and division by zero. | Automated tests for arithmetic, malformed expressions, and errors pass. | PASS | Kept aligned with current architecture. |
| Correct operator precedence and left associativity. | Explicit assignment examples include `3 + 5 * 2 = 13` and other precedence examples. | Precedence table is `+`/`-` = 1, `*`/`/` = 2; equals precedence pops from stack left to right. | Unit tests cover precedence and chaining. | PASS | Verified with test suite. |
| Parentheses handling. | Explicit assignment requirement and examples. | Parentheses are pushed and popped correctly; mismatched parentheses raise `ValueError`. | Unit tests for nested and mismatched parentheses pass. | PASS | Verified. |
| Supported operators. | Assignment examples and project brief show `+ - * /`. | Code supports `+`, `-`, `*`, `/` only and rejects unsupported symbols. | Tests for invalid characters and supported arithmetic pass. | PASS | No unsupported operators were added. |
| Numeric formatting. | Assignment requirement on output format and examples. | Whole numbers output as integers; non-whole results are rounded to 6 decimal places. | Execution and unit tests confirm expected printed strings. | PASS | Final validation done. |
| Invalid expression handling. | Requirement to handle malformed expressions. | Errors are returned as strings beginning with `ERROR:` for empty input, invalid characters, missing operands, excess operands, and mismatched parentheses. | Tests for invalid expressions and error string prefixes. | PASS | Confirmed. |
| Division by zero handling. | Assignment requirement explicitly mentions division by zero. | `evaluate_postfix()` raises `ZeroDivisionError`; `evaluate_expression()` converts it to `ERROR: ...`. | Dedicated tests for `5 / 0` and `10 / (5 - 5)` pass. | PASS | Verified. |
| Multiple expressions and separators. | Assignment requirement to read multiple lines and preserve separator lines. | `read_input_file()`, `process_expressions()`, and `write_output_file()` preserve `-----` separators and evaluate each expression in order. | Unit tests and execution on `input.txt` both pass. | PASS | Verified. |
| Output-file generation. | Required deliverable to write results to `output.txt`. | `main.py` writes evaluated output to `output.txt` and prints a summary. | Run `py main.py`; inspect `output.txt`. | PASS | Output file preserved and verified. |
| Automated tests. | Required project deliverable and testing phase. | `tests/test_stack.py` contains a comprehensive unit test suite. | Run `py -m pytest -v`. | PASS | Test suite passes with 57 tests. |
| Project documentation. | Assignment requires professional documentation and report. | `README.md` is present, and the report directory contains `Assignment_Report.txt` and algorithm notes. | Review of file content and final project structure. | PASS | README was cleaned and finalized; audit checklist added. |
| README accuracy and execution instructions. | Assignment requirement for clear project documentation. | README includes project purpose, features, run instructions, input/output format, supported operators, error handling, and tests. | README review against final implementation. | PASS | Updated to reflect the exact implementation and commands. |
| Report coverage and final report format. | Assignment expects a report with sections including introduction, problem statement, stack explanation, pseudocode, diagram, testing, results, and conclusion. | Existing report draft is present and aligned to the implemented architecture. | Review of `report/Assignment_Report.txt` and algorithm files. | PASS | Retained and aligned to final implementation. |
| Submission file structure. | Assignment mentions required project files and report folders. | Project root contains `main.py`, `input.txt`, `output.txt`, `README.md`, `requirements.txt`, `.gitignore`, `tests/`, `report/`, and `PROJECT_AUDIT.md`. | Directory inspection. | PASS | Final structure is consistent with the assignment. |
| PDF requirement reading. | Assignment authorises reading the original PDF as the primary source. | The project folder includes the assignment PDF; however direct OCR access was limited in this environment. The task brief itself supplied the authoritative requirement set. | Direct source review is limited to the task brief and workspace project files. | NOT VERIFIED | The project was audited against the supplied assignment specification and the implementation was validated by tests and execution. |
| Optional or unnecessary file cleanup. | Project cleanliness and removal of irrelevant files. | Cache files and hidden editor artifacts remain excluded by `.gitignore`; no unrelated source files were removed. | Directory and file inspection. | PASS | No unnecessary source files were deleted. |

## Final audit result

The final implementation satisfies the essential stack and expression-evaluation requirements in the assignment brief and the project specification. The project is functionally correct, the automated tests are passing, and the supporting documentation is aligned with the actual code behavior.

## Validation commands used

- `py -m pytest -v`
- `py main.py`

These checks produced successful execution and 57 passing tests.
