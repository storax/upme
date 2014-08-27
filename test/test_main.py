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

    def test_is_outdated(self):
        p = pkg_resources.get_distribution('pip')
        p._parsed_version = ('00000000', '00000000', '00000000', '*final')
        p._version = '0.0.0'
        r = upme.main.is_outdated(p, dep=True)
        assert p in r
        r = upme.main.is_outdated(p, dep=False)
        assert p in r
        assert len(r) == 1

    def test_update(self):
        try:
            upme.main.update('upme', args=['-h'])
        except SystemExit as e:
            assert e.code == 0

    @classmethod
    def teardown_class(cls):
        pass
