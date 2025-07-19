#!/usr/bin/env python3
"""Unittests and integration tests for GithubOrgClient and utils module."""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct payload."""
        test_payload = {"login": org_name, "id": 1234}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos URL."""
        expected_url = "https://api.github.com/orgs/testorg/repos"
        mock_org_payload = {"repos_url": expected_url}

        with patch.object(
                GithubOrgClient, 'org', new_callable=PropertyMock
                ) as mock_org:
            mock_org.return_value = mock_org_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names."""
        mock_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(
                GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
                ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
                )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test license matching in repos."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient with mocked HTTP."""
    """ Intergration test using actual logic"""

    @classmethod
    def setUpClass(cls) -> None:
        """Start patching requests.get and mock JSON responses."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> Mock:
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/testorg":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test all public repos returned correctly."""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test filtering repos by 'apache-2.0' license."""
        client = GithubOrgClient("testorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
            )
