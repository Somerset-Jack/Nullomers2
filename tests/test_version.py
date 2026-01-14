from typer.testing import CliRunner

from Nullomers.version import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0