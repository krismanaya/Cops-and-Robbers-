import unittest
import copsandrobbers as cr

class Testcopsandrobbers(unittest.TestCase):
    def setUp(self):
        self.g = cr.graph()
        self.g.m = {1: {2, 3},
            2: {1, 4},
            3: {1},
            4: {2}}

    def tearDown(self):
        pass

    def testdisconnectedgraph(self): 
        g = cr.makedisconnected(2)
        self.assertEqual({0, 1}, g.getvertices())
        self.assertEqual(set(), g.getedges())

    def testcreatepath(self): 
        g = cr.makepath(3)
        self.assertEqual({0, 1, 2}, g.getvertices())
        self.assertEqual({(0, 1), (1, 0), (1, 2), (2, 1)}, g.getedges())

    def testcreatcycle(self):
        g = cr.makecycle(4)
        self.assertEqual({0, 1, 2, 3}, g.getvertices())
        self.assertEqual({(0, 1), (0, 3), (1, 0), (1, 2), (2, 1), (2, 3), (3, 0), (3, 2)}, g.getedges())

    def testcreateproduct(self):
        p = cr.makepath(2)
        c = cr.makecycle(3)
        g = cr.product(p,c)
        self.assertEqual({(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)}, g.getvertices())
        self.assertEqual({((0, 0), (0, 1)),
                         ((0, 1), (0, 2)),
                         ((0, 2), (0, 1)),
                         ((0, 2), (0, 0)),
                         ((0, 1), (0, 0)),
                         ((0, 0), (0, 2)),
                         ((1, 0), (1, 1)),
                         ((1, 1), (1, 2)),
                         ((1, 2), (1, 1)),
                         ((1, 2), (1, 0)),
                         ((1, 1), (1, 0)),
                         ((1, 0), (1, 2)),
                         ((0, 0), (1, 0)),
                         ((1, 0), (0, 0)),
                         ((0, 1), (1, 1)),
                         ((1, 1), (0, 1)),
                         ((0, 2), (1, 2)),
                         ((1, 2), (0, 2))}, g.getedges())

    def testgetedges(self):
        expected = {(1, 2), (1, 3), (2, 1), (2, 4), (3, 1), (4, 2)}
        actual = self.g.getedges()
        self.assertEqual(expected, actual)

    def testgetvertices(self):
        expected = set(range(1, 5))
        actual = self.g.getvertices()
        self.assertEqual(expected, actual)
    
    def testfromedges(self): 
        e = set([(0,1),(1,0),(1,2),(2,1)])
        expected_v = {0,1,2}
        g = cr.fromedges(e)
        self.assertEqual(expected_v,g.getvertices())
        self.assertEqual(e,g.getedges())

    def testFirstMove(self):
        g = cr.gamestate(20, 20)
        g.moverobber(-1, 0)
        self.assertEqual([18, 19], g.robber)
        g.movecops()
        self.assertEqual([0, 1], g.cop0)
        self.assertEqual([0, 2], g.cop1)
        
    def testGameOver(self):
        g = cr.gamestate(20, 20)
        self.assertFalse(g.gameover())

        g.robber = [18, 19]
        g.cop0 = [17, 19]
        g.cop1 = [16, 19]
        self.assertFalse(g.gameover())

        g.robber = [17, 19]
        self.assertTrue(g.gameover())

        g.robber = [10, 5]
        g.cop0 = [0, 0]
        g.cop1 = [10, 5]
        self.assertTrue(g.gameover())

    def testLegalRobberMoves(self):
        g = cr.gamestate(20, 20)

        self.assertTrue(g.moverobber(-1, 0))
        self.assertEqual([18, 19], g.robber)

        self.assertTrue(g.moverobber(1, 0))
        self.assertEqual([19, 19], g.robber)

        self.assertTrue(g.moverobber(0, -1))
        self.assertEqual([19, 18], g.robber)

        self.assertTrue(g.moverobber(0, 1))
        self.assertEqual([19, 19], g.robber)

    def testIllegalRobberMoves(self):
        g = cr.gamestate(20, 20)

        g.robber = [0, 10]
        self.assertFalse(g.moverobber(-1, 0))
        self.assertEqual([0, 10], g.robber)

        g.robber = [19, 10]
        self.assertFalse(g.moverobber(1, 0))
        self.assertEqual([19, 10], g.robber)

        g.robber = [10, 0]
        self.assertFalse(g.moverobber(0, -1))
        self.assertEqual([10, 0], g.robber)

        g.robber = [10, 19]
        self.assertFalse(g.moverobber(0, 1))
        self.assertEqual([10, 19], g.robber)
