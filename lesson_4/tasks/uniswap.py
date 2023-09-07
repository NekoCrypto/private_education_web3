import asyncio
import random
from typing import Optional

import fake_useragent
from web3.types import TxParams
from web3.contract import AsyncContract

from tasks.base import Base
from py_eth_async.data.models import TxArgs, TokenAmount
from py_eth_async.data.models import Networks
from py_eth_async.client import Client

import requests
from data.config import logger
from data.models import Contracts


class Uniswap(Base):
    contract_data = {
        Networks.Arbitrum.name: {
            'universalrouter_contract': Contracts.UNISWAP_ETHERIUM_ROUTER,
        },
        Networks.Goerli.name: {
            'GETH_contract': Contracts.GETH_GOERLI,
        }
    }

    async def swap_eth_from_arbitrum_to_geth_goerli(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 0.5,
    ):
        # Network Data
        to_network_name = Networks.Goerli
        from_network_name = Networks.Arbitrum
        # from_token = Contracts.ARBITRUM_ETH
        # to_token = Contracts.GETH_GOERLI

        # Error Text
        failed_text = f'Failed to swap {self.client.network.name} ETH to {to_network_name} GETH via UNISWAP'
        # try:
        # Check if not same network to Swap
        if self.client.network.name != Networks.Arbitrum:
            return f'{failed_text}: This feature only works from avalanche network'

        # Getting Contracts Data
        geth_contract = await self.client.contracts.default_token(
            contract_address=Uniswap.contract_data[self.client.network.name]['GETH_contract'].address)
        uniswap_contract = await self.client.contracts.get(
            contract_address=Uniswap.contract_data[self.client.network.name]['universalrouter_contract'],
            abi=Contracts.UNISWAP_ETHERIUM_ROUTER
        )

        # Not Send Amount -> Then Swap Full Half Balance
        if not amount:
            amount = await self.client.wallet.balance(token=self.client.wallet.balance()) * 0.5

        # Info of the Swap
        logger.info(
            f'{self.client.account.address} | Uniswap | '
            f'swap ETH from {self.client.network.name} to {to_network_name} | amount: {amount.Ether}')

        inputs = ['0x0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000005b00e4b0ddc0x0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000016345785d8a0000000000000000000000000000000000000000000000000000000005b00e4b0ddc00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002bdd69db25f6d620a7bad3023c5d32761d353d3de90001f482af49447d8a07e3bd95bd0d56f35241523fbab10000000000000000000000000000000000000000000x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000']

        # Arrguments for TX
        args = TxArgs(
            commands='0x0b010c',
            inputs=inputs,
            deadline=,
        )

        # Amount
        value = amount

        if not value:
            return f'{failed_text} | can not get value ({self.client.network.name})'

        # Checker for Native Tokens
        native_balance = await self.client.wallet.balance()
        if native_balance.Wei < value.Wei:
            return f'{failed_text}: To low native balance: balance: {native_balance.Ether}; value: {value.Ether}'

        # Checking price for GETH
        token_price = await self.get_quote_eth_geth(value)

        # Encode all Argument for the TX
        tx_params = TxParams(
            to=uniswap_contract.address,
            data=uniswap_contract.encodeABI('execute', args=args.tuple()),
            value=value.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return (f'{amount.Ether} ETH was swapped from {self.client.network.name}'
                    f' to {to_network_name} via Uniswap: {tx.hash.hex()}')
        return f'{failed_text}!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'

    @staticmethod
    async def get_quote_eth_geth(amount) -> TokenAmount:
        user_agent = fake_useragent.UserAgent().random
        url = 'https://api.uniswap.org/v2/quote'

        headers = {
            'authority': 'api.uniswap.org',
            'accept': '*/*',
            'accept-language': 'en,ru;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://app.uniswap.org',
            'referer': 'https://app.uniswap.org/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': user_agent,
        }

        data = {
            "tokenInChainId": 42161,
            "tokenIn": str(Contracts.GETH_GOERLI.address),
            "tokenOutChainId": 42161,
            "tokenOut": "ETH",
            "amount": str(amount),
            "type": "EXACT_OUTPUT",
            "configs": [
                {
                    "protocols":
                        ["V2", "V3", "MIXED"],
                    "routingType":"CLASSIC",
                }
            ]
        }

        response = requests.post(url, headers=headers, data=data)
        return TokenAmount(response)
