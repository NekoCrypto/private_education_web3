import asyncio
from loguru import logger

from py_eth_async.data.models import Networks, TokenAmount
from py_eth_async.client import Client

from data.models import Contracts
from tasks.stargate import Stargate
from tasks.corebridge import CoreDao
from tasks.testnetbridge import OFT

from data.private_data import private_key1
from tasks.woofi import WooFi


async def main():
    client = Client(private_key=private_key1, network=Networks.Arbitrum)
    stargate = Stargate(client=client)
    coredao = CoreDao(client=client)
    oft = OFT(client=client)
    #
    # Balance Checker (USDC and USDT)
    balance = await stargate.get_network_with_usdc(private_key1)
    print(balance)

    # Stargate Swap from OPT to BSC
    status = await stargate.send_usdc_from_optimism_to_usdt_bsc(
        amount=TokenAmount(2, decimals=6),
        max_fee=1.1)

    # CoreBridge Swap from BSC to CoreDao
    status = await coredao.send_usdt_from_bsc_to_usdt_coredao(amount=TokenAmount(0.5))

    if 'Failed' in status:
        logger.error(status)
    else:
        logger.success(status)

    CoreBridge Swap from CoreDao to BSC
    status = await coredao.send_usdt_from_core_to_usdt_bsc(amount=TokenAmount(0.5))

    if 'Failed' in status:
        logger.error(status)
    else:
        logger.success(status)


    # Testnet Bridge from Arbitrum to Goerli
    status = await oft.bridge_geth_from_arbitrum_to_geth_goerli(amount=TokenAmount(0.8))

    if 'Failed' in status:
        logger.error(status)
    else:
        logger.success(status)















    #
    # # status = await stargate.send_usdc(
    # #     to_network_name=Networks.Polygon.name,
    # #     amount=TokenAmount(0.5, decimals=6)
    # # )
    #
    # status = await stargate.send_usdc_from_avalanche_to_usdt_bsc(
    #     amount=TokenAmount(0.5, decimals=6),
    #     dest_fee=TokenAmount(0.005),
    #     max_fee=1.1
    # )
    # # $5.55
    # # $0.74
    #
    # # 3.27
    # # 1.89
    #
    # if 'Failed' in status:
    #     logger.error(status)
    # else:
    #     logger.success(status)
    #
    # res = await client.transactions.decode_input_data(
    #     client=client,
    #     contract=Contracts.UNISWAP_ROUTER,
    #     input_data='0x3593564c000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000064e5d16900000000000000000000000000000000000000000000000000000000000000030b010c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001e000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000005b00e4b0ddc00000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000016345785d8a0000000000000000000000000000000000000000000000000000000005b00e4b0ddc00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002bdd69db25f6d620a7bad3023c5d32761d353d3de90001f482af49447d8a07e3bd95bd0d56f35241523fbab1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000'
    # )
    # print(res)
    # for key, val in res[1].items():
    #     if isinstance(val, bytes):
    #         print(key, val.hex())
    #     elif isinstance(val, tuple):
    #         print(key, '(', end=' ')
    #         for item in val:
    #             if isinstance(item, bytes):
    #                 print(item.hex(), end=', ')
    #             else:
    #                 print(item, end=', ')
    #         print(')')
    #     else:
    #         print(key, val)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
