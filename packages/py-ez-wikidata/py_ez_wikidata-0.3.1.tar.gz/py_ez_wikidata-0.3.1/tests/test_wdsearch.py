"""
Created on 2022-07-24

@author: wf
"""

import json

from ez_wikidata.wdsearch import WikidataSearch
from tests.basetest import BaseTest


class TestWikidataSearch(BaseTest):
    """
    test the WikidataSearch
    """

    def testWikidataSearch(self):
        """
        test Wikidata Search
        """
        examples = {
            "Q2020153": {"search": {"en": "academic con", "fr": "congrès sci"}},
            "Q145": {"search": {"en": "united king"}},
            "Q169889": {"search": {"en": "abc"}},
        }
        wds = WikidataSearch()
        limit = 2
        debug = self.debug
        # debug = True
        for i, (expected_qid, search_dict) in enumerate(examples.items(), start=1):
            search = search_dict["search"]
            for lang, search_for in search.items():
                wds.language = lang
                sr = wds.searchOptions(search_for)
                self.assertTrue(sr is not None)
                if debug:
                    print(f"{i:2}:{search_for}({lang}):{len(sr)}")
                    print(json.dumps(sr, indent=2))
                    for j, record in enumerate(sr):
                        qid, qlabel, desc = record
                        if j < limit and debug:
                            print(f"{j+1}:{qid} {qlabel}-{desc}")
                first_qid = sr[0][0]
                self.assertEqual(expected_qid, first_qid)

    def testWikidataProperties(self):
        """
        test getting wikidata Properties
        """
        wds = WikidataSearch()
        debug = self.debug
        props = wds.getProperties()
        if debug:
            print(f"found {len(props)} wikidata properties")
        self.assertTrue(len(props) > 10000)
