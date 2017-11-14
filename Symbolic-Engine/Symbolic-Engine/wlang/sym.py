# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import wlang.ast
import cStringIO
import sys

import z3
import copy

class SymState(object):
    def __init__(self, solver = None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list ()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver ()

        # true if this is an error state
        self._is_error = False

    def add_pc (self, *exp):
        """Add constraints to the path condition"""
        self.path.extend (exp)
        self._solver.append (exp)
        
    def is_error (self):
        return self._is_error
    def mk_error (self):
        self._is_error = True
        
    def is_empty (self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check ()
        return res == z3.unsat

    def pick_concerete (self):
        """Pick a concrete state consistent with the symbolic state.
           Return None if no such state exists"""
        res = self._solver.check ()
        if res <> z3.sat:
            return None
        model = self._solver.model ()
        import wlang.int
        st = wlang.int.State ()
        for (k, v) in self.env.items():
            st.env [k] = model.eval (v)
        return st
        
    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState ()
        child.env = dict(self.env)
        child.add_pc (*self.path)
        
        return (self, child)
    
    def __repr__ (self):
        return str(self)
        
    def to_smt2 (self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2 ()
    
        
    def __str__ (self):
        buf = cStringIO.StringIO ()
        for k, v in self.env.iteritems():
            buf.write (str (k))
            buf.write (': ')
            buf.write (str (v))
            buf.write ('\n')
        buf.write ('pc: ')
        buf.write (str (self.path))
        buf.write ('\n')
            
        return buf.getvalue ()
                   
class SymExec (wlang.ast.AstVisitor):
    def __init__(self):
        self.dc=list()
        self.copydc=list()
        pass        

    def run (self, ast, state):
        ## set things up and 
        ## call self.visit (ast, state=state)   
        self.visit (ast, state=state)
        
        states=list()
        for s in self.dc:
            p=s.is_empty()
            if p:
                # s.mk_error()
                pass
            else:
            	st=s.pick_concerete()
                st=s.to_smt2
            	# print('%s is one of the concrete result for the current path %s'%(st,s))
                states.append(s)
        return states

    def visit_IntVar (self, node, *args, **kwargs):
        return kwargs['state'].env [node.name]
    
    def visit_BoolConst(self, node, *args, **kwargs):
        return z3.BoolVal (node.val)

    def visit_IntConst (self, node, *args, **kwargs):
        return z3.IntVal (node.val)
    
    def visit_RelExp (self, node, *args, **kwargs):
        lhs = self.visit (node.arg (0), *args, **kwargs)
        rhs = self.visit (node.arg (1), *args, **kwargs)

        st=kwargs['state']

        if node.op == '<=': return lhs <= rhs
        if node.op == '<': return lhs < rhs
        if node.op == '=': return lhs == rhs
        if node.op == '>=': return lhs >= rhs
        if node.op == '>': return lhs > rhs
        

    def visit_BExp (self, node, *args, **kwargs):
        kids = [self.visit (a, *args, **kwargs) for a in node.args]
        
        if node.op == 'not':
            assert node.is_unary ()
            assert len (kids) == 1
            return z3.Not(kids[0]) 
        
        fn = None
        base = None
        if node.op == 'and':
            fn = lambda x, y : z3.And(x,y)
            base = True
        elif node.op == 'or':
            fn = lambda x, y : z3.Or(x,y)
            base = False

        assert fn is not None
        return reduce (fn, kids, base)
        
    def visit_AExp (self, node, *args, **kwargs):
        kids = [self.visit (a, *args, **kwargs) for a in node.args]

        fn = None
        base = None

        if node.op == '+':
            fn = lambda x, y: x + y
            
        elif node.op == '-':
            fn = lambda x, y: x - y

        elif node.op == '*':
            fn = lambda x, y: x * y

        elif node.op == '/':
            fn = lambda x, y : x / y
            
        
        assert fn is not None
        return reduce (fn, kids)
        
    def visit_SkipStmt (self, node, *args, **kwargs):
        return kwargs['state']
    
    def visit_PrintStateStmt (self, node, *args, **kwargs):
        print (kwargs['state'])
        return kwargs['state']

    def visit_AsgnStmt (self, node, *args, **kwargs):
        st = kwargs['state']       
        st.env [node.lhs.name] = self.visit (node.rhs, *args, **kwargs)
        return st

    def visit_IfStmt (self, node, *args, **kwargs):
        st = kwargs['state']  #symbolic from havoc

        # tempdc=list()
        # tempdc1=list()
        # for s in self.dc:
        x=0
        y=len(self.dc)
        while x<y:
            s=self.dc[x]                
            if s._solver.check()==z3.sat: 
                fork1=s.fork() 

                kwargs['state'] = s
                cond = self.visit (node.cond, *args, **kwargs)

                fork1[0].add_pc(cond)
                fork1[1].add_pc(z3.Not(cond)) 

                if fork1[0]._solver.check()==z3.sat: 
                    # tempdc.append(fork1[0])
                    # tempdc1.append(fork1[0])
                    # self.dc.append(fork1[1])              
                    kwargs['state'] = fork1[0] 
                    self.visit (node.then_stmt, *args, **kwargs)               
                else:
                    fork1[0].mk_error()

                if fork1[1]._solver.check()==z3.sat: 
                    # tempdc.append(fork1[1])
                    # tempdc1.append(fork1[1])
                    self.dc.append(fork1[1])
                    if node.has_else ():               
                        kwargs['state'] = fork1[1]
                        self.visit (node.else_stmt, *args, **kwargs)
                else:
                    fork1[1].mk_error()
            x=x+1
        # self.dc=list()
        # self.dc=tempdc
        # self.copydc=list()
        # self.copydc=tempdc1        
        return kwargs['state']

    

    def visit_WhileStmt (self, node, *args, **kwargs):
        st = kwargs['state']
        
        x=0
        y=len(self.dc)
        while x<y:
        # len(self.dc)               
        # for v in self.dc:
            v=self.dc[x]
            if v._solver.check()==z3.sat:
                forkp=v.fork()

                kwargs['state']=v
                cond = self.visit (node.cond, *args, **kwargs)

                forkp[0].add_pc(cond)
                forkp[1].add_pc(z3.Not(cond))

                if forkp[0]._solver.check()==z3.sat:
                    kwargs['state']=forkp[0]
                    # execute the body       
                    st = self.visit (node.body, *args, **kwargs)
                    # execute the loop again
                    kwargs['state'] = st
                    self.visit (node, *args, **kwargs)
                else:
                    forkp[0].mk_error()
                
                if forkp[1]._solver.check()==z3.sat:
                    kwargs['state']=forkp[1]
                    self.dc.append(forkp[1])
                else:
                    forkp[1].mk_error()
            x=x+1
        # self.dc=list()
        # self.dc=tempdc
        # print(self.dc)
        return kwargs['state']
        

    def visit_AssertStmt (self, node, *args, **kwargs):
        ## Don't forget to print an error message if an assertion might be violated
        st = kwargs['state']
        cond = self.visit (node.cond, *args, **kwargs)
         		
        tempdc=list()
        tempdc1=list()
        for s in self.dc:
            if s._solver.check()==z3.sat:
                forkl=s.fork() 
                kwargs['state']=s
                cond = self.visit (node.cond, *args, **kwargs)
                forkl[0].add_pc(cond)
                            
                if forkl[0].is_empty():
                    print ('Assertion error for states:')
                    print(forkl[0])  
                    # return kwargs['state'] 
                else:
                    tempdc.append(forkl[0])            
                    tempdc1.append(forkl[0])
        self.dc=list()
        self.dc=tempdc
        self.copydc=list()
        self.copydc=tempdc1
        return st


    def visit_AssumeStmt (self, node, *args, **kwargs):	
        return self.visit_AssertStmt (node, *args, **kwargs)

    def visit_HavocStmt (self, node, *args, **kwargs):
       	st = kwargs['state']

        for v in node.vars:
            st.env [v.name] = z3.Int(str(v.name))
        
        forkhavoc=st.fork()
        self.dc.append(forkhavoc[1])
        self.copydc.append(forkhavoc[1])
        # self.empty.append(forkhavoc[1])
        return st

    def visit_StmtList (self, node, *args, **kwargs):
        st = kwargs['state']

        nkwargs = dict (kwargs)
        for stmt in node.stmts:
            nkwargs ['state'] = st
            st = self.visit (stmt, *args, **nkwargs)
        return st
        
def _parse_args ():
    import argparse
    ap = argparse.ArgumentParser (prog='sym',
                                  description='WLang Interpreter')
    ap.add_argument ('in_file', metavar='FILE', help='WLang program to interpret')
    args = ap.parse_args ()
    return args
    
def main ():
    args = _parse_args ()
    ast = wlang.ast.parse_file (args.in_file)
    st = SymState ()
    sym = SymExec ()

    states = sym.run (ast, st)
    if states is None:
        print ('[symexec]: no output states')
    else:
        count = 0
        for out in states:
            count = count + 1
            print ('[symexec]: symbolic state reached')
            print (out)
        print ('[symexec]: found', count, 'symbolic states')
    return 0

if __name__ == '__main__':
    sys.exit (main ())
                    
