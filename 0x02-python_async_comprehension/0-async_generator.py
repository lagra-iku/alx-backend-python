#!/usr/bin/env python3
"""
A coroutine called async_generator that takes no arguments.
"""

import asyncio
import random


async def async_generator():
    """
    The generator function
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.randint(0, 10)
