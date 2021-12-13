import aiohttp


async def get(url, headers=None, data=None, res_method=""):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, data=data) as response:
            if res_method == "text":
                return await response.text()
            elif res_method == "json":
                return await response.json()
            else:
                return await response.read()


async def post(url, headers=None, data=None, res_method=""):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if res_method == "text":
                return await response.text()
            elif res_method == "json":
                return await response.json()
            else:
                return await response.read()


async def put(url, headers=None, data=None, res_method=""):
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, data=data) as response:
            if res_method == "text":
                return await response.text()
            elif res_method == "json":
                return await response.json()
            else:
                return await response.read()


async def delete(url, headers=None, data=None, res_method=""):
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers, data=data) as response:
            if res_method == "text":
                return await response.text()
            elif res_method == "json":
                return await response.json()
            else:
                return await response.read()


async def patch(url, headers=None, data=None, res_method=""):
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, data=data) as response:
            if res_method == "text":
                return await response.text()
            elif res_method == "json":
                return await response.json()
            else:
                return await response.read()
