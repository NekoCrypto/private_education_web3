import random
from loguru import logger

from py_eth_async.client import Client

from data.models import Settings
from data.config import IMPORT_PATH
from utilss.files_utils import get_initial_data_from_csv_file
from db_api.database import db, get_wallet
from db_api.models import Wallet, Base
from db_api.db import DB


class Import:
    @staticmethod
    def wallets() -> None:
        print(f'''Open and fill in the {IMPORT_PATH}.\n''')
        input(f'Then press Enter.')
        data = get_initial_data_from_csv_file(path=IMPORT_PATH)

        if data:
            settings = Settings()
            imported = []
            edited = []
            total = len(data)
            for wallet in data:
                try:
                    private_key = wallet.private_key

                    if not private_key:
                        print(f"You didn't specify one or more of the mandatory values: private_key!")
                        continue

                    if len(private_key) == 64 or private_key.startswith('0x') and len(private_key) == 66:
                        wallet_instance = get_wallet(private_key=private_key)
                        wallet_db = db.all(Wallet, Wallet.private_key.is_(private_key))
                        for wallet_read in wallet_db:
                            name_db = wallet_read.name
                            proxy_db = wallet_read.proxy
                            if name_db == wallet.name:
                                pass
                            else:
                                new_name = wallet.name
                                wallet = get_wallet(private_key=private_key)
                                wallet.name = new_name
                                db.commit()
                                edited.append(wallet)
                            if proxy_db == wallet.proxy:
                                pass
                            else:
                                new_proxy = wallet.proxy
                                wallet = get_wallet(private_key=private_key)
                                wallet.proxy = new_proxy
                                db.commit()
                                edited.append(wallet)

                        if not wallet_instance:
                            client = Client(private_key=private_key)
                            address = client.account.address
                            name = wallet.name
                            proxy = wallet.proxy
                            stargate_swaps = random.randint(
                                settings.stargate_swaps.from_, settings.stargate_swaps.to_)
                            coredao_swaps = random.randint(
                                settings.coredao_swaps.from_, settings.coredao_swaps.to_)
                            uniswap_geth_amount = random.randint(
                                settings.uniswap_geth_amount.from_, settings.uniswap_geth_amount.to_)
                            testnetbridge_swaps = random.randint(
                                settings.testnetbridge_swaps.from_, settings.testnetbridge_swaps.to_)
                            wallet_instance = Wallet(
                                private_key=private_key,
                                address=address,
                                name=name,
                                proxy=proxy,
                                stargate_swaps=stargate_swaps,
                                coredao_swaps=coredao_swaps,
                                uniswap_geth_amount=uniswap_geth_amount,
                                testnetbridge_swaps=testnetbridge_swaps
                            )
                            db.insert(wallet_instance)
                            imported.append(wallet_instance)

                except:
                    logger.exception('Import.wallets')
                    print(f'Failed to import wallet!')

            text = ''
            if imported:
                text += '\n--- Imported\nN\taddress\tname\tproxy\tstargate_swaps\tcoredao_swaps\tuniswap_geth_amount\ttestnetbridge_swaps'
                for i, wallet in enumerate(imported):
                    text += f'\n{i + 1}\t{wallet.address}\t{wallet.name}\t{wallet.proxy}\t{wallet.stargate_swaps}\t{wallet.coredao_swaps}\t{wallet.uniswap_geth_amount}\t{wallet.testnetbridge_swaps}'

                text += '\n'

            if edited:
                text += '\n--- Edited\nN\taddress\t\t\t\t\t\t\t\t\t\tname\t\t\tproxy\t\t\t\t\t\tstargate_swaps\tcoredao_swaps\tuniswap_geth_amount\ttestnetbridge_swaps'
                for i, wallet in enumerate(edited):
                    text += f'\n{i + 1}\t{wallet.address}\t{wallet.name}\t{wallet.proxy}\t{wallet.stargate_swaps}\t{wallet.coredao_swaps}\t{wallet.uniswap_geth_amount}\t{wallet.testnetbridge_swaps}'

                text += '\n'

            print(
                f'{text}\nDone! {len(imported)}/{total} wallets were imported, '
                f'info have been changed at {len(edited)}/{total}.'
            )

        else:
            print(f'There are no wallets on the file!')

