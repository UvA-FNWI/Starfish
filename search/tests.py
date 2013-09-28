"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from search.utils import parse_query
from steep.settings import SEARCH_SYNTAX

class SearchTest(TestCase):
    def test_parse_query(self):
        """
        Tests query parses.
        """
        # Define test shortcut
        def test(query, t2, p2, l2):
            t1, p1, l1 = parse_query(query)
            # t1, p1 and l1 should be (under sort) be equal to t2, p2 and l2
            self.assertEqual(
                (sorted(t1), sorted(p1), sorted(l1)),
                (sorted(t2), sorted(p2), sorted(l2))
            )

        # Create shortnames for special symbols
        dsymb = SEARCH_SYNTAX['DELIM']
        psymb = SEARCH_SYNTAX['PERSON']
        tsymb = SEARCH_SYNTAX['TAG']
        lsymb = SEARCH_SYNTAX['LITERAL']
        esymb = SEARCH_SYNTAX['ESCAPE']

        # Test person tokens
        test("%sTerm" % (psymb,), [], ["Term"], [])
        test("%sTe%srm" % (psymb,tsymb), [], ["Te%srm" % (tsymb, ) ], [])
        test("%sTe%srm" % (psymb,lsymb), [], ["Te%srm" % (lsymb, ) ], [])
        test("%sTerm%s%sTerm2" % (psymb, dsymb, psymb),
                [], ["Term", "Term2"], [])
        test("%sTerm2%s%sTerm" % (psymb, dsymb, psymb),
                [], ["Term", "Term2"], [])
        test(psymb, [], [], [])
        # Test tag tokens
        test("%sTerm" % (tsymb,), ["Term"], [], [])
        test("%sTe%srm" % (tsymb,psymb), ["Te%srm" % (psymb, ) ], [], [])
        test("%sTe%srm" % (tsymb,lsymb), ["Te%srm" % (lsymb, ) ], [], [])
        test("%sTerm%s%sTerm2" % (tsymb, dsymb, tsymb),
                ["Term", "Term2"], [], [])
        test("%sTerm2%s%sTerm" % (tsymb, dsymb, tsymb),
                ["Term", "Term2"], [], [])
        test(tsymb, [], [], [])
        # Test single literal tokens
        test("Term", [], [], ["Term"])
        test("Te%srm" % (tsymb, ), [], [], ["Te%srm" % (tsymb, ) ],)
        test("Te%srm" % (psymb, ), [], [], ["Te%srm" % (psymb, ) ],)
        test("Te%srm" % (lsymb, ), [], [], ["Te%srm" % (lsymb, ) ],)
        test("Term%sTerm2" % (dsymb,),
                [], [], ["Term", "Term2"])
        test("Term2%sTerm" % (dsymb,),
                [], [], ["Term", "Term2"])
        # Test long literal tokens
        test("%sTerm%s" % (lsymb, lsymb), [], [], ["Term"])
        test("%sTerm" % (lsymb,), [], [], ["Term"])
        test("%sTe%srm%s" % (lsymb,psymb, lsymb),
                [], [], ["Te%srm" % (psymb, ) ])
        test("%sTe%srm%s" % (lsymb,tsymb, lsymb),
                [], [], ["Te%srm" % (tsymb, ) ])
        test("%sTerm%s%s%sTerm2%s" % (lsymb, lsymb, dsymb, lsymb, lsymb),
                [], [], ["Term", "Term2"])
        test("%sTerm2%s%s%sTerm%s" % (lsymb, lsymb, dsymb, lsymb, lsymb),
                [], [], ["Term", "Term2"])
        test("%sTerm Term2%s%s%sTerm3%s" % (lsymb, lsymb, dsymb, lsymb, lsymb),
                [], [], ["Term Term2", "Term3"])
        test(lsymb+lsymb, [], [], [])
        # Test mix of persons and tags
        test("%sTerm%s%sTerm2" % (psymb, dsymb, tsymb),
                ["Term2"], ["Term"], [])
        test("%sTerm%s%sTerm2" % (tsymb, dsymb, psymb),
                ["Term"], ["Term2"], [])
        # Test mix of persons and single literals
        test("%sTerm%sTerm2" % (psymb, dsymb),
                [], ["Term"], ["Term2"])
        test("Term%s%sTerm2" % (dsymb, psymb),
                [], ["Term2"], ["Term"])
        # Test mix of persons and long literals
        test("%sTerm%s%sTerm2 Term3%s" % (psymb, dsymb, lsymb, lsymb),
                [], ["Term"], ["Term2 Term3"])
        test("%sTerm2 Term3%s%s%sTerm" % (lsymb, lsymb, dsymb, psymb),
                [], ["Term"], ["Term2 Term3"])
        # Test mix of tags and single literals
        test("%sTerm%sTerm2" % (tsymb, dsymb),
                ["Term"], [], ["Term2"])
        test("Term%s%sTerm2" % (dsymb, tsymb),
                ["Term2"], [], ["Term"])
        # Test mix of tags and long literals
        test("%sTerm%s%sTerm2 Term3%s" % (tsymb, dsymb, lsymb, lsymb),
                ["Term"], [], ["Term2 Term3"])
        test("%sTerm2 Term3%s%s%sTerm" % (lsymb, lsymb, dsymb, tsymb),
                ["Term"], [], ["Term2 Term3"])
        # Test mix of single literals and long literals
        test("Term%s%sTerm2 Term3%s" % (dsymb, lsymb, lsymb),
                [], [], ["Term2 Term3", "Term"])
        test("%sTerm2 Term3%s%sTerm" % (lsymb, lsymb, dsymb),
                [], [], ["Term2 Term3", "Term"])
        # Test escape of tag symbol
        test("%s%sTerm" % (esymb, tsymb), [], [], ["%sTerm" % (tsymb)])
        test("%s%sTerm%s" % (esymb, tsymb, dsymb),
                [], [], ["%sTerm" % (tsymb)])
        # Test escape of person symbol
        test("%s%sTerm" % (esymb, psymb), [], [], ["%sTerm" % (psymb)])
        test("%s%sTerm%s" % (esymb, psymb, dsymb),
                [], [], ["%sTerm" % (psymb)])
        # Test escape of literal symbol
        test("%s%sTerm" % (esymb, lsymb), [], [], ["%sTerm" % (lsymb)])
        test("%s%sTerm%s" % (esymb, lsymb, dsymb),
                [], [], ["%sTerm" % (lsymb)])
        test("%s%sTerm%sTerm2" % (esymb, lsymb, dsymb),
                [], [], ["%sTerm" % (lsymb), "Term2"])
