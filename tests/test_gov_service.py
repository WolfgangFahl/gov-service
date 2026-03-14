"""
Created on 2026-03-14

@author: wf
"""
from basemkit.basetest import Basetest
from fastapi.testclient import TestClient

from govservice.govservice import GovService


class TestGovService(Basetest):
    """
    Test the GOV service /item/show endpoint
    see https://github.com/WolfgangFahl/gov-service/issues/1
    """

    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.service = GovService(debug=debug)
        self.client = TestClient(self.service.app)

    def test_item_show_name_by_gov_id(self):
        """
        test /item/show/SCHERGJO54EJ returns GOV-Kennung and Name
        """
        if self.inPublicCI():
            return
            
        response = self.client.get("/item/show/SCHERGJO54EJ")
        self.assertEqual(200, response.status_code)
        html = response.text
        if self.debug:
            print(html)
        self.assertIn("SCHERGJO54EJ", html)
        self.assertIn("Schönberg", html)
