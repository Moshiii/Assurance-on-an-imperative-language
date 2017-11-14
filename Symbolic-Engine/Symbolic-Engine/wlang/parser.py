#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.buffering import Buffer
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


__all__ = [
    'WhileLangParser',
    'WhileLangSemantics',
    'main'
]

KEYWORDS = {}


class WhileLangBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re='#[^\\r\\n]*',
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(WhileLangBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class WhileLangParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re='#[^\\r\\n]*',
        ignorecase=None,
        left_recursion=False,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=WhileLangBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(WhileLangParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @graken()
    def _start_(self):
        self._stmt_list_()

    @graken()
    def _stmt_list_(self):

        def sep0():
            self._token(';')

        def block0():
            self._stmt_()
        self._positive_closure(block0, sep=sep0)

    @graken()
    def _stmt_(self):
        with self._choice():
            with self._option():
                self._skip_stmt_()
            with self._option():
                self._asgn_stmt_()
            with self._option():
                self._block_stmt_()
            with self._option():
                self._if_stmt_()
            with self._option():
                self._while_stmt_()
            with self._option():
                self._assert_stmt_()
            with self._option():
                self._assume_stmt_()
            with self._option():
                self._havoc_stmt_()
            with self._option():
                self._print_state_stmt_()
            self._error('no available options')

    @graken()
    def _asgn_stmt_(self):
        self._name_()
        self.name_last_node('lhs')
        self._token(':=')
        self._aexp_()
        self.name_last_node('rhs')
        self.ast._define(
            ['lhs', 'rhs'],
            []
        )

    @graken()
    def _block_stmt_(self):
        self._token('{')
        self._stmt_list_()
        self.name_last_node('@')
        self._token('}')

    @graken()
    def _skip_stmt_(self):
        self._token('skip')

    @graken()
    def _print_state_stmt_(self):
        self._token('print_state')

    @graken()
    def _if_stmt_(self):
        self._token('if')
        self._cut()
        self._bexp_()
        self.name_last_node('cond')
        self._token('then')
        self._stmt_()
        self.name_last_node('then_stmt')
        with self._optional():
            self._token('else')
            self._stmt_()
            self.name_last_node('else_stmt')
        self.ast._define(
            ['cond', 'else_stmt', 'then_stmt'],
            []
        )

    @graken()
    def _while_stmt_(self):
        self._token('while')
        self._bexp_()
        self.name_last_node('cond')
        with self._optional():
            self._token('inv')
            self._bexp_()
            self.name_last_node('inv')
        self._token('do')
        self._stmt_()
        self.name_last_node('body')
        self.ast._define(
            ['body', 'cond', 'inv'],
            []
        )

    @graken()
    def _assert_stmt_(self):
        self._token('assert')
        self._bexp_()
        self.name_last_node('cond')
        self.ast._define(
            ['cond'],
            []
        )

    @graken()
    def _assume_stmt_(self):
        self._token('assume')
        self._bexp_()
        self.name_last_node('cond')
        self.ast._define(
            ['cond'],
            []
        )

    @graken()
    def _havoc_stmt_(self):
        self._token('havoc')
        self._var_list_()
        self.name_last_node('vars')
        self.ast._define(
            ['vars'],
            []
        )

    @graken()
    def _var_list_(self):

        def sep0():
            self._token(',')

        def block0():
            self._name_()
        self._positive_closure(block0, sep=sep0)

    @graken()
    def _bexp_(self):

        def sep0():
            with self._group():
                self._token('or')
                self.name_last_node('op')

        def block0():
            self._bterm_()
            self.name_last_node('args')
        self._positive_closure(block0, sep=sep0)
        self.ast._define(
            ['args'],
            []
        )

    @graken()
    def _bterm_(self):

        def sep0():
            with self._group():
                self._token('and')
                self.name_last_node('op')

        def block0():
            self._bfactor_()
            self.name_last_node('args')
        self._positive_closure(block0, sep=sep0)
        self.ast._define(
            ['args'],
            []
        )

    @graken()
    def _bfactor_(self):
        with self._choice():
            with self._option():
                self._batom_()
                self.name_last_node('arg')
            with self._option():
                self._token('not')
                self.name_last_node('op')
                self._cut()
                self._batom_()
                self.name_last_node('arg')
            self._error('no available options')
        self.ast._define(
            ['arg', 'op'],
            []
        )

    @graken()
    def _batom_(self):
        with self._choice():
            with self._option():
                self._rexp_()
            with self._option():
                self._bool_const_()
            with self._option():
                self._token('(')
                self._bexp_()
                self.name_last_node('@')
                self._token(')')
            self._error('no available options')

    @graken()
    def _bool_const_(self):
        with self._choice():
            with self._option():
                self._token('true')
            with self._option():
                self._token('false')
            self._error('expecting one of: false true')

    @graken()
    def _rexp_(self):
        self._aexp_()
        self.name_last_node('lhs')
        self._rop_()
        self.name_last_node('op')
        self._cut()
        self._aexp_()
        self.name_last_node('rhs')
        self.ast._define(
            ['lhs', 'op', 'rhs'],
            []
        )

    @graken()
    def _rop_(self):
        with self._choice():
            with self._option():
                self._token('<=')
            with self._option():
                self._token('<')
            with self._option():
                self._token('=')
            with self._option():
                self._token('>=')
            with self._option():
                self._token('>')
            self._error('expecting one of: < <= = > >=')

    @graken()
    def _aexp_(self):
        with self._choice():
            with self._option():
                self._addition_()
            with self._option():
                self._subtraction_()
            with self._option():
                self._term_()
            self._error('no available options')

    @graken()
    def _addition_(self):
        self._term_()
        self.name_last_node('lhs')
        self._token('+')
        self.name_last_node('op')
        self._cut()
        self._aexp_()
        self.name_last_node('rhs')
        self.ast._define(
            ['lhs', 'op', 'rhs'],
            []
        )

    @graken()
    def _subtraction_(self):
        self._term_()
        self.name_last_node('lhs')
        self._token('-')
        self.name_last_node('op')
        self._cut()
        self._aexp_()
        self.name_last_node('rhs')
        self.ast._define(
            ['lhs', 'op', 'rhs'],
            []
        )

    @graken()
    def _term_(self):
        with self._choice():
            with self._option():
                self._mult_()
            with self._option():
                self._division_()
            with self._option():
                self._factor_()
            self._error('no available options')

    @graken()
    def _mult_(self):
        self._factor_()
        self.name_last_node('lhs')
        self._token('*')
        self.name_last_node('op')
        self._cut()
        self._term_()
        self.name_last_node('rhs')
        self.ast._define(
            ['lhs', 'op', 'rhs'],
            []
        )

    @graken()
    def _division_(self):
        self._factor_()
        self.name_last_node('lhs')
        self._token('/')
        self.name_last_node('op')
        self._cut()
        self._term_()
        self.name_last_node('rhs')
        self.ast._define(
            ['lhs', 'op', 'rhs'],
            []
        )

    @graken()
    def _factor_(self):
        with self._choice():
            with self._option():
                self._atom_()
            with self._option():
                self._neg_number_()
            with self._option():
                self._token('(')
                self._aexp_()
                self.name_last_node('@')
                self._token(')')
            self._error('no available options')

    @graken()
    def _neg_number_(self):
        self._token('-')
        self._cut()
        self._number_()
        self.name_last_node('@')

    @graken()
    def _atom_(self):
        with self._choice():
            with self._option():
                self._name_()
            with self._option():
                self._number_()
            self._error('no available options')

    @graken()
    def _name_(self):
        self._NAME_()

    @graken()
    def _number_(self):
        self._INT_()

    @graken()
    def _INT_(self):
        self._pattern(r'0[xX][0-9a-fA-F]+|[0-9]+')

    @graken()
    def _NAME_(self):
        self._pattern(r'(?!\d)\w+')

    @graken()
    def _NEWLINE_(self):
        self._pattern(r'[\u000C\r\n]+')
        self._cut()


class WhileLangSemantics(object):
    def start(self, ast):
        return ast

    def stmt_list(self, ast):
        return ast

    def stmt(self, ast):
        return ast

    def asgn_stmt(self, ast):
        return ast

    def block_stmt(self, ast):
        return ast

    def skip_stmt(self, ast):
        return ast

    def print_state_stmt(self, ast):
        return ast

    def if_stmt(self, ast):
        return ast

    def while_stmt(self, ast):
        return ast

    def assert_stmt(self, ast):
        return ast

    def assume_stmt(self, ast):
        return ast

    def havoc_stmt(self, ast):
        return ast

    def var_list(self, ast):
        return ast

    def bexp(self, ast):
        return ast

    def bterm(self, ast):
        return ast

    def bfactor(self, ast):
        return ast

    def batom(self, ast):
        return ast

    def bool_const(self, ast):
        return ast

    def rexp(self, ast):
        return ast

    def rop(self, ast):
        return ast

    def aexp(self, ast):
        return ast

    def addition(self, ast):
        return ast

    def subtraction(self, ast):
        return ast

    def term(self, ast):
        return ast

    def mult(self, ast):
        return ast

    def division(self, ast):
        return ast

    def factor(self, ast):
        return ast

    def neg_number(self, ast):
        return ast

    def atom(self, ast):
        return ast

    def name(self, ast):
        return ast

    def number(self, ast):
        return ast

    def INT(self, ast):
        return ast

    def NAME(self, ast):
        return ast

    def NEWLINE(self, ast):
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = WhileLangParser(parseinfo=False)
    return parser.parse(text, startrule, filename=filename, **kwargs)

if __name__ == '__main__':
    import json
    ast = generic_main(main, WhileLangParser, name='WhileLang')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()
