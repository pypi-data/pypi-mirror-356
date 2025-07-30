# -*- coding: utf-8 -*-
"""
Created on 2025/6/15 19:42
@author: guest881
"""

from Decorators import *
@get_time()
@retry(3,0.5)
def fabonacci(n:int)->int:
    """生成斐波那契数列第N项"""
    if n<2:
        return n
    return fabonacci(n-1)+fabonacci(n-2)
fabonacci(1)
from requests import get
@get_time()
@cache(persist=True,file_path='cache.pkl')
def get_status(url):
    return get(url)
import asyncio
async def fetch_status(url:str)->dict:
   response=await asyncio.to_thread(get,url,None)
   return {"status":response.status_code,"url":url}
async def main()->None:
    Baidu_status,Apple_status=await asyncio.gather(
        fetch_status("https://www.baidu.com"),
        fetch_status("https://apple.com")
    )
    logger.info(f'{Baidu_status},{Apple_status}')
# asyncio.run(main=main())
print(numerize(1e5))


