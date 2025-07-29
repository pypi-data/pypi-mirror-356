import pytest
from unittest.mock import patch, MagicMock
from dbt_heartbeat.main import main


def test_main_with_version_flag(capsys, mock_sys_argv):
    """Test that the version flag works correctly."""
    with mock_sys_argv("--version"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "script.py" in captured.out


def test_main_without_job_id(capsys, mock_sys_argv):
    """Test that the script exits with help message when no job ID is provided."""
    with mock_sys_argv():
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "usage:" in captured.out


@patch("dbt_heartbeat.main.job_monitor")
@patch("dbt_heartbeat.main.dbt_api")
@patch("utils.notifications.run_notifs.Notifier")
def test_main_with_valid_job_id(
    mock_notifier,
    mock_dbt_api,
    mock_job_monitor,
    sample_job_run_data,
    mock_job_run_info,
    mock_sys_argv,
):
    """Test the main function with a valid job ID."""
    # Setup mocks
    mock_job_monitor.monitor_job.return_value = sample_job_run_data
    mock_dbt_api.get_job_run_info.return_value = mock_job_run_info

    with mock_sys_argv("12345"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    # Verify the mocks were called correctly
    mock_job_monitor.monitor_job.assert_called_once_with("12345", 30)
    mock_dbt_api.get_job_run_info.assert_called_once_with("12345")


@patch("dbt_heartbeat.main.validate_environment_vars")
def test_main_with_missing_env_vars(mock_validate_env_vars, mock_sys_argv):
    """Test that the script exits when environment variables are missing."""
    mock_validate_env_vars.return_value = ["DBT_CLOUD_API_KEY"]

    with mock_sys_argv("12345"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


@patch("dbt_heartbeat.main.job_monitor")
@patch("dbt_heartbeat.main.dbt_api")
@patch("utils.notifications.run_notifs.Notifier")
def test_custom_poll_interval(
    mock_notifier,
    mock_dbt_api,
    mock_job_monitor,
    sample_job_run_data,
    mock_job_run_info,
    mock_sys_argv,
):
    """Test that the application correctly uses a custom poll interval."""
    # Setup mocks
    mock_job_monitor.monitor_job.return_value = sample_job_run_data
    mock_dbt_api.get_job_run_info.return_value = mock_job_run_info

    with mock_sys_argv("12345", "--poll-interval", "15"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    # Verify the poll interval was used
    mock_job_monitor.monitor_job.assert_called_once_with("12345", 15)


@patch("dbt_heartbeat.main.job_monitor")
@patch("dbt_heartbeat.main.dbt_api")
@patch("utils.notifications.run_notifs.Notifier")
def test_log_level_changes(
    mock_dbt_api,
    mock_job_monitor,
    sample_job_run_data,
    mock_job_run_info,
    mock_sys_argv,
    caplog,
):
    """Test that changing the log level via command-line arguments correctly affects logging output."""
    # Setup mocks
    mock_job_monitor.monitor_job.return_value = sample_job_run_data
    mock_dbt_api.get_job_run_info.return_value = mock_job_run_info

    # Test with DEBUG level
    with mock_sys_argv("12345", "--log-level", "DEBUG"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    # Verify debug messages are logged
    assert any(record.levelname == "DEBUG" for record in caplog.records)

    # Clear the log
    caplog.clear()

    # Test with ERROR level
    with mock_sys_argv("12345", "--log-level", "ERROR"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    # Verify debug messages are not logged
    assert not any(record.levelname == "DEBUG" for record in caplog.records)


@patch("dbt_heartbeat.main.job_monitor")
@patch("dbt_heartbeat.main.dbt_api")
@patch("utils.notifications.run_notifs.requests.post")
@patch("utils.notifications.run_notifs.os.getenv")
def test_slack_flag_long(
    mock_getenv,
    mock_slack_post,
    mock_dbt_api,
    mock_job_monitor,
    sample_job_run_data,
    mock_job_run_info,
    mock_sys_argv,
):
    """Test that the --slack flag triggers Slack notifications."""
    # Setup mocks
    mock_job_monitor.monitor_job.return_value = sample_job_run_data
    mock_dbt_api.get_job_run_info.return_value = mock_job_run_info
    mock_getenv.return_value = "https://hooks.slack.com/services/test/webhook/url"
    mock_slack_response = MagicMock()
    mock_slack_response.raise_for_status.return_value = None
    mock_slack_post.return_value = mock_slack_response

    with mock_sys_argv("12345", "--slack"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    # Verify Slack notification was sent
    mock_slack_post.assert_called_once()
    call_args = mock_slack_post.call_args
    assert call_args[0][0] == "https://hooks.slack.com/services/test/webhook/url"
    blocks = call_args[1]["json"]["blocks"]
    assert blocks[0]["text"]["text"] == "✅ dbt Job Status Update"
    assert any("Test Job" in field["text"] for field in blocks[1]["fields"])
    assert any("Success" in field["text"] for field in blocks[1]["fields"])


@patch("dbt_heartbeat.main.job_monitor")
@patch("dbt_heartbeat.main.dbt_api")
@patch("utils.notifications.run_notifs.requests.post")
@patch("utils.notifications.run_notifs.os.getenv")
def test_slack_flag_short(
    mock_getenv,
    mock_slack_post,
    mock_dbt_api,
    mock_job_monitor,
    sample_job_run_data,
    mock_job_run_info,
    mock_sys_argv,
):
    """Test that the -s flag triggers Slack notifications."""
    # Setup mocks
    mock_job_monitor.monitor_job.return_value = sample_job_run_data
    mock_dbt_api.get_job_run_info.return_value = mock_job_run_info
    mock_getenv.return_value = "https://hooks.slack.com/services/test/webhook/url"
    mock_slack_response = MagicMock()
    mock_slack_response.raise_for_status.return_value = None
    mock_slack_post.return_value = mock_slack_response

    with mock_sys_argv("12345", "-s"):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    # Verify Slack notification was sent
    mock_slack_post.assert_called_once()
    call_args = mock_slack_post.call_args
    assert call_args[0][0] == "https://hooks.slack.com/services/test/webhook/url"
    blocks = call_args[1]["json"]["blocks"]
    assert blocks[0]["text"]["text"] == "✅ dbt Job Status Update"
    assert any("Test Job" in field["text"] for field in blocks[1]["fields"])
    assert any("Success" in field["text"] for field in blocks[1]["fields"])
