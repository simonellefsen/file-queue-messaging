import aiofiles

async def append_line(path: str, line: str):
    """
    Append a line to a file asynchronously.
    Ensures correct newline handling.
    """
    async with aiofiles.open(path, "a") as f:
        await f.write(line + "\n")

