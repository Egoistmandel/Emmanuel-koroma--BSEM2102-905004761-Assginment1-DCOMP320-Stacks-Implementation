"""
DCOMP320 - Data Structures and Algorithm Analysis
Assignment 1: Stacks Implementation

Test Suite
----------
Tests cover:
  1.  Stack class — push, pop, peek, is_empty, size
  2.  Stack error handling — empty stack exceptions
  3.  Expression evaluator — basic operations
  4.  Operator precedence
  5.  Parentheses
  6.  Unary minus (negative numbers)
  7.  Complex / nested expressions
  8.  Division by zero
  9.  Invalid / malformed expressions
  10. File processing helpers
"""

import sys
import os
import unittest

# Make sure we can import from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import (
    Stack,
    evaluate_expression,
    tokenise,
    infix_to_postfix,
    evaluate_postfix,
    process_expressions,
    SEPARATOR,
)


# =============================================================================
# 1.  Stack — basic operations
# =============================================================================

class TestStackPush(unittest.TestCase):
    """Tests for Stack.push()"""

    def test_push_single_item(self):
        s = Stack()
        s.push(10)
        self.assertEqual(s.size(), 1)

    def test_push_multiple_items(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.size(), 3)

    def test_push_preserves_order(self):
        """The last item pushed should be on top."""
        s = Stack()
        s.push('a')
        s.push('b')
        s.push('c')
        self.assertEqual(s.peek(), 'c')

    def test_push_various_types(self):
        s = Stack()
        s.push(42)
        s.push(3.14)
        s.push('hello')
        s.push([1, 2, 3])
        self.assertEqual(s.size(), 4)


class TestStackPop(unittest.TestCase):
    """Tests for Stack.pop()"""

    def test_pop_returns_last_pushed(self):
        s = Stack()
        s.push(10)
        s.push(20)
        self.assertEqual(s.pop(), 20)

    def test_pop_decreases_size(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.pop()
        self.assertEqual(s.size(), 1)

    def test_pop_lifo_order(self):
        """LIFO: last in, first out."""
        s = Stack()
        for i in [5, 10, 15]:
            s.push(i)
        self.assertEqual(s.pop(), 15)
        self.assertEqual(s.pop(), 10)
        self.assertEqual(s.pop(), 5)

    def test_pop_empty_stack_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_pop_until_empty(self):
        s = Stack()
        s.push('x')
        s.pop()
        self.assertTrue(s.is_empty())


class TestStackPeek(unittest.TestCase):
    """Tests for Stack.peek()"""

    def test_peek_returns_top(self):
        s = Stack()
        s.push(99)
        self.assertEqual(s.peek(), 99)

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(7)
        s.peek()
        self.assertEqual(s.size(), 1)

    def test_peek_after_push(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.peek()          # should still be 2
        self.assertEqual(s.peek(), 2)

    def test_peek_empty_stack_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.peek()


class TestStackHelpers(unittest.TestCase):
    """Tests for Stack.is_empty() and Stack.size()"""

    def test_is_empty_on_new_stack(self):
        s = Stack()
        self.assertTrue(s.is_empty())

    def test_is_empty_after_push(self):
        s = Stack()
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_is_empty_after_push_and_pop(self):
        s = Stack()
        s.push(1)
        s.pop()
        self.assertTrue(s.is_empty())

    def test_size_empty(self):
        s = Stack()
        self.assertEqual(s.size(), 0)

    def test_size_after_pushes(self):
        s = Stack()
        for i in range(5):
            s.push(i)
        self.assertEqual(s.size(), 5)

    def test_size_after_pop(self):
        s = Stack()
        s.push(10)
        s.push(20)
        s.pop()
        self.assertEqual(s.size(), 1)


# =============================================================================
# 2.  Expression Evaluator — basic arithmetic
# =============================================================================

class TestBasicArithmetic(unittest.TestCase):
    """Tests for the four basic operators."""

    def test_addition(self):
        self.assertEqual(evaluate_expression("3 + 5"), "8")

    def test_subtraction(self):
        self.assertEqual(evaluate_expression("10 - 4"), "6")

    def test_multiplication(self):
        self.assertEqual(evaluate_expression("6 * 7"), "42")

    def test_integer_division(self):
        self.assertEqual(evaluate_expression("8 / 4"), "2")

    def test_non_integer_division(self):
        # 7 / 2 = 3.5
        self.assertEqual(evaluate_expression("7 / 2"), "3.5")

    def test_single_number(self):
        self.assertEqual(evaluate_expression("42"), "42")


# =============================================================================
# 3.  Operator Precedence
# =============================================================================

class TestOperatorPrecedence(unittest.TestCase):
    """* and / must be evaluated before + and -."""

    def test_multiply_before_add(self):
        # 3 + 5 * 2  →  3 + 10  =  13
        self.assertEqual(evaluate_expression("3 + 5 * 2"), "13")

    def test_divide_before_subtract(self):
        # 10 - 8 / 4  →  10 - 2  =  8
        self.assertEqual(evaluate_expression("10 - 8 / 4"), "8")

    def test_mixed_precedence(self):
        # 2 + 3 * 4 - 1  →  2 + 12 - 1  =  13
        self.assertEqual(evaluate_expression("2 + 3 * 4 - 1"), "13")

    def test_left_to_right_same_precedence(self):
        # 10 - 3 - 2  →  7 - 2  =  5
        self.assertEqual(evaluate_expression("10 - 3 - 2"), "5")

    def test_multiply_and_divide_left_to_right(self):
        # 8 / 4 * 2  →  2 * 2  =  4
        self.assertEqual(evaluate_expression("8 / 4 * 2"), "4")


# =============================================================================
# 4.  Parentheses
# =============================================================================

class TestParentheses(unittest.TestCase):
    """Parentheses must override the default precedence."""

    def test_parentheses_override_precedence(self):
        # (3 + 5) * 2  →  8 * 2  =  16
        self.assertEqual(evaluate_expression("(3 + 5) * 2"), "16")

    def test_nested_parentheses(self):
        # ((2 + 3) * (4 - 1)) / 5  →  (5 * 3) / 5  =  15 / 5  =  3
        self.assertEqual(evaluate_expression("((2 + 3) * (4 - 1)) / 5"), "3")

    def test_parentheses_in_denominator(self):
        # 8 / (4 + 4)  →  8 / 8  =  1
        self.assertEqual(evaluate_expression("8 / (4 + 4)"), "1")

    def test_assignment_example_1(self):
        # From assignment input.txt:  3 + 5 * 2  =  13
        self.assertEqual(evaluate_expression("3 + 5 * 2"), "13")

    def test_assignment_example_2(self):
        # From assignment input.txt:  (8 / 4) + 7 * 2  →  2 + 14  =  16
        self.assertEqual(evaluate_expression("(8 / 4) + 7 * 2"), "16")

    def test_assignment_example_3(self):
        # From assignment input.txt:  10 - (2 + 3) * 4  →  10 - 20  =  -10
        self.assertEqual(evaluate_expression("10 - (2 + 3) * 4"), "-10")

    def test_parentheses_around_whole_expression(self):
        # (5 + 3)  =  8
        self.assertEqual(evaluate_expression("(5 + 3)"), "8")


# =============================================================================
# 5.  Unary Minus (Negative Numbers)
# =============================================================================

class TestUnaryMinus(unittest.TestCase):

    def test_negative_first_operand(self):
        # -5 + 10  =  5
        self.assertEqual(evaluate_expression("-5 + 10"), "5")

    def test_negative_result(self):
        # 3 - 8  =  -5
        self.assertEqual(evaluate_expression("3 - 8"), "-5")

    def test_expression_resulting_in_negative(self):
        # 10 - (2 + 3) * 4  =  -10
        self.assertEqual(evaluate_expression("10 - (2 + 3) * 4"), "-10")


# =============================================================================
# 6.  Complex Expressions
# =============================================================================

class TestComplexExpressions(unittest.TestCase):

    def test_multi_operator_chain(self):
        # 100 / 5 + 3 * 2  →  20 + 6  =  26
        self.assertEqual(evaluate_expression("100 / 5 + 3 * 2"), "26")

    def test_mixed_parens_and_precedence(self):
        # (10 + 2) * 3 - 6 / 2  →  36 - 3  =  33
        self.assertEqual(evaluate_expression("(10 + 2) * 3 - 6 / 2"), "33")

    def test_nested_parens_with_division(self):
        # 50 / (5 * 2) + 3  →  50 / 10 + 3  →  5 + 3  =  8
        self.assertEqual(evaluate_expression("50 / (5 * 2) + 3"), "8")

    def test_three_level_nesting(self):
        # ((3 + 2) * 2) + 1  →  (5 * 2) + 1  =  11
        self.assertEqual(evaluate_expression("((3 + 2) * 2) + 1"), "11")

    def test_longer_expression(self):
        # 15 - 3 * 2 + 8 / 4  →  15 - 6 + 2  =  11
        self.assertEqual(evaluate_expression("15 - 3 * 2 + 8 / 4"), "11")


# =============================================================================
# 7.  Error Handling
# =============================================================================

class TestErrorHandling(unittest.TestCase):

    def test_division_by_zero(self):
        result = evaluate_expression("5 / 0")
        self.assertTrue(result.startswith("ERROR:"))

    def test_division_by_zero_expression(self):
        result = evaluate_expression("10 / (5 - 5)")
        self.assertTrue(result.startswith("ERROR:"))

    def test_invalid_character(self):
        result = evaluate_expression("3 @ 5")
        self.assertTrue(result.startswith("ERROR:"))

    def test_mismatched_open_paren(self):
        result = evaluate_expression("(3 + 5")
        self.assertTrue(result.startswith("ERROR:"))

    def test_mismatched_close_paren(self):
        result = evaluate_expression("3 + 5)")
        self.assertTrue(result.startswith("ERROR:"))

    def test_empty_expression(self):
        result = evaluate_expression("")
        self.assertTrue(result.startswith("ERROR:"))

    def test_whitespace_only(self):
        result = evaluate_expression("   ")
        self.assertTrue(result.startswith("ERROR:"))

    def test_missing_operand_infix(self):
        self.assertTrue(evaluate_expression("5 +").startswith("ERROR:"))

    def test_excess_operand_infix(self):
        self.assertTrue(evaluate_expression("2 2 +").startswith("ERROR:"))

    def test_decimal_input_supported(self):
        self.assertEqual(evaluate_expression("2.5 + 1.5"), "4")

    def test_repeated_decimal_or_bad_number(self):
        self.assertTrue(evaluate_expression("1..2 + 3").startswith("ERROR:"))


# =============================================================================
# 8.  File Processing (process_expressions)
# =============================================================================

class TestFileProcessing(unittest.TestCase):

    def test_separator_preserved(self):
        items = ["3 + 5", "-----", "10 - 2"]
        results = process_expressions(items)
        self.assertEqual(results[1], "-----")

    def test_correct_result_count(self):
        items = ["3 + 5", "-----", "10 - 2"]
        results = process_expressions(items)
        self.assertEqual(len(results), 3)

    def test_expression_evaluated(self):
        items = ["3 + 5"]
        results = process_expressions(items)
        self.assertEqual(results[0], "8")

    def test_multiple_expressions_with_separators(self):
        items = ["3 + 5 * 2", "-----", "(8 / 4) + 7 * 2", "-----", "10 - (2 + 3) * 4"]
        results = process_expressions(items)
        self.assertEqual(results[0], "13")
        self.assertEqual(results[1], "-----")
        self.assertEqual(results[2], "16")
        self.assertEqual(results[3], "-----")
        self.assertEqual(results[4], "-10")

    def test_blank_lines_preserved(self):
        items = ["3 + 2", ""]
        results = process_expressions(items)
        self.assertEqual(results[1], "")


# =============================================================================
# Run all tests
# =============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
