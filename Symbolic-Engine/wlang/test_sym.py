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

import unittest
import wlang.ast as ast
import wlang.sym



class TestSym (unittest.TestCase):
    def test_one (self):
        prg1 = "havoc x; assume x > 10;assert x > 15"         
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        print('test1\n')
        print(out)  
        self.assertEquals (len(out), 1)

    def test_two (self):
			prg1 = "havoc x; if true then x:=x+1;x:=x-1;x:=x*1;x:=x/1"         
			ast1 = ast.parse_string (prg1)
			sym = wlang.sym.SymExec ()
			st = wlang.sym.SymState ()
			out = [s for s in sym.run (ast1, st)]
			print('test2\n')
			print(out)
			self.assertEquals (len(out), 1)


    def test_three (self):
      prg1 = "havoc x,y;if x < 8 then y:=2;print_state"         
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('test3\n')  
      print(out)
      self.assertEquals (len(out), 2)

    def test_four (self):
      prg1 = "havoc x;if x > 5 then x:=x+1;while x < 10 and x>-1 do x:=x+1"         
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('test4\n') 
      print(out)  
      self.assertEquals (len(out), 11)

    def test_five (self):
      prg1 = "havoc x; if x<8 or x>10 then x:=x+1 else x:=x-1;if not x>0 then x:=x+1;if x>5 then x:=10;skip" 
      # if x<5 then x:=x+5        # 
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('test5\n')
      print(out)
      self.assertEquals (len(out), 4)
         

    def test_six (self):
      prg1 = "havoc x; while x >-11 and x<0 do x:=x+1"         
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('test6\n')
      print(out)
      self.assertEquals (len(out), 11)

    def test_seven (self):
      prg1 = "havoc x;assert x>5;while x < 10 and x>-1 do x:=x+1"         
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('test4\n') 
      print(out)  
      self.assertEquals (len(out), 5)

   #  

    def test_eight (self):
      prg1 = "havoc x,y,z;if x>10 then {if x>5 then x:=10}"         
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('testProgram\n')
      print(out)      
    
        
    def test_nine (self):
      prg1 = "havoc x,r; assume x>10;assert x<0"         
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('test9\n')
      print(out)
      self.assertEquals (len(out), 0)

    # def test_program1 (self):
    #   prg1 = "havoc x,y,z;while x>-1 and x<10 do {y:=y;while y < 10 and x>-1 do y:=y+1;x:=x+1}"         
    #   ast1 = ast.parse_string (prg1)
    #   sym = wlang.sym.SymExec ()
    #   st = wlang.sym.SymState ()
    #   out = [s for s in sym.run (ast1, st)]
    #   print('testProgram1\n')
    #   print(out) 
    #   self.assertEquals (len(out), 13)


    def test_program2 (self):
      prg1 = "havoc x,y,z;if x>10 then {if x<20 then {if x>15 then {while x < 20 and x>9 do x:=x+1}}};while x < 25 and x>14 do x:=x+1"         
      ast1 = ast.parse_string (prg1)
      sym = wlang.sym.SymExec ()
      st = wlang.sym.SymState ()
      out = [s for s in sym.run (ast1, st)]
      print('testProgram2\n')
      print(out) 
      self.assertEquals (len(out), 13)






        
