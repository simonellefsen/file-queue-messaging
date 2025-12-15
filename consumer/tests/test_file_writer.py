import aiofiles
import pytest
from file_writer import append_line

@pytest.mark.asyncio
async def test_append_line(tmp_path):
    file_path = tmp_path / "out.txt"

    await append_line(str(file_path), "hello")
    await append_line(str(file_path), "world")

    async with aiofiles.open(file_path, "r") as f:
        contents = await f.readlines()

    assert contents == ["hello\n", "world\n"]

