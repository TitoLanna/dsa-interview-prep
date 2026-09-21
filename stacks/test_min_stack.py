import importlib.util
import os

import pytest

_MODULE_PATH = os.path.join(os.path.dirname(__file__), "Min Stack.py")
_spec = importlib.util.spec_from_file_location("min_stack", _MODULE_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
MinStack = _module.MinStack


def test_push_top_getmin_single_element():
    stack = MinStack()
    stack.push(5)
    assert stack.top() == 5
    assert stack.getMin() == 5


def test_getmin_tracks_new_minimum():
    stack = MinStack()
    stack.push(5)
    stack.push(3)
    assert stack.getMin() == 3
    stack.push(7)
    assert stack.getMin() == 3
    stack.push(2)
    assert stack.getMin() == 2


def test_pop_restores_previous_minimum():
    stack = MinStack()
    stack.push(-2)
    stack.push(0)
    stack.push(-3)
    assert stack.getMin() == -3
    stack.pop()
    assert stack.top() == 0
    assert stack.getMin() == -2


def test_pop_updates_top():
    stack = MinStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.pop()
    assert stack.top() == 2
    stack.pop()
    assert stack.top() == 1


def test_duplicate_minimums():
    stack = MinStack()
    stack.push(1)
    stack.push(1)
    stack.push(0)
    stack.push(1)
    assert stack.getMin() == 0
    stack.pop()
    assert stack.getMin() == 0
    stack.pop()
    assert stack.getMin() == 1
    stack.pop()
    assert stack.getMin() == 1


def test_leetcode_example():
    stack = MinStack()
    stack.push(-2)
    stack.push(0)
    stack.push(-3)
    assert stack.getMin() == -3
    stack.pop()
    assert stack.top() == 0
    assert stack.getMin() == -2
