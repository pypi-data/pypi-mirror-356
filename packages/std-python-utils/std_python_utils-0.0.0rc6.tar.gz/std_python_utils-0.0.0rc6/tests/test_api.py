import pytest
from pydantic import ValidationError

# Assuming the models are defined in a file called models.py
# Adjust the import paths accordingly in your own project.
from std_utils.models.api import APIRequest, APIResponse


def test_api_request_creation_valid():
    """
    Test that a valid APIRequest is created successfully.
    """
    valid_request_data = {
        "endpoint": "https://api.example.com/v1/users",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "query_params": {
            "verbose": True
        },
        "body": {
            "username": "john_doe"
        }
    }
    request = APIRequest(**valid_request_data)

    assert (
        request.endpoint.unicode_string() == "https://api.example.com/v1/users")
    assert request.method == "POST"
    assert request.headers == {"Content-Type": "application/json"}
    assert request.query_params == {"verbose": True}
    assert request.body == {"username": "john_doe"}


def test_api_request_missing_method():
    """
    Test that creating an APIRequest without a required field (method) raises
    a ValidationError.
    """
    invalid_request_data = {
        "endpoint": "https://api.example.com/v1/users"
        # 'method' is missing
    }
    with pytest.raises(ValidationError):
        APIRequest(**invalid_request_data)


def test_api_request_invalid_endpoint():
    """
    Test that an invalid URL for the endpoint raises a ValidationError.
    """
    invalid_request_data = {
        "endpoint": "not-a-valid-url",  # Invalid URL format
        "method": "GET"
    }
    with pytest.raises(ValidationError):
        APIRequest(**invalid_request_data)


def test_api_request_defaults():
    """
    Test that default values (headers, query_params, body) are set correctly
    when not provided.
    """
    request_data = {
        "endpoint": "https://api.example.com/v1/users", "method": "GET",
    }
    request = APIRequest(**request_data)

    assert request.headers == {'Content-Type': 'application/json'}
    assert request.query_params == {}
    assert request.body == {}


def test_api_response_creation_valid():
    """
    Test that a valid APIResponse is created successfully.
    """
    valid_response_data = {
        "status_code": 200, "headers": {
            "Content-Type": "application/json"
        }, "data": {
            "result": "success"
        }, "error": None
    }
    response = APIResponse(**valid_response_data)

    assert response.status_code == 200
    assert response.headers == {"Content-Type": "application/json"}
    assert response.data == {"result": "success"}
    assert response.error is None


def test_api_response_missing_status_code():
    """
    Test that creating an APIResponse without a required field (status_code)
    raises a ValidationError.
    """
    invalid_response_data = {
        # 'status_code' is missing
        "headers": {
            "Content-Type": "application/json"
        }
    }
    with pytest.raises(ValidationError):
        APIResponse(**invalid_response_data)


def test_api_response_default_fields():
    """
    Test that optional fields have expected default values when not provided.
    """
    response_data = {
        "status_code": 404
    }
    response = APIResponse(**response_data)

    assert response.status_code == 404
    assert response.headers == {}  # default
    assert response.data == {}  # default
    assert response.error is None  # default
