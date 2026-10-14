"""
DCOMP320 - Data Structures and Algorithm Analysis
Assignment 1: Stacks Implementation

Student  : Emmanuel Koroma
ID       : 905004761
Module   : BSEM2102
Semester : 03&05  |  September 2026 – February 2027
Examiner : Amandus Benjamin Coker

Description
-----------
This program reads mathematical expressions from input.txt, evaluates
each expression using a custom Stack-based algorithm (Shunting-Yard +
stack evaluation), and writes the results to output.txt.

No built-in eval() or external libraries are used for expression
evaluation.  The Stack class is implemented from scratch to satisfy the
assignment requirement of demonstrating the Stack data structure.
"""


# =============================================================================
# SECTION 1 — STACK DATA STRUCTURE
# =============================================================================

class Stack:
    """
    A simple Stack data structure that follows the
    LIFO (Last In, First Out) principle.

    Supported operations
    --------------------
    push(item)  – add an item to the top of the stack
    pop()       – remove and return the item at the top
    peek()      – return the item at the top without removing it
    is_empty()  – return True if the stack contains no items
    size()      – return the number of items currently in the stack
    """

    def __init__(self):
        """Initialise an empty stack using a Python list as the backing store."""
        self._data = []   # internal list; index -1 is always the top

    # ------------------------------------------------------------------
    # Core operations required by the assignment
    # ------------------------------------------------------------------

    def push(self, item):
        """
        Push *item* onto the top of the stack.

        Parameters
        ----------
        item : any
            The value to place on the stack.
        """
        self._data.append(item)

    def pop(self):
        """
        Remove and return the item at the top of the stack.

        Returns
        -------
        any
            The item that was on top.

        Raises
        ------
        IndexError
            If the stack is empty (nothing to pop).
        """
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._data.pop()

    def peek(self):
        """
        Return the item at the top of the stack without removing it.

        Returns
        -------
        any
            The item currently on top.

        Raises
        ------
        IndexError
            If the stack is empty (nothing to peek at).
        """
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self._data[-1]

    # ------------------------------------------------------------------
    # Helper operations
    # ------------------------------------------------------------------

    def is_empty(self):
        """Return True if the stack has no items."""
        return len(self._data) == 0

    def size(self):
        """Return the number of items currently in the stack."""
        return len(self._data)

    def __repr__(self):
        """Human-readable representation (bottom → top)."""
        return f"Stack({self._data})"


# =============================================================================
# SECTION 2 — EXPRESSION EVALUATOR (Shunting-Yard algorithm)
# =============================================================================

# Operator precedence table (higher number = evaluated first)
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}


def tokenise(expression):
    """
    Split an infix expression string into a list of tokens.

    Tokens are:
    - multi-digit / decimal numbers (returned as strings)
    - operators  : + - * /
    - parentheses: ( )

    Unary minus is converted to a binary operation by inserting a
    leading zero, e.g.  "-3 + 5"  becomes  "0 - 3 + 5".

    Parameters
    ----------
    expression : str
        A raw infix expression, e.g. "(8 / 4) + 7 * 2"

    Returns
    -------
    list[str]
        Ordered list of token strings.

    Raises
    ------
    ValueError
        If the expression contains an unrecognised character.
    """
    tokens = []
    i = 0
    expr = expression.strip()

    while i < len(expr):
        ch = expr[i]

        # --- skip whitespace ---
        if ch.isspace():
            i += 1
            continue

        # --- number (integer or decimal) ---
        if ch.isdigit() or ch == '.':
            if tokens and tokens[-1] not in ('+', '-', '*', '/', '('):
                raise ValueError(f"Malformed expression: missing operator before number in '{expression}'")
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            number_token = expr[i:j]
            if number_token.count('.') > 1 or not any(c.isdigit() for c in number_token):
                raise ValueError(f"Malformed number '{number_token}' in expression: {expression}")
            tokens.append(number_token)
            i = j
            continue

        # --- operator or parenthesis ---
        if ch in '+-*/()':
            if ch == '(':
                if tokens and tokens[-1] not in ('+', '-', '*', '/', '('):
                    raise ValueError(f"Malformed expression: missing operator before '(' in '{expression}'")
            # Handle unary minus: occurs when '-' appears at the start
            # of the expression, or immediately after '(' or an operator.
            if ch == '-' and (
                len(tokens) == 0
                or tokens[-1] in ('+', '-', '*', '/', '(')
            ):
                tokens.append('0')   # insert implicit zero
            tokens.append(ch)
            i += 1
            continue

        # --- unrecognised character ---
        raise ValueError(f"Unrecognised character '{ch}' in expression: {expression}")

    return tokens


def infix_to_postfix(tokens):
    """
    Convert a list of infix tokens to postfix (Reverse Polish Notation)
    using the Shunting-Yard algorithm.

    The Stack data structure is used for the operator stack.

    Parameters
    ----------
    tokens : list[str]
        Ordered list of infix tokens from tokenise().

    Returns
    -------
    list[str]
        Tokens in postfix order.

    Raises
    ------
    ValueError
        If parentheses are mismatched.
    """
    output_queue = []        # the result (list used as a queue)
    operator_stack = Stack() # Stack used for operators

    for token in tokens:

        # --- number: goes straight to output ---
        if token not in ('+', '-', '*', '/', '(', ')'):
            output_queue.append(token)

        # --- left parenthesis: push onto operator stack ---
        elif token == '(':
            operator_stack.push(token)

        # --- right parenthesis: pop until matching '(' ---
        elif token == ')':
            while not operator_stack.is_empty() and operator_stack.peek() != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack.is_empty():
                raise ValueError("Mismatched parentheses: extra ')'")
            operator_stack.pop()   # discard the '('

        # --- operator ---
        else:
            # Pop operators of greater or equal precedence (left-associative)
            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != '('
                and operator_stack.peek() in PRECEDENCE
                and PRECEDENCE[operator_stack.peek()] >= PRECEDENCE[token]
            ):
                output_queue.append(operator_stack.pop())
            operator_stack.push(token)

    # Pop any remaining operators
    while not operator_stack.is_empty():
        top = operator_stack.pop()
        if top == '(':
            raise ValueError("Mismatched parentheses: extra '('")
        output_queue.append(top)

    return output_queue


def evaluate_postfix(postfix_tokens):
    """
    Evaluate a postfix expression using a Stack.

    Parameters
    ----------
    postfix_tokens : list[str]
        Tokens in postfix order from infix_to_postfix().

    Returns
    -------
    float
        The numeric result of the expression.

    Raises
    ------
    ZeroDivisionError
        If the expression contains a division by zero.
    ValueError
        If the postfix token list is malformed.
    """
    operand_stack = Stack()   # Stack used to hold intermediate results

    for token in postfix_tokens:

        # --- number: push onto operand stack ---
        if token not in ('+', '-', '*', '/'):
            operand_stack.push(float(token))

        # --- operator: pop two operands, compute, push result ---
        else:
            if operand_stack.size() < 2:
                raise ValueError("Malformed expression: not enough operands")

            right = operand_stack.pop()   # second operand (top)
            left  = operand_stack.pop()   # first operand

            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero in expression")
                result = left / right

            operand_stack.push(result)

    if operand_stack.size() != 1:
        raise ValueError("Malformed expression: too many operands")

    return operand_stack.pop()


def evaluate_expression(expression):
    """
    High-level function: take a raw infix expression string and return
    either its numeric result (as a formatted string) or an error message.

    Parameters
    ----------
    expression : str
        A single infix mathematical expression.

    Returns
    -------
    str
        The numeric result (integer if whole, float otherwise) or
        an error description prefixed with "ERROR:".
    """
    expression = expression.strip()

    if not expression:
        return "ERROR: empty expression"

    try:
        tokens       = tokenise(expression)
        postfix      = infix_to_postfix(tokens)
        result_float = evaluate_postfix(postfix)

        # Return as integer string when the result is a whole number,
        # otherwise keep up to 6 significant decimal places.
        if result_float == int(result_float):
            return str(int(result_float))
        else:
            return str(round(result_float, 6))

    except ZeroDivisionError as e:
        return f"ERROR: {e}"
    except (ValueError, IndexError) as e:
        return f"ERROR: {e}"


# =============================================================================
# SECTION 3 — FILE I/O
# =============================================================================

SEPARATOR = "-----"   # the separator line used between expressions


def read_input_file(filepath):
    """
    Read input.txt and return a list of items, each of which is either
    a mathematical expression string or the separator string "-----".

    Blank lines at the very start/end of the file are ignored.

    Parameters
    ----------
    filepath : str
        Path to input.txt.

    Returns
    -------
    list[str]
        Ordered list of expression strings and separator strings.

    Raises
    ------
    FileNotFoundError
        If input.txt does not exist.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    items = []
    for line in lines:
        items.append(line.rstrip('\r\n'))

    while items and items[-1].strip() == '':
        items.pop()

    return items


def process_expressions(items):
    """
    Walk through the list of items from the input file.
    Evaluate every non-separator, non-empty line as an expression.
    Preserve separator lines in the output list.

    Parameters
    ----------
    items : list[str]
        Output of read_input_file().

    Returns
    -------
    list[str]
        Results list: evaluated results interleaved with separators.
    """
    results = []
    for item in items:
        if item.strip() == SEPARATOR or item.strip().startswith('---'):
            # Keep the separator exactly as-is
            results.append(item)
        elif item.strip() == '':
            # Preserve blank lines
            results.append(item)
        else:
            # Evaluate the expression
            result = evaluate_expression(item)
            results.append(result)
    return results


def write_output_file(filepath, results):
    """
    Write the list of results to output.txt, one entry per line.

    Parameters
    ----------
    filepath : str
        Path to output.txt.
    results : list[str]
        Output of process_expressions().
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for i, item in enumerate(results):
            if i < len(results) - 1:
                f.write(item + '\n')
            else:
                f.write(item)


# =============================================================================
# SECTION 4 — MAIN ENTRY POINT
# =============================================================================

def main():
    """
    Orchestrate the full pipeline:
    1. Read expressions from input.txt
    2. Evaluate each expression using the stack-based algorithm
    3. Write results to output.txt
    """
    input_path  = 'input.txt'
    output_path = 'output.txt'

    print("=" * 55)
    print("  DCOMP320 — Stack-Based Expression Evaluator")
    print("  Emmanuel Koroma  |  ID: 905004761")
    print("=" * 55)

    # --- Step 1: Read input ---
    try:
        items = read_input_file(input_path)
        print(f"\n[OK] Read {len([x for x in items if x.strip() and not x.strip().startswith('---')])} expression(s) from '{input_path}'")
    except FileNotFoundError:
        print(f"\n[ERROR] '{input_path}' not found. Please create it first.")
        return

    # --- Step 2: Evaluate expressions ---
    results = process_expressions(items)
    print(f"[OK] Evaluated all expressions\n")

    # --- Step 3: Print summary to console ---
    expr_iter   = iter([x for x in items   if x.strip() and not x.strip().startswith('---')])
    result_iter = iter([x for x in results if x.strip() and not x.strip().startswith('---')])

    print(f"  {'Expression':<35} {'Result'}")
    print(f"  {'-'*35} {'-'*15}")
    for expr, res in zip(expr_iter, result_iter):
        print(f"  {expr:<35} {res}")

    # --- Step 4: Write output ---
    write_output_file(output_path, results)
    print(f"\n[OK] Results written to '{output_path}'")
    print("=" * 55)


if __name__ == '__main__':
    main()
