#!/usr/bin/env python3
"""Parameterize and patch as decorators"""

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock


class TestGithubOrgClient(unittest.TestCase):
    """Parameterize and patch as decorators"""
    @patch('client.get_json')
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org"""
        test_response = {"login": org_name}
        mock_get_json.return_value = test_response

        github_org_client = GithubOrgClient(org_name)
        result = github_org_client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_response)
