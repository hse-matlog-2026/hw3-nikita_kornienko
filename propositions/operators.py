# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """
    substitution_map = {
        '+': Formula.parse('((p&~q)|(~p&q))'),
        '->': Formula.parse('(~p|q)'),
        '<->': Formula.parse('((p&q)|(~p&~q))'),
        '-&': Formula.parse('~(p&q)'),
        '-|': Formula.parse('~(p|q)'),
        'T': Formula.parse('(p|~p)'),
        'F': Formula.parse('(p&~p)')
    }
    return formula.substitute_operators(substitution_map)
    # Task 3.5

def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """
    substitution_map = {
        '|': Formula.parse('~(~p&~q)'),
        '->': Formula.parse('~(p&~q)'),
        '+': Formula.parse('~(~(p&~q)&~(~p&q))'),
        '<->': Formula.parse('(~(p&~q)&~(~p&q))'),
        '-&': Formula.parse('~(p&q)'),
        '-|': Formula.parse('(~p&~q)'),
        'T': Formula.parse('~(p&~p)'),
        'F': Formula.parse('(p&~p)')
    }
    return formula.substitute_operators(substitution_map)
    # Task 3.6a

def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """
    p = Formula('p')
    q = Formula('q')

    # Вспомогательные формулы для удобства
    not_p = Formula('-&', p, p)
    not_q = Formula('-&', q, q)
    p_and_q = Formula('-&', Formula('-&', p, q), Formula('-&', p, q))

    substitution_map = {
        '~': not_p,
        '&': p_and_q,
        '|': Formula('-&', not_p, not_q),
        '->': Formula('-&', p, not_q),
        'T': Formula('-&', not_p, p),  # p NAND ~p всегда True
        'F': Formula('-&', Formula('-&', not_p, p), Formula('-&', not_p, p)),  # ~(T) всегда False
        '+': Formula('-&',
                     Formula('-&', not_p, q),
                     Formula('-&', p, not_q)),  # (p | q) & ~(p & q) в NAND-виде
        '<->': Formula('-&',
                       Formula('-&', p, q),
                       Formula('-&', not_p, not_q)),
        '-&': Formula('-&', p, q),
        '-|': Formula('-&', Formula('-&', not_p, not_q), Formula('-&', not_p, not_q))
    }

    return formula.substitute_operators(substitution_map)
    # Task 3.6b

def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """
    substitution_map = {
        '~': Formula.parse('~p'),
        '->': Formula.parse('(p->q)'),
        '|': Formula.parse('(~p->q)'),
        '&': Formula.parse('~(p->~q)'),
        # (p <-> q) эквивалентно (p->q) & (q->p), в базисе {->, ~} это:
        '<->': Formula.parse('~((p->q)->~(q->p))'),
        # (p + q) эквивалентно ~(p <-> q)
        '+': Formula.parse('((p->q)->~(q->p))'),
        '-&': Formula.parse('(p->~q)'),
        '-|': Formula.parse('~(~p->q)'),
        # T и F должны быть корректными тавтологией и противоречием
        'T': Formula.parse('(p->p)'),
        'F': Formula.parse('~(p->p)')
    }
    return formula.substitute_operators(substitution_map)
    # Task 3.6c

def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """
    substitution_map = {
        'F': Formula.parse('F'),
        '->': Formula.parse('(p->q)'),
        '~': Formula.parse('(p->F)'),
        'T': Formula.parse('(F->F)'),
        '|': Formula.parse('((p->F)->q)'),
        '&': Formula.parse('((p->(q->F))->F)'),
        '-&': Formula.parse('(p->(q->F))'),
        '-|': Formula.parse('(((p->F)->q)->F)'),
        # (p <-> q) выражается через (p->q) & (q->p)
        '<->': Formula.parse('(((p->q)->((q->p)->F))->F)'),
        # (p + q) выражается через ~(p <-> q)
        '+': Formula.parse('((p->q)->((q->p)->F))')
    }
    return formula.substitute_operators(substitution_map)
    # Task 3.6d
