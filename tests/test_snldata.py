import pytest
import sys
from module import snldata

    def test_setUp():
        service = snldata.SnlSession()
        super().setUp()

    def test_tearDown():
        service.close()
        
    def test_testQuery():
        service = snldata.SnlSession()
        service.search(query="aa-", best=True)
        assert self.service.title == "aa-"
        service.close()
    
    def test_python():
        assert sys.version_info >= (3, 6)
