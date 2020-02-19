import unittest
import SnlData.snldata

class TestSnlData(unittest.TestCase):

    def setUp(self):
        self.service = snldata.SnlSession()
        super().setUp()

    def tearDown(self):
        self.service.close()
        
    def testQuery(self):
        self.service.search(query="aa-", best=True)
        self.assertEqual( self.service.title, "aa-")
        
if __name__ == '__main__':
    unittest.main()
