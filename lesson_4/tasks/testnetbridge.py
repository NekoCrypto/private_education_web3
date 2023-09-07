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


class OFT(Base):
    contract_data = {
        Networks.Arbitrum.name: {
            'geth_contract': Contracts.ARBITRUM_GETH_GOERLI,
            'bridge_contract': Contracts.TESTNET_BRIDGE_ARBITRUM,
        },
    }

    async def bridge_geth_from_arbitrum_to_geth_goerli(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        # Network Data
        to_network_name = Networks.Goerli.name
        from_network_name = Networks.Arbitrum.name
        failed_text = f'Failed to send {self.client.network.name} GETH to {to_network_name} GETH via TestNetBridge'

        # try:
        if self.client.network.name != Networks.Arbitrum.name:
            return f'{failed_text}: This feature only works from Arbitrum network'

        # Contract to work
        geth_contract = await self.client.contracts.default_token(
            contract_address=OFT.contract_data[self.client.network.name]['geth_contract'].address)
        bridge_contract = await self.client.contracts.get(
            contract_address=OFT.contract_data[self.client.network.name]['bridge_contract'],
            abi=Contracts.TESTNET_BRIDGE_ARBITRUM.abi
        )

        if not amount:
            amount = await self.client.wallet.balance(token=geth_contract.address)

        logger.info(
            f'{self.client.account.address} | TestNetBridge | '
            f'send GETH from {self.client.network.name} to {to_network_name} | amount: {amount.Ether}')

        # TX Arguments
        args = TxArgs(
            _from=self.client.account.address,
            _dstChainId=154,
            _toAddress=self.client.account.address,
            _amount=amount.Wei,
            _zroPaymentAddress=self.client.account.address,
            _refundAddress='0x0000000000000000000000000000000000000000',
            _adapterParams='0x',
        )

        value = await self.get_value(bridge_contract, 154, amount.Wei)

        if not value:
            return f'{failed_text} | can not get value ({self.client.network.name})'

        native_balance = await self.client.wallet.balance()
        if native_balance.Wei < value.Wei:
            return f'{failed_text}: To low native balance: balance: {native_balance.Ether}; value: {value.Ether}'

        token_price = await self.get_token_price(token=self.client.network.coin_symbol)
        network_fee = float(value.Ether) * token_price
        if network_fee > max_fee:
            return f'{failed_text} | too high fee: {network_fee} ({self.client.network.name})'

        tx_params = TxParams(
            to=bridge_contract.address,
            data=bridge_contract.encodeABI('sendFrom', args=args.tuple()),
            value=value.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return (f'{amount.Ether} GETH was send from {self.client.network.name} '
                    f'to {to_network_name} via TestNetBridge: {tx.hash.hex()}')
        return f'{failed_text}!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'

    async def get_value(self, router_contract: AsyncContract, dstchainid: str,
                        amount: int) -> Optional[TokenAmount]:
        res = await router_contract.functions.estimateSendFee(
            _dstChainId=dstchainid,
            _toAddress=self.client.account.address,
            _amount=amount,
            _useZro=False,
            _adapterParams='0x',
        ).call()
        return TokenAmount(amount=res[0], wei=True)
