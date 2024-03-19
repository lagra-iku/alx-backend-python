#!/usr/bin/env python3
"""
write a measure_runtime coroutine that will execute async_comprehension
four times in parallel using asyncio.gather
"""

import asyncio
import random
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime():
    """
    a measure_runtime coroutine function
    """
    start_time = time.time()
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )
    end_time = time.time()
    return end_time - start_time
