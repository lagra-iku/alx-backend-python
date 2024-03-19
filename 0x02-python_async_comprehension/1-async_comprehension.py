#!/usr/bin/env python3
"""
write a coroutine called async_comprehension that takes no arguments.
"""

import asyncio
import random
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension():
    """
    A coroutine called async_comprehension that takes no arguments.
    """
    random_numbers = [num async for num in async_generator()]
    return random_numbers
