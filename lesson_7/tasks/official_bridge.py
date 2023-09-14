import time
import asyncio
import random
from typing import Optional

from web3.contract import AsyncContract
from web3.types import TxParams

from tasks.base import Base
from loguru import logger
from py_eth_async.data.models import Ether, TxArgs, TokenAmount
from pretty_utils.type_functions.floats import randfloat

from data.models import Settings, Contracts


class OfficialBridge(Base):
    async def send_eth_to_zksync(self, amount: Optional[TokenAmount] = None,) -> str:

        # All Data for Bridge
        failed_text = f'Failed bridge ETH to Zksync via Official Bridge'
        contract = await self.client.contracts.get(
            contract_address=Contracts.DIAMONDPROXY.address,
            abi=Contracts.DIAMONDPROXY.abi
        )

        # Balance Checker
        balance_eth = await self.client.wallet.balance()
        gas_price = await self.client.w3.eth.gas_price
        l2_gas_limit = 783252

        bridge_fee = await OfficialBridge.get_value(self, contract, gas_price, amount.Wei, l2_gas_limit)

        if balance_eth.GWei >= gas_price:
            logger.error(f'Not enough ETH Balance | {self.client.account.address}')

        if not amount:
            amount = balance_eth.Wei * 0.05

        params = TxArgs(
            _contractL2=self.client.account.address,
            _l2Value=amount.Wei,
            _calldata='',
            _l2GasLimit=l2_gas_limit,
            _l2GasPerPubdataByteLimit=800,
            _factoryDeps=[],
            _refundRecipient=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('requestL2Transaction', args=params.tuple()),
            value=amount.Wei + bridge_fee
        )
        self.parse_params(tx_params['data'])
        tx_params = await self.client.transactions.auto_add_params(tx_params=tx_params)

        print(tx_params)
        gas = await self.client.transactions.estimate_gas(w3=self.client.w3, tx_params=tx_params)

        return gas.Wei

        # tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        # receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        # if receipt:
        #     return f'{amount.Ether} ETH was bridged to ZKsync Official Bridge: {tx.hash.hex()}'
        # return f'{failed_text}!'

    async def send_eth_from_zksync(self, amount: Optional[TokenAmount] = None,) -> str:

        # All Data for Bridge
        failed_text = f'Failed bridge ETH from Zksync via Official Bridge'
        contract = await self.client.contracts.get(
            contract_address=Contracts.L2ETHTOKEN.address,
            abi=Contracts.L2ETHTOKEN.abi
        )

        # Balance Checker
        balance_eth = await self.client.wallet.balance()
        gas_price = await self.client.w3.eth.gas_price

        if balance_eth.GWei >= gas_price:
            logger.error(f'Not enough ETH Balance | {self.client.account.address}')

        if not amount:
            amount = balance_eth.Wei * 0.05

        params = TxArgs(_l1Receiver=self.client.account.address)

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('withdraw', args=params.tuple()),
            value=amount.Wei
        )
        self.parse_params(tx_params['data'])
        tx_params = await self.client.transactions.auto_add_params(tx_params=tx_params)

        for key, value in tx_params.items():
            print(f'{key}: {value}')
        gas = await self.client.transactions.estimate_gas(w3=self.client.w3, tx_params=tx_params)

        return gas.Wei

        # tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        # receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        # if receipt:
        #     return f'{amount.Ether} ETH was bridged to ZKsync Official Bridge: {tx.hash.hex()}'
        # return f'{failed_text}!'

    async def get_value(self, contract: AsyncContract, gas_price: int, amount: int, l2_gas_limit: int) -> int:
        res = await contract.functions.l2TransactionBaseCost(
            gas_price,
            l2_gas_limit,
            amount,

        ).call()
        return res
