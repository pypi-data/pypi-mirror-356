#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2025/6/18 16:34
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI

base_url = "https://api.gptgod.online"


# {
#     "prompt": "牛飞上天了",
#     "model": "veo2-fast",
#     "enhance_prompt": true
# }
async def create_task(
        request: dict,
        api_key: Optional[str] = None

):
    payload = request
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    response = client.post(
        "/v1/video/create",
        body=payload,
        cast_to=dict,
    )
    return response


if __name__ == '__main__':
    payload = {
        "prompt": "牛飞上天了",
        "model": "veo2-fast",
        "images": [
            "https://filesystem.site/cdn/20250612/VfgB5ubjInVt8sG6rzMppxnu7gEfde.png",
            "https://filesystem.site/cdn/20250612/998IGmUiM2koBGZM3UnZeImbPBNIUL.png"
        ],
        "enhance_prompt": True
    }

    arun(create_task(payload))
