from pydantic import ValidationError
import pytest
import requests
import chevron
from unittest.mock import patch, MagicMock

from agent_pilot.prompt import create_task, get_prompt, render, templateCache
from agent_pilot.models import PromptVersion


class TestGetTemplate:
    def test_get_template_cache_hit(self, mock_time, sample_prompt_version):
        """Test retrieving a template from cache."""
        # Setup cache with a recent entry
        task_id = "test-task-123"
        version = "v1"
        templateCache[task_id] = {
            "timestamp": (mock_time() * 1000) - 30000,  # 30 seconds ago
            "prompt_version": sample_prompt_version,
        }

        # Reset mock counter after setup
        mock_time.reset_mock()

        # Call the function
        result = get_prompt(task_id, version, api_key="test_api_key")

        # Check the result
        assert result == sample_prompt_version
        assert mock_time.call_count == 1  # Called once to check cache timestamp

    def test_get_template_cache_miss(self, mock_config, mock_requests_post, mock_time, sample_prompt_version_dict):
        """Test retrieving a template when not in cache."""
        # Clear cache
        templateCache.clear()

        # Setup mock response
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"Result": {"prompt_version": sample_prompt_version_dict}}

        task_id = "test-task-123"
        version = "v1"

        # Call the function
        result = get_prompt(task_id, version, api_key="test_api_key")

        assert result

        # Verify request
        mock_requests_post.assert_called_once()
        assert task_id in mock_requests_post.call_args[1]["json"]["TaskId"]
        assert version in mock_requests_post.call_args[1]["json"]["PromptVersion"]

        # Check that result is added to cache
        assert task_id in templateCache
        assert "timestamp" in templateCache[task_id]
        assert "prompt_version" in templateCache[task_id]

    def test_get_template_custom_credentials(self, mock_requests_post, sample_prompt_version_dict):
        """Test retrieving a template with custom API key and URL."""
        # Clear cache
        templateCache.clear()

        # Setup mock response
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"Result": {"prompt_version": sample_prompt_version_dict}}

        task_id = "test-task-123"
        version = "v1"
        custom_api_key = "custom_api_key"
        custom_api_url = "https://custom-api-url.com"

        # Call the function
        result = get_prompt(task_id, version, custom_api_key, custom_api_url)

        assert result

        # Verify custom credentials were used
        auth_header = mock_requests_post.call_args[1]["headers"]["Authorization"]
        assert custom_api_key in auth_header
        assert custom_api_url in mock_requests_post.call_args[0][0]

    def test_get_template_no_api_key(self, mock_config, monkeypatch):
        """Test that an error is raised when no API key is provided."""
        # Set API key to None in config
        mock_config.api_key = None
        mock_config.local_debug = False
        mock_config.api_url = "http://test-api-url.com"

        # Create a mock HttpClient with a post method that raises the expected error
        mock_client = MagicMock()
        mock_client.post.side_effect = RuntimeError("No authentication api_key provided")

        # Patch the get_http_client function to return our mock
        monkeypatch.setattr("agent_pilot.prompt.get_http_client", lambda: mock_client)

        with pytest.raises(RuntimeError, match="No authentication api_key provided"):
            get_prompt("test-task", "v1")

    def test_get_template_unauthorized(self, mock_requests_post):
        """Test handling of 401 unauthorized response."""
        # Clear cache
        templateCache.clear()

        # Setup mock response for 401
        mock_response = mock_requests_post.return_value
        mock_response.status_code = 401
        mock_response.ok = False

        with pytest.raises(RuntimeError, match="Invalid or unauthorized API credentials"):
            get_prompt("test-task", "v1", api_key="test_api_key")

    def test_get_template_server_error(self, mock_requests_post):
        """Test handling of server error response."""
        # Clear cache
        templateCache.clear()

        # Setup mock response for server error
        mock_response = mock_requests_post.return_value
        mock_response.status_code = 500
        mock_response.ok = False
        mock_response.text = "Internal Server Error"

        with pytest.raises(RuntimeError, match="500 - Internal Server Error"):
            get_prompt("test-task", "v1", api_key="test_api_key")

    def test_get_template_network_error(self, mock_requests_post):
        """Test handling of network error during request."""
        # Clear cache
        templateCache.clear()

        # Setup mock for network error
        mock_requests_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with pytest.raises(RuntimeError, match="Network error while fetching template"):
            get_prompt("test-task", "v1", api_key="test_api_key")

    def test_get_template_missing_prompt_version(self, mock_requests_post):
        """Test handling missing prompt_version in response."""
        # Clear cache
        templateCache.clear()

        # Setup mock response with missing prompt_version
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"other_data": "something"}

        with pytest.raises(RuntimeError, match="Template not found"):
            get_prompt("test-task", "v1", api_key="test_api_key")

    def test_get_template_local_debug(self, mock_config, mock_requests_post, sample_prompt_version_dict):
        """Test behavior when local_debug is enabled."""
        # Clear cache
        templateCache.clear()

        # Enable local_debug
        mock_config.local_debug = True

        # Setup mock response
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"Result": {"prompt_version": sample_prompt_version_dict}}

        # Call the function
        get_prompt("test-task", "v1", api_key="test_api_key")

        # Verify local debug headers were used
        headers = mock_requests_post.call_args[1]["headers"]
        assert "Authorization" in headers


class TestRenderTemplate:
    def test_render_template_basic(self, mock_requests_post, sample_prompt_version, sample_prompt_version_dict):
        """Test basic template rendering functionality."""
        # Clear cache
        templateCache.clear()

        # Setup mock for get_template
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"Result": {"prompt_version": sample_prompt_version_dict}}

        # Variables for template
        variables = {"variable": "I am a test variable", "name": "Test User"}

        # Call the function
        result = render("test-task-123", "v1", variables, api_key="test_api_key")

        # Check result structure
        assert "messages" in result
        assert "task_id" in result
        assert "version" in result
        assert "temperature" in result
        assert "top_p" in result
        assert "extra_headers" in result

        # Verify template variables were rendered
        assert "I am a test variable" in result["messages"][0]["content"]
        assert "Test User" in result["messages"][1]["content"]

    def test_render_template_empty_variables(
        self, mock_requests_post, sample_prompt_version, sample_prompt_version_dict
    ):
        """Test template rendering with empty variables."""
        # Clear cache
        templateCache.clear()

        # Setup mock for get_template
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"Result": {"prompt_version": sample_prompt_version_dict}}

        # Call with empty variables
        result = render("test-task-123", "v1", {}, api_key="test_api_key")

        # Verify empty variables in rendered output
        assert result["messages"][0]["content"] == "You are a helpful assistant. "
        assert result["messages"][1]["content"] == "Hello, !"

    def test_render_template_not_found(self, mock_requests_post):
        """Test handling of template not found."""
        # Clear cache
        templateCache.clear()

        # Setup mock response for missing template
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"prompt_version": None}

        with pytest.raises(RuntimeError, match="Template not found"):
            render("missing-task", "v1", {}, api_key="test_api_key")

    def test_render_template_rendering_error(self, mock_requests_post, sample_prompt_version_dict, monkeypatch):
        """Test handling of rendering error."""
        # Clear cache
        templateCache.clear()

        # Setup mock for get_template
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"prompt_version": sample_prompt_version_dict}

        # Mock chevron.render to raise an exception
        def mock_render(*args, **kwargs):
            raise ValueError("Error rendering template")

        monkeypatch.setattr(chevron, "render", mock_render)

        with pytest.raises(RuntimeError, match="Error rendering template"):
            render("test-task-123", "v1", {}, api_key="test_api_key")

    def test_render_template_custom_credentials(self, mock_requests_post, sample_prompt_version_dict):
        """Test rendering with custom API credentials."""
        # Clear cache
        templateCache.clear()

        # Setup mock for get_template
        mock_response = mock_requests_post.return_value
        mock_response.json.return_value = {"Result": {"prompt_version": sample_prompt_version_dict}}

        custom_api_key = "custom_api_key"
        custom_api_url = "https://custom-api-url.com"
        variables = {"variable": "test", "name": "User"}

        # Call with custom credentials
        result = render("test-task-123", "v1", variables, custom_api_key, custom_api_url)

        assert result

        # Verify custom API URL was used
        print(mock_requests_post.call_args)
        assert mock_requests_post.call_args is not None
        assert custom_api_url in mock_requests_post.call_args[0][0]

        # Check if the custom API key was used (this depends on how headers are set)
        headers = mock_requests_post.call_args[1]["headers"]
        assert "Authorization" in headers or "X-Top-Account-Id" in headers


@pytest.fixture
def sample_task_info():
    """Provides sample valid task information."""
    return {
        "task_name": "test_task",
        "task_category": "DEFAULT",
        "prompt": "Hello, how are you? {{CONTENT}}",
        "model_name": "doubao-1.5-pro-32k-250115",
    }


class TestCreateTask:
    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_success(self, mock_get_http_client, sample_task_info, sample_prompt_version_dict):
        """Test successful task creation."""
        mock_client_instance = MagicMock()
        mock_get_http_client.return_value = mock_client_instance
        # Simulate successful API response
        api_response_data = {"Result": {"prompt_version": sample_prompt_version_dict}}
        mock_client_instance.post.return_value = (api_response_data, 200)

        # Expected PromptVersion object based on sample_prompt_version_dict
        expected_prompt_version = PromptVersion(**sample_prompt_version_dict)

        result = create_task(sample_task_info, api_key="test_key", api_url="http://test.url")

        assert isinstance(result, PromptVersion)
        assert result == expected_prompt_version
        mock_client_instance.post.assert_called_once()
        call_args = mock_client_instance.post.call_args[1]
        assert call_args["action"] == "CreateTask"
        assert call_args["api_key"] == "test_key"
        assert call_args["api_url"] == "http://test.url"

    @patch("agent_pilot.prompt.CreateTaskRequest.from_task_info_dict_to_create_task_request")
    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_validation_error(self, mock_get_http_client, mock_from_task_info_method, sample_task_info):
        """Test task creation with validation error in task_info."""
        mock_from_task_info_method.side_effect = ValidationError.from_exception_data(
            title="Test ValidationError", line_errors=[]
        )

        with pytest.raises(RuntimeError, match="Validation error: "):
            create_task(sample_task_info, api_key="test_key")

        mock_get_http_client.return_value.post.assert_not_called()

    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_unauthorized(self, mock_get_http_client, sample_task_info):
        """Test task creation with 401 Unauthorized response."""
        mock_client_instance = MagicMock()
        mock_get_http_client.return_value = mock_client_instance
        mock_client_instance.post.return_value = ({"error": "unauthorized"}, 401)

        with pytest.raises(RuntimeError, match="Invalid or unauthorized API credentials"):
            create_task(sample_task_info, api_key="test_key")

    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_server_error(self, mock_get_http_client, sample_task_info):
        """Test task creation with 500 Server Error response."""
        mock_client_instance = MagicMock()
        mock_get_http_client.return_value = mock_client_instance
        error_response_text = "Internal Server Error Details"
        mock_client_instance.post.return_value = (error_response_text, 500)

        with pytest.raises(RuntimeError, match=f"Error fetching template: 500 - {error_response_text}"):
            create_task(sample_task_info, api_key="test_key")

    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_api_call_exception(self, mock_get_http_client, sample_task_info):
        """Test task creation when API call itself raises an exception (e.g., network error)."""
        mock_client_instance = MagicMock()
        mock_get_http_client.return_value = mock_client_instance
        # Simulate a requests.exceptions.RequestException or similar
        mock_client_instance.post.side_effect = requests.exceptions.ConnectionError("Network down")

        with pytest.raises(RuntimeError, match="Network down"):
            create_task(sample_task_info, api_key="test_key")

    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_custom_credentials_used(
        self, mock_get_http_client, sample_task_info, sample_prompt_version_dict
    ):
        """Test that custom API key and URL are used when provided."""
        mock_client_instance = MagicMock()
        mock_get_http_client.return_value = mock_client_instance
        api_response_data = {"Result": {"prompt_version": sample_prompt_version_dict}}
        mock_client_instance.post.return_value = (api_response_data, 200)

        custom_key = "custom_api_key_for_create"
        custom_url = "https://custom.api.url/for_create"

        create_task(sample_task_info, api_key=custom_key, api_url=custom_url)

        mock_client_instance.post.assert_called_once()
        call_args = mock_client_instance.post.call_args[1]
        assert call_args["api_key"] == custom_key
        assert call_args["api_url"] == custom_url

    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_no_prompt_version_in_response(self, mock_get_http_client, sample_task_info):
        """Test handling when 'prompt_version' is missing in a successful API response."""
        mock_client_instance = MagicMock()
        mock_get_http_client.return_value = mock_client_instance
        # Simulate successful API response but missing 'prompt_version'
        api_response_data = {"Result": {"other_data": "some_value"}}
        mock_client_instance.post.return_value = (api_response_data, 200)

        with pytest.raises(RuntimeError):
            create_task(sample_task_info, api_key="test_key")

    @patch("agent_pilot.prompt.get_http_client")
    def test_create_task_result_key_missing_in_response(self, mock_get_http_client, sample_task_info):
        """Test handling when 'Result' key is missing in a successful API response."""
        mock_client_instance = MagicMock()
        mock_get_http_client.return_value = mock_client_instance
        api_response_data = {"UnexpectedKey": {"prompt_version": {}}}  # 'Result' key is missing
        mock_client_instance.post.return_value = (api_response_data, 200)

        with pytest.raises(RuntimeError):
            create_task(sample_task_info, api_key="test_key")
