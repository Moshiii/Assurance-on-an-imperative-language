import unittest
from a2q3.verbal_arithmetic import solve

class PuzzleTests (unittest.TestCase):

    def setUp (self):
        """Reset Z3 context between tests"""
        import z3
        z3._main_ctx = None
    def tearDown (self):
        """Reset Z3 context after test"""
        import z3
        z3._main_ctx = None
        
    def test_1 (self):
        """SEND + MORE = MONEY"""
        res = solve ('SEND', 'MORE', 'MONEY')
        self.assertEquals (res, [9567, 1085, 10652])

    def test_2 (self):
        """SEND + ORRE = MONEY"""
        res = solve ('SEND', 'ORRE', 'MONEY')
        self.assertEquals (res, None)

    def test_3 (self):
        """PLAYS + WELL = BETTER"""
        res = solve ('PLAYS', 'WELL', 'BETTER')
        self.assertEquals (res, [97426, 8077, 105503])
    
    def test_4 (self):
        """CRACK + HACK = ERROR"""
        res = solve ('CRACK', 'HACK', 'ERROR')
        self.assertEquals (res, [42641, 9641, 52282])
        
