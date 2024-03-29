import asyncio

import aiohttp
from eth_abi import encode, decode  # type: ignore


async def ping(session: aiohttp.ClientSession) -> None:
    async with session.get("http://127.0.0.1:3000/") as response:
        print(await response.text())


async def post_directly_web2(session: aiohttp.ClientSession) -> None:
    async with session.post(
        "http://127.0.0.1:3000/service_output",
        json={
            "source": 1,
            "data": {"input": [[1.0380048, 0.5586108, 1.1037828, 1.712096]]},
        },
    ) as response:
        print(await response.json())


async def post_directly_web3(session: aiohttp.ClientSession) -> None:
    async with session.post(
        "http://127.0.0.1:3000/service_output",
        json={
            "source": 0,
            "data": encode(
                ["uint256[]"], [[1_038_004, 558_610, 1_103_782, 1_712_096]]
            ).hex(),
        },
    ) as response:
        print(await response.text())
        result = await response.json()
        output = result["raw_output"]
        result = decode(["uint256[]"], bytes.fromhex(output))[0]
        print(f"result: {result}")


# async maine
async def main(session: aiohttp.ClientSession) -> None:
    await post_directly_web3(session)


if __name__ == "__main__":
    # run main async

    async def provide_session() -> None:
        async with aiohttp.ClientSession() as session:
            await main(session)

    asyncio.run(provide_session())
