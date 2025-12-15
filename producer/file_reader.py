import os
import asyncio
import aiofiles

async def tail_file(path: str, poll_interval: float = 0.1):
    # Retry until file exists
    while not os.path.exists(path):
        await asyncio.sleep(0.1)

    async with aiofiles.open(path, "r") as f:
        await f.seek(0, 2)  # go to end
        while True:
            line = await f.readline()
            if line:
                yield line.rstrip("\n")
            else:
                await asyncio.sleep(poll_interval)

