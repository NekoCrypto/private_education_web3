import asyncio
import random
from typing import Optional
from web3.types import TxParams
from web3.contract import AsyncContract

from tasks.base import Base
from py_eth_async.data.models import TxArgs, TokenAmount
from py_eth_async.data.models import Networks
from py_eth_async.client import Client

from data.private_data import private_key1

from data.config import logger
from data.models import Contracts


class CoreDao(Base):
    contract_data = {
        Networks.BSC.name: {
            'usdt_contract': Contracts.BSC_USDT,
            'core_contract': Contracts.BSC_CORE_BRIDGE,
        },
        Networks.CORE.name: {
            'usdt_contract': Contracts.CORE_BINACEPEG,
            'core_contract': Contracts.CORE_CORE_ROUTER
        }
    }

    async def send_usdt_from_bsc_to_usdt_coredao(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        to_network_name = Networks.CORE.name
        from_network_name = Networks.BSC.name
        failed_text = f'Failed to send {self.client.network.name} USDT to {to_network_name} USDT via CoreBridge'
        # try:
        if self.client.network.name != Networks.BSC.name:
            return f'{failed_text}: This feature only works from avalanche network'

        usdt_contract = await self.client.contracts.default_token(
            contract_address=CoreDao.contract_data[self.client.network.name]['usdt_contract'].address)
        core_dao_contract = await self.client.contracts.get(
            contract_address=CoreDao.contract_data[self.client.network.name]['core_contract'],
            abi=Contracts.BSC_CORE_BRIDGE.abi
        )

        if not amount:
            amount = await self.client.wallet.balance(token=usdt_contract.address)

        logger.info(
            f'{self.client.account.address} | CoreBridge | '
            f'send USDT from {self.client.network.name} to {to_network_name} | amount: {amount.Ether}')

        callparams = TxArgs(
            refundAddress=self.client.account.address,
            zroPaymentAddress='0x0000000000000000000000000000000000000000',
        )

        args = TxArgs(
            token=usdt_contract.address,
            amountLD=amount.Wei,
            to=self.client.account.address,
            callParams=callparams.tuple(),
            adapterParams='0x',
        )

        value = await self.get_value()

        if not value:
            return f'{failed_text} | can not get value ({self.client.network.name})'

        native_balance = await self.client.wallet.balance()
        if native_balance.Wei < value.Wei:
            return f'{failed_text}: To low native balance: balance: {native_balance.Ether}; value: {value.Ether}'

        token_price = await self.get_token_price(token=self.client.network.coin_symbol)
        network_fee = float(value.Ether) * token_price
        if network_fee > max_fee:
            return f'{failed_text} | too high fee: {network_fee} ({self.client.network.name})'

        if await self.approve_interface(
                token_address=usdt_contract.address,
                spender=core_dao_contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | can not approve'

        tx_params = TxParams(
            to=core_dao_contract.address,
            data=core_dao_contract.encodeABI('bridge', args=args.tuple()),
            value=value.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} USDT was send from {self.client.network.name} to {to_network_name} via CoreBridge: {tx.hash.hex()}'
        return f'{failed_text}!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'

    async def send_usdt_from_core_to_usdt_bsc(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        to_network_name = Networks.BSC.name
        from_network_name = Networks.CORE.name
        failed_text = f'Failed to send {self.client.network.name} USDT to {to_network_name} USDT via CoreBridge'
        # try:
        if self.client.network.name != Networks.CORE.name:
            return f'{failed_text}: This feature only works from avalanche network'

        usdt_contract = await self.client.contracts.default_token(
            contract_address=CoreDao.contract_data[self.client.network.name]['usdt_contract'].address)
        core_dao_contract = await self.client.contracts.get(
            contract_address=CoreDao.contract_data[self.client.network.name]['core_contract'],
            abi=Contracts.CORE_CORE_ROUTER.abi
        )

        if not amount:
            amount = await self.client.wallet.balance(token=usdt_contract.address)

        logger.info(
            f'{self.client.account.address} | CoreBridge | '
            f'send USDT from {self.client.network.name} to {to_network_name} | amount: {amount.Ether}')

        callparams = TxArgs(
            refundAddress=self.client.account.address,
            zroPaymentAddress='0x0000000000000000000000000000000000000000',
        )

        args = TxArgs(
            localToken=usdt_contract.address,
            remoteChainId='102',
            amountLD=amount.Wei,
            to=self.client.account.address,
            unwrapWeth=False,
            callParams=callparams.tuple(),
            adapterParams='0x',
        )

        value = await self.get_value()

        if not value:
            return f'{failed_text} | can not get value ({self.client.network.name})'

        native_balance = await self.client.wallet.balance()
        if native_balance.Wei < value.Wei:
            return f'{failed_text}: To low native balance: balance: {native_balance.Ether}; value: {value.Ether}'

        token_price = await self.get_token_price(token=self.client.network.coin_symbol)
        network_fee = float(value.Ether) * token_price
        if network_fee > max_fee:
            return f'{failed_text} | too high fee: {network_fee} ({self.client.network.name})'

        if await self.approve_interface(
                token_address=usdt_contract.address,
                spender=core_dao_contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | can not approve'

        tx_params = TxParams(
            to=core_dao_contract.address,
            data=core_dao_contract.encodeABI('bridge', args=args.tuple()),
            value=value.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} USDT was send from {self.client.network.name} to {to_network_name} via CoreBridge: {tx.hash.hex()}'
        return f'{failed_text}!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'
    @staticmethod
    async def get_value() -> Optional[TokenAmount]:
        client = Client(private_key=private_key1, network=Networks.BSC)
        contract = await client.contracts.get(
            contract_address=Contracts.BSC_CORE_BRIDGE.address,
            abi=Contracts.BSC_CORE_BRIDGE.abi
        )
        res = await contract.functions.estimateBridgeFee(False, '0x').call()
        return TokenAmount(amount=res[0], wei=True)
