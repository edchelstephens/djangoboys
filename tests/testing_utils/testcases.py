import datetime
import json
from typing import Any
from urllib.parse import urlencode

import pytest
from django.db.models import Model, QuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.test.testcases import SimpleTestCase, TestCase
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from tests import User
from tests.testing_utils.parsers import StringToHTMLParserMixin
from tests.testing_utils.request import (
    DjangoRequestFactoryMixin,
    RestRequestFactoryMixin,
)
from utils.debug import DebuggerMixin


class TestAssertionsMixin(StringToHTMLParserMixin):
    """Mixins for custom test assertions."""

    def assertListsAreEqual(self, first: list, second: list, msg: str = None) -> None:
        """Assert that first and second lists are equal."""

        list_from_first_side_equal = all(
            (item in second) and first.count(item) == second.count(item)
            for item in first
        )

        list_from_second_side_equal = all(
            (item in first) and first.count(item) == second.count(item)
            for item in second
        )

        lists_equal = list_from_first_side_equal and list_from_second_side_equal

        if msg is None:
            msg = f"Lists are not equal! \n\n  {first} \n\n!= \n \n{second}"

        assert lists_equal, msg

    def assertIdInRecords(self, id: int, records: list[dict]) -> None:
        """Assert that id is in one of records dict in records list."""

        id_in_records = any([id == record.get("id") for record in records])
        msg = f"{id} not found on {records}"

        assert id_in_records, msg

    def assertIdNotInRecords(self, id: int, records: list[dict]) -> None:
        """Assert that id is not in one of records dict in records list."""

        id_in_records = any([id == record.get("id") for record in records])
        msg = f"{id} found on {records}"

        assert not id_in_records, msg

    def assertDatesEqual(
        self, date1: datetime.date, date2: datetime.date, string_format="%Y-%m-%d"
    ) -> None:
        """Assert given dates are equal when formatted using string format."""

        date1_string = date1.strftime(string_format)
        date2_string = date2.strftime(string_format)

        msg = f"{date1_string} != {date2_string}"

        assert date1_string == date2_string, msg

    def assertTimesEqual(
        self, time1: datetime.time, time2: datetime.time, string_format="%H:%M"
    ) -> None:
        """Assert given times are equal when formatted using string format."""

        time1_string = time1.strftime(string_format)
        time2_string = time2.strftime(string_format)

        msg = f"{time1_string} != {time2_string}"

        assert time1_string == time2_string, msg

    def assertIsJsonResponse(self, response: HttpResponse) -> None:
        """Assert that response is an instance of JsonResponse."""

        msg = f"{response} is not an instance of JsonResponse"

        assert isinstance(response, JsonResponse), msg

    def assertDictValuesUpdated(self, dict1: dict, dict2: dict) -> None:
        """Assert that every value on dictionary keys from dict1 has been changed in dict2."""

        for key in dict1:
            dict1_value = dict1[key]
            dict2_value = dict2[key]
            msg = f"{dict1_value} == {dict2_value}"
            assert dict1_value != dict2_value, msg

    def assertStringIsInHTMLResponseContent(
        self, string: str, response: HttpResponse, msg=None
    ) -> None:
        """Assert that string is inside of html response content when converted to bytes."""

        string = self.parse_to_html(string)
        content = str(response.content)
        if msg is None:
            msg = f"{string} not in {content}"
        assert string in content, msg

    def assertStringIsNotInHTMLResponseContent(
        self, string: str, response: HttpResponse, msg=None
    ) -> None:
        """Assert that string is not inside of html response content when converted to bytes."""

        string = self.parse_to_html(string)
        content = str(response.content)
        if msg is None:
            msg = f"{string} in {content}"
        assert string not in content, msg


class TestMixin(TestAssertionsMixin, DebuggerMixin):
    """Mixin class for tests."""

    def save_and_refresh(self, model: Model) -> None:
        """Save and refresh from db the model instance."""
        model.save()
        model.refresh_from_db()

    def get_record_dict_with_id(self, id: int, records) -> dict:
        """Get record dict data from list of record dict data."""

        data = {}
        for record in records:
            if record.get("id") == id:
                data = record
                break

        return data

    def is_last_index(self, index: int, items: list) -> bool:
        """Check if index is last index."""
        return index + 1 == len(items)

    def get_url_parameterized(self, url: str, **parameters) -> str:
        """Get url with passed query string parameters"""
        url += "?"
        for index, key in enumerate(parameters):
            url += f"{key}={parameters[key]}"
            if not (self.is_last_index(index, parameters)):
                url += "&"

        return url

    def get_response_context_single_message(self, response: HttpResponse) -> str:
        """Get the single message from django messages middleware on the response."""

        context_messages = response.context["messages"]
        messages_strings = [m.message for m in context_messages]

        assert len(messages_strings) == 1

        single_message = messages_strings[0]

        return single_message

    def encode_data_for_form_urlencoded_content_type(self, data: dict) -> str:
        """Transform data to url encoded string.

        Used for requests with application/x-www-form-urlencoded content type."""
        return urlencode(data)


@pytest.mark.django_db
@pytest.mark.models
class QuerySetTestMixin:
    """Mixin for query set tests."""

    def assertQuerySetEqualByIds(
        self, first: QuerySet, second: QuerySet, msg: str = None
    ) -> None:
        """Assert query sets are equal by using id checks."""
        first_queryset_ids = list(first.values_list("id", flat=True))
        second_queryset_ids = list(second.values_list("id", flat=True))

        if msg is None:
            msg = "Queryset ids not equal! {} != {}".format(
                repr(first_queryset_ids), repr(second_queryset_ids)
            )
        assert first_queryset_ids == second_queryset_ids, msg

    def assertQuerySetIsIn(
        self, first: QuerySet, second: QuerySet, msg: str = None
    ) -> None:
        """Assert first query sets is a subset of second queryset."""
        first_queryset_ids = list(first.values_list("id", flat=True))
        second_queryset_ids = list(second.values_list("id", flat=True))

        if msg is None:
            msg = "Queryset {} not in {}!".format(
                repr(first_queryset_ids), repr(second_queryset_ids)
            )
        for model_id in first_queryset_ids:
            assert model_id in second_queryset_ids, msg


@pytest.mark.non_db
class NonDBTestCase(TestMixin, SimpleTestCase):
    """Our custom test case wrapper for tests not involving database access."""

    maxDiff = None


@pytest.mark.django_db
class WithDBTestCase(QuerySetTestMixin, TestMixin, TestCase):
    """Our custom test case wrapper for tests including database access."""

    maxDiff = None


@pytest.mark.django_db
@pytest.mark.models
class ModelTestCase(TestMixin, TestCase):
    """Our custom test case wrapper for testing django models."""

    maxDiff = None


@pytest.mark.django_db
@pytest.mark.django_views
class DjangoViewTestCase(TestMixin, DjangoRequestFactoryMixin, TestCase):
    """Our test case wrapper for testing django views."""

    maxDiff = None

    def set_user(self, request, user: User) -> None:
        """Manually set request.user to user.

        To simulate a user logged-in trying to access an endpoint.
        """
        request.user = user

    def get_json_response_data(self, response) -> Any:
        """Get json response data from JSONResponse object content."""
        try:
            return json.loads(response.content)
        except TypeError:
            return json.loads(self.get_string_response(response))
        except Exception as exc:
            raise exc

    def get_dict_response_data(self, response) -> dict:
        """Get expected dictionary response data from deserialized JSONResponse response.content"""
        data = self.get_json_response_data(response)
        if not isinstance(data, dict):
            raise TypeError(
                "deserialized response.content is not a python dict but a {}".format(
                    type(data)
                )
            )
        return data

    def get_list_response_data(self, response) -> list:
        """Get expected list response data from deserialized JSONResponse response.content"""
        data = self.get_json_response_data(response)
        if not isinstance(data, list):
            raise TypeError(
                "deserialized response.content is not a python list but a {}".format(
                    type(data)
                )
            )
        return data

    def get_string_response(self, response) -> str:
        """Get the decoded response string from bytestring response.content"""
        return response.content.decode()


@pytest.mark.django_db
@pytest.mark.api_views
class RestAPITestCase(TestMixin, RestRequestFactoryMixin, APITestCase):
    """Our test case wrapper for rest_framework api views."""

    maxDiff = None

    def set_user(self, request, user: User) -> None:
        """Forcibly set request.user to user.

        This is used on views which requires authenticated requests.
        https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
        """
        force_authenticate(request, user=user)


class WithRedirectionTestCase(DjangoViewTestCase):
    """Test case for django views with redirections."""

    def run_redirection_assertions(self, response, redirect_url: str) -> None:
        """Run assertions that response is a redirect response object to given redirect url."""

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, redirect_url)


class DjangoJsonListViewTestCase(DjangoViewTestCase):
    """Test case class wtih views that return JsonResponse list of data."""

    def run_list_view_response_data_assertions(
        self, response, expected_data: dict
    ) -> None:
        """Run assertion that response data for a listing endpoint is the same as expected data.

        The endpoint should return a json on this shape:
        {
            "total": <total_count>,
            "records": [],
        }
        """

        response_data = self.get_dict_response_data(response)
        self.assertEqual(response_data["total"], expected_data["total"])
        self.assertListsAreEqual(response_data["records"], expected_data["records"])
