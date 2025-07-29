from ooga_booga_python.client import OogaBoogaClient
import asyncio
from dotenv import load_dotenv
import os

from ooga_booga_python.models import SwapParams

# Load environment variables from the .env file
load_dotenv()


async def approve_allowance(client: OogaBoogaClient):
    token = "0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce"
    approval_response = await client.approve_allowance(token)
    print(f"Approval transaction: {approval_response}")


async def perform_swap(client: OogaBoogaClient):
    swap_params = SwapParams(
        tokenIn="0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        amount=1000000000000000000000,  # 1 token in wei
        tokenOut="0x549943e04f40284185054145c6E4e9568C1D3241",
        to="0x98A79CF6288B27b2aBED90C73E2F3106DC234f43",
        slippage=0.02,
    )
    await client.swap(swap_params)


async def perform_swap_insufficient_balance(client: OogaBoogaClient):
    swap_params = SwapParams(
        tokenIn="0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        amount=10000000000000000000000000,  # 10000 token in wei
        tokenOut="0x549943e04f40284185054145c6E4e9568C1D3241",
        to="0x98A79CF6288B27b2aBED90C73E2F3106DC234f43",
        slippage=0.02,
    )
    await client.swap(swap_params)

async def perform_swap_slippage_too_high(client: OogaBoogaClient):
    swap_params = SwapParams(
        tokenIn="0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        amount=10000000000000000000000000,  # 10000 token in wei
        tokenOut="0x549943e04f40284185054145c6E4e9568C1D3241",
        to="0x98A79CF6288B27b2aBED90C73E2F3106DC234f43",
        slippage=2,
    )
    await client.swap(swap_params)


async def approve_allowance_invalid_token_address(client: OogaBoogaClient):
    token = "0xFCBD14DC51f0A4d49dasdasdasd0950e0bC26d0Dce"
    amount = "1000000000000000000000"  # 1 token in wei

    approval_response = await client.approve_allowance(token, amount)
    print(f"Approval transaction: {approval_response}")

async def main():
    client = OogaBoogaClient(
        api_key=os.getenv("OOGA_BOOGA_API_KEY"),
        private_key=os.getenv("PRIVATE_KEY")
    )
    # Example: Fetch token list
    await perform_swap_slippage_too_high(client)

asyncio.run(main())
