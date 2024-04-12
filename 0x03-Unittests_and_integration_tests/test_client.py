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

    def test_public_repos(self, mock_json):
        """More patching"""
        json_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public:

            mock_public.return_value = "hello/world"
            test_class = GithubOrgClient('test')
            result = test_class.public_repos()

            check = [i["name"] for i in json_payload]
            self.assertEqual(result, check)

            mock_public.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Parameterize"""
        github_org_client = GithubOrgClient("example_org")

        result = github_org_client.has_license(repo, license_key)

        self.assertEqual(result, expected_result)


@parameterized_class([
    {"name": "org_payload", "value": org_payload},
    {"name": "repos_payload", "value": repos_payload},
    {"name": "expected_repos", "value": expected_repos},
    {"name": "apache2_repos", "value": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test: fixtures"""
    @classmethod
    def setUpClass(cls):
        """return example payloads found in the fixtures."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration tests"""
        github_org_client = GithubOrgClient("google")
        result = github_org_client.public_repos()

        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """test against license"""
        github_org_client = GithubOrgClient("google")
        result = github_org_client.public_repos("apache-2.0")

        self.assertEqual(result, self.apache2_repos)
