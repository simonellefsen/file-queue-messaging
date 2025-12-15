import asyncio
import aiofiles
import pytest
from file_reader import tail_file

@pytest.mark.asyncio
async def test_tail_file(tmp_path):
    file_path = tmp_path / "test.txt"
    async with aiofiles.open(file_path, "w") as f:
        await f.write("hello\n")

    # Start tailer
    async def collect():
        async for line in tail_file(str(file_path)):
            return line

    task = asyncio.create_task(collect())

    await asyncio.sleep(0.1)
    async with aiofiles.open(file_path, "a") as f:
        await f.write("world\n")

    line = await asyncio.wait_for(task, timeout=1)
    assert line == "world"

