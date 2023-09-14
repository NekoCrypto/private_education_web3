import asyncio
from loguru import logger

from py_eth_async.data.models import Networks, TokenAmount
from py_eth_async.client import Client

from data.models import Contracts
# from tasks.stargate import Stargate
from tasks.corebridge import CoreDao
# from tasks.testnetbridge import OFT
from tasks.meuna import Meuna

from data.private_data import private_key1
from tasks.woofi import WooFi


async def main():
    client = Client(private_key=private_key1, network=Networks.Bsctestnet)
    # stargate = Stargate(client=client)
    # coredao = CoreDao(client=client)
    # oft = OFT(client=client)

    meuna = Meuna(client=client)
    # status = await meuna.request_hay_meuna()
    status = await meuna.swap_meuna2(amount=TokenAmount(2.78))

    if 'Failed' in status:
        logger.error(status)
    else:
        logger.success(status)
    # Balance Checker (USDC and USDT)
    # balance = await stargate.get_network_with_usdc(private_key1)
    # print(balance)
    #
    # # Stargate Swap from OPT to BSC
    # status = await stargate.send_usdc_from_optimism_to_usdt_bsc(
    #     amount=TokenAmount(2, decimals=6),
    #     max_fee=1.1)
    #
    # # CoreBridge Swap from BSC to CoreDao
    # status = await coredao.send_usdt_from_bsc_to_usdt_coredao(amount=TokenAmount(0.5))
    #
    # if 'Failed' in status:
    #     logger.error(status)
    # else:
    #     logger.success(status)
    #
    # CoreBridge Swap from CoreDao to BSC
    # status = await coredao.send_usdt_from_core_to_usdt_bsc(amount=TokenAmount(0.5))
    #
    # if 'Failed' in status:
    #     logger.error(status)
    # else:
    #     logger.success(status)
    #
    #
    # # Testnet Bridge from Arbitrum to Goerli
    # status = await oft.bridge_geth_from_arbitrum_to_geth_goerli(amount=TokenAmount(0.8))
    #
    # if 'Failed' in status:
    #     logger.error(status)
    # else:
    #     logger.success(status)















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
    #     contract=Contracts.MEUNA_ROUTER,
    #     input_data='0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000d02ab486cedc00000000000000000000000000000000000000000000000000000071a6f10be94c88'
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
