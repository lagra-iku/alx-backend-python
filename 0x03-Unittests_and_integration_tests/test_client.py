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

        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_response)

    def test_public_repos_url(self):
        """Mocking a property"""
        mock_payload = {
            "login": "example_org",
            "repos_url": "https://api.github.com/orgs/example_org/repos"
        }

        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_payload

            github_org_client = GithubOrgClient("example_org")
            result = github_org_client._public_repos_url

            self.assertEqual(
                result,
                "https://api.github.com/orgs/example_org/repos"
            )
