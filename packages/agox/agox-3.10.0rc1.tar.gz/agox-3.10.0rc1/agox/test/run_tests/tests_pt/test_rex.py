import pytest

from agox.test.run_tests.run_utils import agox_test_run


@pytest.mark.skip
@pytest.mark.ray
def test_rex(tmp_path, cmd_options, ray_fix):
    mode = "rex"  # This determines the script that is imported.
    agox_test_run(mode, tmp_path, cmd_options)
