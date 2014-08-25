"""
Tests for `upme` module.
"""
import pkg_resources
import upme.main

class Test_Main(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_get_required(self):
        r = upme.main.get_required('upme')
        expect = ('pip', 'setuptools', 'upme')
        for req in expect:
            assert pkg_resources.get_distribution(req) in r

    @classmethod
    def teardown_class(cls):
        pass
