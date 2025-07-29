"""Tests for alphai CLI."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, Mock

from alphai.cli import main
from alphai.config import Config


def test_cli_version():
    """Test --version flag works."""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert "alphai version" in result.output


def test_cli_help():
    """Test --help flag works."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "alphai - A CLI tool for the runalph.ai platform" in result.output


@patch('alphai.config.Config.load')
def test_cli_status_not_logged_in(mock_config_load):
    """Test status command when not logged in."""
    # Mock configuration without token
    mock_config = Mock(spec=Config)
    mock_config.bearer_token = None
    mock_config.api_url = "https://runalph.ai/api"
    mock_config.current_org = None
    mock_config.current_project = None
    mock_config.debug = False
    mock_config_load.return_value = mock_config
    
    runner = CliRunner()
    result = runner.invoke(main, ['status'])
    assert result.exit_code == 0
    assert "Not logged in" in result.output


def test_config_commands_help():
    """Test config subcommands help."""
    runner = CliRunner()
    result = runner.invoke(main, ['config', '--help'])
    assert result.exit_code == 0
    assert "Manage configuration settings" in result.output


def test_orgs_commands_help():
    """Test orgs subcommands help."""
    runner = CliRunner()
    result = runner.invoke(main, ['orgs', '--help'])
    assert result.exit_code == 0
    assert "Manage organizations" in result.output


def test_projects_commands_help():
    """Test projects subcommands help."""
    runner = CliRunner()
    result = runner.invoke(main, ['projects', '--help'])
    assert result.exit_code == 0
    assert "Manage projects" in result.output


def test_run_command_help():
    """Test run command help."""
    runner = CliRunner()
    result = runner.invoke(main, ['run', '--help'])
    assert result.exit_code == 0
    assert "Launch and manage local Docker containers" in result.output 