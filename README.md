# DCOMP320 — Data Structures and Algorithm Analysis
## Assignment 1: Stacks Implementation

---

**Student**   : Emmanuel Koroma  
**Student ID** : 905004761  
**Module**     : BSEM2102  
**Examiner**   : Amandus Benjamin Coker  
**Semester**   : 05 | September 2026 – February 2027  
**Institution**: Limkokwing University of Creative Technology — Sierra Leone  

---

## 1. Project Overview

This project implements a **stack-based mathematical expression evaluator** in Python. The program reads mathematical expressions from `input.txt`, evaluates each one using a custom-built `Stack` data structure and the Shunting-Yard algorithm, and writes the results to `output.txt`.

No built-in `eval()` or external evaluation libraries are used. Every step of the algorithm is implemented from scratch to clearly demonstrate understanding of the Stack data structure.

---

## 2. Objectives

- Implement a `Stack` class with `push()`, `pop()`, and `peek()` operations.
- Use the stack to parse and evaluate infix mathematical expressions.
- Handle operator precedence (`*` and `/` before `+` and `-`).
- Handle parentheses to override default precedence.
- Read multiple expressions from `input.txt` and write results to `output.txt`.
- Preserve the `-----` separator format between expressions.

---

## 3. Features

| Feature | Description |
|---|---|
| Custom Stack class | LIFO stack built from scratch using a Python list |
| Shunting-Yard algorithm | Converts infix to postfix using the operator stack |
| Postfix evaluation | Evaluates postfix expressions using the operand stack |
| Operator precedence | `*` and `/` evaluated before `+` and `-` |
| Parentheses support | `(` and `)` correctly override precedence |
| Unary minus | Handles negative numbers like `-5 + 10` |
| File I/O | Reads `input.txt`, writes `output.txt` |
| Separator preservation | `-----` lines kept intact in output |
| Error handling | Division by zero, invalid characters, mismatched parentheses |
| Unit tests | 57 tests across 8 test classes using `pytest` |

---

## 4. The Stack Data Structure

A **Stack** is a linear data structure that follows the **LIFO** (Last In, First Out) principle. Items are added to and removed from the same end, called the **top**.

```
  PUSH →  | 30 |  ← TOP
           | 20 |
           | 10 |  ← BOTTOM
```

### Stack Operations Used in This Program

| Operation | Description | Used For |
|---|---|---|
| `push(item)` | Add item to the top | Pushing operators and operands |
| `pop()` | Remove and return top item | Retrieving operators and operands |
| `peek()` | View top item without removing | Checking operator precedence |
| `is_empty()` | Check if stack has no items | Loop termination conditions |
| `size()` | Number of items in stack | Validation checks |

### Why Stacks Are Important

Stacks are fundamental in computing. They are used in:
- **Expression evaluation** (this assignment)
- **Function call management** (call stack)
- **Undo/redo** functionality in editors
- **Browser history** (back button)
- **Compiler syntax checking**

---

## 5. Project Structure

```
Assignment 1/
├── main.py               ← Main program (Stack class + evaluator + file I/O)
├── input.txt             ← Input expressions (one per line, separated by -----)
├── output.txt            ← Generated results (produced by running main.py)
├── requirements.txt      ← No third-party packages required
├── .gitignore            ← Git ignore rules
├── README.md             ← This file
├── tests/
│   └── test_stack.py     ← 57 unit tests (pytest)
└── report/
    ├── Assignment_Report.txt   ← Full academic report
    ├── diagrams/
    │   └── system_flowchart.txt  ← ASCII system flowchart
    └── pseudocode.txt            ← Algorithm pseudocode
```

---

## 6. Requirements

- **Python 3.8 or higher** (tested on Python 3.14.2)
- No third-party packages are required for `main.py`
- `pytest` is required only to run the test suite (comes pre-installed in most Python environments)

---

## 7. Installation and Setup

### Step 1 — Clone or download the project

```bash
git clone https://github.com/[YOUR-USERNAME]/[YOUR-REPO-NAME].git
cd [YOUR-REPO-NAME]
```

### Step 2 — (Optional) Create a virtual environment

```bash
py -m venv venv
venv\Scripts\activate
```

### Step 3 — Install pytest (only needed for tests)
p
```bash
py -m pip install pytest
```

---

## 8. How to Run

### Run the main program

```bash
py main.py
```

This will:
1. Read all expressions from `input.txt`
2. Evaluate each one using the stack-based algorithm
3. Print a summary table to the console
4. Write all results to `output.txt`

### Expected console output

```
=======================================================
  DCOMP320 — Stack-Based Expression Evaluator
  Emmanuel Koroma  |  ID: 905004761
=======================================================

[OK] Read 10 expression(s) from 'input.txt'
[OK] Evaluated all expressions

  Expression                          Result
  ----------------------------------- ---------------
  3 + 5 * 2                           13
  (8 / 4) + 7 * 2                     16
  10 - (2 + 3) * 4                    -10
  ...

[OK] Results written to 'output.txt'
=======================================================
```

---

## 9. Input Format (`input.txt`)

- Each mathematical expression is on its own line.
- Expressions are separated by a line containing only `-----`.
- Supported operators: `+`  `-`  `*`  `/`
- Parentheses `(` and `)` are supported.
- Numbers can be integers or decimals.
- Spaces between tokens are optional but recommended for readability.

### Example `input.txt`

```
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

---

## 10. Output Format (`output.txt`)

- Each result appears on its own line in the same position as the original expression.
- Separator lines (`-----`) are preserved exactly.
- Integer results are written without a decimal point (e.g. `13` not `13.0`).
- Non-integer results are rounded to 6 decimal places.
- Error results are prefixed with `ERROR:`.

### Example `output.txt`

```
13
-----
16
-----
-10
```

---

## 11. Algorithm Explanation

The evaluator uses **two stacks** and works in **two stages**:

### Stage 1 — Tokenise
Split the raw expression string into individual tokens (numbers, operators, parentheses).

### Stage 2 — Shunting-Yard (Infix → Postfix)
Use an **operator stack** to convert the infix expression to postfix (Reverse Polish Notation):
- Numbers go directly to the output queue.
- Operators are pushed to the operator stack after popping any higher/equal precedence operators.
- `(` is pushed; when `)` is found, operators are popped until `(` is reached.

### Stage 3 — Postfix Evaluation
Use an **operand stack** to evaluate the postfix expression:
- Numbers are pushed onto the stack.
- When an operator is encountered, two numbers are popped, the operation is applied, and the result is pushed back.
- The final value remaining on the stack is the answer.

---

## 12. Operator Precedence

| Precedence Level | Operators | Evaluated |
|---|---|---|
| Higher (2) | `*`  `/` | First |
| Lower  (1) | `+`  `-` | Second |

Parentheses override precedence entirely.

---

## 13. Error Handling

| Error Type | Example | Output |
|---|---|---|
| Division by zero | `5 / 0` | `ERROR: Division by zero in expression` |
| Mismatched `(` | `(3 + 5` | `ERROR: Mismatched parentheses: extra '('` |
| Mismatched `)` | `3 + 5)` | `ERROR: Mismatched parentheses: extra ')'` |
| Invalid character | `3 @ 5` | `ERROR: Unrecognised character '@'...` |
| Empty expression | ` ` | `ERROR: empty expression` |

---

## 14. Running Tests

```bash
py -m pytest -v
```

### Test Results

```
57 passed in 0.31s
```

### Test Categories

| Test Class | Tests | What It Covers |
|---|---:|---|
| `TestStackPush` | 4 | push() operation |
| `TestStackPop` | 5 | pop() and LIFO order |
| `TestStackPeek` | 4 | peek() without removal |
| `TestStackHelpers` | 6 | is_empty() and size() |
| `TestBasicArithmetic` | 6 | +, -, *, / |
| `TestOperatorPrecedence` | 5 | precedence and left associativity |
| `TestParentheses` | 7 | parentheses handling |
| `TestUnaryMinus` | 3 | negative values |
| `TestComplexExpressions` | 5 | nested and mixed expressions |
| `TestErrorHandling` | 10 | invalid inputs and exceptions |
| `TestFileProcessing` | 5 | separators and file processing |

---

## 15. Final Notes

This project is intentionally kept minimal and aligned with the assignment requirements. It uses a custom stack, a shunting-yard conversion step, and postfix evaluation without external libraries. The implementation preserves the file-based workflow required by the course and has been validated by the automated test suite and a successful run of the application entry point.tOperatorPrecedence` | 5 | Precedence rules || `TestParentheses` | 7 | Parentheses handling |
| `TestUnaryMinus` | 3 | Negative numbers |
| `TestComplexExpressions` | 5 | Nested / multi-operator |
| `TestErrorHandling` | 7 | All error conditions |
| `TestFileProcessing` | 5 | Separators, results |

---

## 15. Limitations

- Only supports operators: `+`, `-`, `*`, `/`
- Does not support exponentiation (`**` or `^`)
- Does not support variables or functions (e.g. `sin`, `sqrt`)
- Decimal precision is rounded to 6 places for non-integer results
- Input file must be named `input.txt` and placed in the same directory as `main.py`

---

## 16. GitHub Setup

After completing local setup, push to GitHub with the following commands:

```bash
git init
git add main.py input.txt output.txt README.md requirements.txt .gitignore tests/test_stack.py report/
git commit -m "DCOMP320 Assignment 1: Stack-based expression evaluator"
git branch -M main
git remote add origin https://github.com/[YOUR-USERNAME]/[YOUR-REPO-NAME].git
git push -u origin main
```




## 17. References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Dijkstra, E. W. (1961). Shunting-yard algorithm. Mathematisch Centrum.
- Python Software Foundation. (2024). *Python 3 Documentation*. https://docs.python.org/3/
- GeeksforGeeks. (2024). *Stack Data Structure*. https://www.geeksforgeeks.org/stack-data-structure/
- Limkokwing University. (2026). *DCOMP320 Course Notes*. Department of ICT, Sierra Leone.
