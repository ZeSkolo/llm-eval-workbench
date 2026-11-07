import unittest
from core import run

class Tests(unittest.TestCase):

    def p(self):
        return {'cases': [{'id': 'x', 'must_include': ['safe']}], 'candidate': {'x': 'safe'}}

    def test_pass(self):
        self.assertTrue(run(self.p())['release_passed'])

    def test_regression(self):
        p = self.p()
        p.update(candidate={'x': 'bad'}, baseline={'x': 'safe'}, threshold=0)
        self.assertFalse(run(p)['release_passed'])

    def test_json_failure(self):
        p = self.p()
        p['cases'] = [{'id': 'x', 'json_keys': ['a']}]
        self.assertFalse(run(p)['release_passed'])

    def test_missing(self):
        p = self.p()
        p['candidate'] = {}
        with self.assertRaises(ValueError):
            run(p)

    def test_no_rules(self):
        p = self.p()
        p['cases'] = [{'id': 'x'}]
        with self.assertRaises(ValueError):
            run(p)
