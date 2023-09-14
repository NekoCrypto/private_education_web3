import csv
from data.config import IMPORT_PATH

# Define the path to the CSV file
csv_file_path = IMPORT_PATH

# Open the CSV file for reading
with open(csv_file_path, 'r', newline='') as csv_file:
    # Create a CSV reader
    csv_reader = csv.reader(csv_file)

    # Skip the header row (if it exists)
    next(csv_reader)

    # Iterate over the rows using a for loop
    for row in csv_reader:
        private_key = row[0]
        name = row[1]
        proxy = row[2]

        # Process the data for each row
        print(f"Private Key: {private_key}, Name: {name}, Proxy: {proxy}")

import random
from loguru import logger

from py_eth_async.client import Client

from data.models import Settings
from data.config import IMPORT_PATH
from utilss.files_utils import get_initial_data_from_csv_file
from db_api.database import db, get_wallet
from db_api.models import Wallet


class Import:
    @staticmethod
    def wallets() -> None:
        print(f'''Open and fill in the {IMPORT_PATH}.\n''')
        input(f'Then press Enter.')
        data = get_initial_data_from_csv_file(path=IMPORT_PATH)
        for wallet_data in data:
            private_key = wallet_data[0]
            name = wallet_data[1]
            proxy = wallet_data[2]

            print(f"Private Key: {private_key}, Name: {name}, Proxy: {proxy}")


# Call the wallets() method to initiate the data import and printing
# Import.wallets()
#
# N	address										name				proxy	stargate_swaps	coredao_swaps	uniswap_geth_amount	testnetbridge_swaps
# 1	0xeE3c73D22e145695b4019de3CA18cAAF9b52Fec8	Olga Alexandrovna	olga:0123456@127.11.101.08	    15	5	5.0000000000	9