import asyncio
from loguru import logger

from functions.create_files import create_files
from functions.Import import Import
from data import config

from functions.initial import initial
from functions.activity import activity


async def test():
    from db_api.database import get_wallets
    from py_eth_async.client import Client
    from py_eth_async.client import Networks
    from data.models import zkSync
    from tasks.base import Base
    from tasks.mute import Mute
    from tasks.space_fi import SpaceFi
    from tasks.syncswap import SyncSwap
    from tasks.official_bridge import OfficialBridge
    from py_eth_async.data.models import TokenAmount

    wallet = get_wallets()[0]

    # client = Client(private_key=wallet.private_key, network=Networks.Ethereum)
    client = Client(private_key=wallet.private_key, network=zkSync)

    base = Base(client=client)

    # await base.get_token_info(contract_address='0x80115c708e12edd42e504c1cd52aea96c547c05c')
    # Base.parse_params('0xeb672419000000000000000000000000f76d5879ebe6cdf5dc7d89af0b233f9a0cf49fb800000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000bf39400000000000000000000000000000000000000000000000000000000000003200000000000000000000000000000000000000000000000000000000000000100000000000000000000000000f76d5879ebe6cdf5dc7d89af0b233f9a0cf49fb800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    # mute = Mute(client=client)
    # print(await mute.swap_eth_to_usdc())
    # print(await mute.swap_usdc_to_eth())

    # space_fi = SpaceFi(client=client)
    # print(await space_fi.swap_eth_to_usdc())
    # print(await space_fi.swap_usdc_to_eth())

    # sync_swap = SyncSwap(client=client)
    # print(await sync_swap.swap_eth_to_usdc())
    # print(await sync_swap.swap_usdc_to_eth())

    # bridge_eth = OfficialBridge(client=client)
    # print(await bridge_eth.send_eth_to_zksync(amount=TokenAmount(0.00043)))
    # print(await bridge_eth.send_eth_from_zksync(amount=TokenAmount(0.000043)))


async def start_script():
    await asyncio.wait([
        asyncio.create_task(initial()),
        asyncio.create_task(activity()),
    ])


async def start_okx_withdraw():
    pass


if __name__ == '__main__':
    create_files()
    print(f'''Select the action:
1) Import wallets from the {config.IMPORT_PATH} to the DB;
2) OKX Withdraw 
3) Start the script;
4) Exit.''')

    try:
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        action = int(input('> '))
        if action == 1:
            Import.wallets()
        elif action == 2:
            loop.run_until_complete(start_okx_withdraw())
        elif action == 3:
            loop.run_until_complete(start_script())
        elif action == 4:
            loop.run_until_complete(test())
        else:
            exit(1)

    except KeyboardInterrupt:
        print()

    # except ValueError:
    #     print(f"You didn't enter a number!")

    except BaseException as e:
        logger.exception('main')
        print(f'\nSomething went wrong: {e}\n')
