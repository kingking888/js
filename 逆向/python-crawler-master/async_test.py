# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/3/2
# @File     : async_test.py
# @Software : PyCharm
import asyncio
import uvloop
import time

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def test(sec):
    print('任务进入时间: ', time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()))
    await asyncio.sleep(sec)
    print('任务完成时间:', time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()))


async def run():
    task = []
    for i in range(5):
        loop = asyncio.create_task(test(i+1))
        task.append(loop)

    # 先进入事件循环test函数的先运行,之后在响应run函数
    # await asyncio.sleep(2)
    # for t in task:
    #     await t

    # await后运行test函数
    time.sleep(10)

if __name__ == '__main__':
    asyncio.run(run())
