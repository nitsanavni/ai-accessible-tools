import pytest
import shutil
import tempfile


@pytest.fixture
def temp_fizzbuzz_copy():
    with tempfile.NamedTemporaryFile(
        mode="w", delete=True, dir=".", prefix="fizzbuzz_copy_", suffix=".py"
    ) as temp_file:
        shutil.copyfile("fizzbuzz.py", temp_file.name)
        yield temp_file.name
