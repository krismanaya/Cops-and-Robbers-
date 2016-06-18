import unittest
import tests.testExample
import tests.testiannis 
import tests.testProduction

def suite():
    s = unittest.TestSuite()

    s.addTest(unittest.makeSuite(tests.testExample.TestSequenceFunctions))
    s.addTest(unittest.makeSuite(tests.testiannis.TestIannis))
    s.addTest(unittest.makeSuite(tests.testProduction.TestProduction))

    return s

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
