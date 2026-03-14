"""
Created on 2026-03-14

@author: wf
"""

import json

import yaml
from basemkit.basetest import Basetest
from fastapi.testclient import TestClient

from govservice.govservice import GovService

GOV_ID = "SCHERGJO54EJ"
EXPECTED_NAME = "Schönberg"


class TestGovService(Basetest):
    """
    Test the GOV service /item/show endpoint with content negotiation.
    see https://github.com/WolfgangFahl/gov-service/issues/1
    see https://github.com/WolfgangFahl/gov-service/issues/2
    """

    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.service = GovService(debug=debug)
        self.client = TestClient(self.service.app)

    def test_item_show_html(self):
        """
        test /item/show/SCHERGJO54EJ returns HTML by default (Accept: text/html)
        """
        if self.inPublicCI():
            return
        response = self.client.get(f"/item/show/{GOV_ID}", headers={"Accept": "text/html"})
        self.assertEqual(200, response.status_code)
        html = response.text
        if self.debug:
            print(html)
        self.assertIn(GOV_ID, html)
        self.assertIn(EXPECTED_NAME, html)

    def test_item_show_json(self):
        """
        test /item/show/SCHERGJO54EJ returns JSON via Accept header
        """
        if self.inPublicCI():
            return
        response = self.client.get(f"/item/show/{GOV_ID}", headers={"Accept": "application/json"})
        self.assertEqual(200, response.status_code)
        data = json.loads(response.text)
        if self.debug:
            print(data)
        self.assertEqual(GOV_ID, data["gov_id"])
        self.assertIn(EXPECTED_NAME, data["names"])

    def test_item_show_json_format_param(self):
        """
        test /item/show/SCHERGJO54EJ?format=json returns JSON via query param
        """
        if self.inPublicCI():
            return
        response = self.client.get(f"/item/show/{GOV_ID}?format=json")
        self.assertEqual(200, response.status_code)
        data = json.loads(response.text)
        self.assertEqual(GOV_ID, data["gov_id"])
        self.assertIn(EXPECTED_NAME, data["names"])

    def test_item_show_yaml(self):
        """
        test /item/show/SCHERGJO54EJ returns YAML via Accept header
        """
        if self.inPublicCI():
            return
        response = self.client.get(f"/item/show/{GOV_ID}", headers={"Accept": "application/x-yaml"})
        self.assertEqual(200, response.status_code)
        data = yaml.safe_load(response.text)
        if self.debug:
            print(response.text)
        self.assertEqual(GOV_ID, data["gov_id"])
        self.assertIn(EXPECTED_NAME, data["names"])

    def test_item_show_name_by_gov_id(self):
        """
        test /item/show/SCHERGJO54EJ returns GOV-Kennung and Name (default html)
        """
        if self.inPublicCI():
            return
        response = self.client.get(f"/item/show/{GOV_ID}")
        self.assertEqual(200, response.status_code)
        html = response.text
        if self.debug:
            print(html)
        self.assertIn(GOV_ID, html)
        self.assertIn(EXPECTED_NAME, html)
