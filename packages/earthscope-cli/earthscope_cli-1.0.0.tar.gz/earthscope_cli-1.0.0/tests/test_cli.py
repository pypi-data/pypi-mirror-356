from earthscope_sdk import __version__ as sdk_version

from earthscope_cli import __version__ as cli_version
from earthscope_cli.main import app

from .conftest import runner


class TestCli:
    def test_version(self):
        result = runner.invoke(app, "--version")
        assert result.exit_code == 0
        assert (
            result.stdout.strip()
            == f"earthscope-cli/{cli_version} earthscope-sdk/{sdk_version}"
        )
