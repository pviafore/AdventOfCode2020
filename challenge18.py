import operator as op

from dataclasses import dataclass
from typing import Callable, Optional, Union

import common.input_data as input_data

def get_sum_of_equations(equations: list[str], add_precedence: bool = False) -> int:
    if add_precedence:
        return sum(evaluate_equation_with_add_precedence(eq) for eq in equations)
    return sum(evaluate_equation(eq) for eq in equations)

Value = Union[Callable,int]
@dataclass
class EquationTree:
    value: Value
    left: Optional['EquationTree']= None
    right: Optional['EquationTree'] = None

    def compute(self) -> int:
        if self.value is op.add:
            assert self.left is not None and self.right is not None
            return self.left.compute() + self.right.compute()
        if self.value is op.mul:
            assert self.left is not None and self.right is not None
            return self.left.compute() * self.right.compute()
        assert isinstance(self.value, int)
        return self.value

    def get_rightmost_tree_with_empty_right(self) -> 'EquationTree':
        if self.right is None:
            return self
        return self.right.get_rightmost_tree_with_empty_right()


def evaluate_equation_with_add_precedence(equation: str) -> int:
    tree: Optional[EquationTree] = None
    tree_stack: list[Optional[EquationTree]] = []
    for char in equation:
        if char in '0123456789':
            value_tree = EquationTree(int(char))
            if tree is not None:
                tree.get_rightmost_tree_with_empty_right().right = value_tree
            else:
                tree = value_tree
        if char == '+':
            if tree is not None and tree.right is not None:
                new_tree = EquationTree(op.add, tree.right)
                tree.right = new_tree
            else:
                tree = EquationTree(op.add, tree)
        if char == '*':
            tree = EquationTree(op.mul, tree)
        if char == '(':
            tree_stack.append(tree)
            tree = None
        if char == ')':
            assert tree is not None
            value = tree.compute()
            parent_tree = tree_stack.pop()
            if parent_tree is not None:
                parent_tree.get_rightmost_tree_with_empty_right().right = EquationTree(value)
                tree = parent_tree
            else:
                tree = EquationTree(value)
    assert tree is not None
    return tree.compute()

def evaluate_equation(equation: str)  -> int:
    value = 1
    op_func = op.mul
    value_stack: list[tuple[int, Callable]] = []
    for char in equation:
        if char in '0123456789':
            value = op_func(value, int(char))
        elif char == '(':
            value_stack.append((value, op_func))
            value = 1
            op_func = op.mul
        elif char == ')':
            last_val, last_func = value_stack.pop()
            value = last_func(last_val, value)
        elif char == '+':
            op_func = op.add
        elif char == '*':
            op_func = op.mul
    return value

def to_equation(data: str) -> str:
    return data.replace(" ", "")

EQUATIONS = input_data.read("input/input18.txt", to_equation)

if __name__ == "__main__":
    print(get_sum_of_equations(EQUATIONS))
    print(get_sum_of_equations(EQUATIONS, True))
