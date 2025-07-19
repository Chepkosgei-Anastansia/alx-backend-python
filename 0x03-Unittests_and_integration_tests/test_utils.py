#!/usr/bin/env python3
"""Unittests and integration tests for GithubOrgClient and utils module."""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test successful access of nested maps."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test KeyError is raised for invalid access."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected payload."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch(
                "utils.requests.get", return_value=mock_response
                ) as mock_get:

            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method result."""

        class TestClass:
            def a_method(self) -> int:
                """A method that returns 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized property."""
                return self.a_method()

        with patch.object(
                TestClass, 'a_method', return_value=42
                ) as mock_method:

            my_object = TestClass()
            result1 = my_object.a_property
            result2 = my_object.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


