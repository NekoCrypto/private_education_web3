import asyncio
from typing import Optional
from loguru import logger
from decimal import Decimal

from web3.types import TxParams
from py_eth_async.data.models import Networks, TokenAmount, Unit, Ether
from py_eth_async.client import Client
from pretty_utils.miscellaneous.files import read_json
from py_eth_async.transactions import Tx

from tasks.woofi import WooFi
from data.models import Contracts
from data.config import ABIS_DIR
# from private_data import private_key1, proxy


async def swap(client, woofi, pair):
    if pair == 'ETH - USDT':
        await woofi.swap_eth_to_usdt(amount=0.0001)
    elif pair == 'USDT - ETH':
        await woofi.swap_usdt_to_eth()
    elif pair == 'ETH - WBTC':
        await woofi.swap_eth_to_wbtc(amount=0.00012)
    elif pair == 'WBTC - ETH':
        await woofi.swap_wbtc_to_eth()
    else:
        logger.info(f"You didn't choose any Pair to Swap")


async def main():
    client = Client(network=Networks.Arbitrum)

    trade_pairs = ["ETH - USDT", "ETH - WBTC", "USDT - ETH", "WBTC - ETH"]

    # Display available trade pairs to the user
    print("Please choose a pair to SWAP:")
    for index, pair in enumerate(trade_pairs, start=1):
        print(f"{index}. {pair}")

    # Get user's choice
    user_choice = int(input("Enter the number of the pair you want to choose: "))

    # Validate user's choice
    if 1 <= user_choice <= len(trade_pairs):
        selected_pair = trade_pairs[user_choice - 1]
        print("You have chosen:", selected_pair)

        await asyncio.sleep(2)

        logger.info(f'You choose to swap {selected_pair}')

        await swap(client, WooFi(client=Client), selected_pair)

    else:
        print("Invalid choice. Please choose a valid number.")
    # print(await client.contracts.get_signature(hex_signature='0x7dc20382'))
    # print(await client.contracts.parse_function(text_signature='swap(address,address,uint256,uint256,address,address)'))
    # print(await client.contracts.get_contract_attributes(contract=Contracts.ARBITRUM_USDC))
    # print(await client.contracts.get_abi(contract_address=Contracts.ARBITRUM_USDC.address))

    # contract = await client.contracts.get(
    #     contract_address=Contracts.ARBITRUM_WOOFI.address,
    #     abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    # )

    # print(await client.contracts.get_functions(contract=Contracts.ARBITRUM_USDC))

    # print((await client.wallet.balance()).Ether)
    # print(await client.wallet.nonce())

    # print((await client.transactions.gas_price(w3=client.w3)).Wei)
    # print(await client.transactions.max_priority_fee(w3=client.w3))

    # print(await client.transactions.decode_input_data(
    #     client=client,
    #     contract=Contracts.ARBITRUM_WOOFI,
    #     input_data='0x7dc20382000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000af88d065e77c8cc2239327c5edb3a432268e583100000000000000000000000000000000000000000000000000038d7ea4c6800000000000000000000000000000000000000000000000000000000000001be86500000000000000000000000069c1dc6d723f15d7ef8154ba7194977fcc90d85b00000000000000000000000069c1dc6d723f15d7ef8154ba7194977fcc90d85b'
    # ))

    # woofi = WooFi(client=client)
    # res = await woofi.swap_eth_to_usdc(amount=TokenAmount(amount=0.001))
    # res = await woofi.swap_usdc_to_eth()
    # if 'Failed' in res:
    #     logger.error(res)
    # else:
    #     logger.success(res)
    #
    # tx_hash = '0xf9bd50990974b8107a8ef1a2d2dc79c5de6114b42d5533827068ddccabe35240'
    # tx = Tx(tx_hash=tx_hash)
    # print(tx)
    # print(await tx.parse_params(client=client))
    # print(await tx.decode_input_data(client=client, contract=Contracts.ARBITRUM_WOOFI))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
