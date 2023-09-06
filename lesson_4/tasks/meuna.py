import asyncio
import random
import time
from typing import Optional

import fake_useragent
from web3.types import TxParams
from web3.contract import AsyncContract
from py_eth_async.data.models import RawContract

from tasks.base import Base
from py_eth_async.data.models import TxArgs, TokenAmount
from py_eth_async.data.models import Networks
from py_eth_async.client import Client

import requests
from data.config import logger
from data.models import Contracts


class Meuna(Base):
    contract_data = {
        Networks.Bsctestnet.name: {
            'request_contract': Contracts.MEUNA_HAY_REQUEST,
            'router_contract': Contracts.MEUNA_ROUTER,
            'erc20mock_contract': Contracts.MEUNA_ERC20MOCK,
            'erc20mock_pool_contract': Contracts.MEUNA_ERC20MOCK_POOL,
            'pair_contract': Contracts.MEUNA_PAIR,
            'staiking_contract': Contracts.MEUNA_STAIKING,
            'mint_test_contract': Contracts.MEUNA_MINT_SYNTEST3,
            'hay_contract': Contracts.MEUNA_HAY,
            'mapple': Contracts.MEUNA_MAPPLE,
            'mamzn': Contracts.MEUNA_MAMZN,
            'mxau': Contracts.MEUNA_MXAU,
            'mhkd': Contracts.MEUNA_MHKD,
            'maed': Contracts.MEUNA_MAED,
        },
    }

    async def request_hay_meuna(
            self
    ):
        failed_text = f'Failed request {self.client.network.name} HAY via Meuna'

        request_contract = await self.client.contracts.get(
            contract_address=Meuna.contract_data[self.client.network.name]['request_contract'].address,
            abi=Contracts.MEUNA_HAY_REQUEST.abi)

        logger.info(
            f'{self.client.account.address} | MEUNA | '
            f'request HAY from {self.client.network.name} | Meuna')

        tx_params = TxParams(
            to=request_contract.address,
            data=request_contract.encodeABI('claim', args=()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'Request HAY was done from {self.client.network.name} | Meuna via BSC Testnet: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_meuna(
            self,
            # amount: Optional[TokenAmount] = None,
            # # to_token: str,
            # slippage: float = 1,
            # max_fee = 1,
    ):
        router_contract = await self.client.contracts.get(
            contract_address=Contracts.MEUNA_ROUTER.address,
            abi=Contracts.MEUNA_ROUTER.abi
        )

        from_token_name = Meuna.contract_data[self.client.network.name]['hay_contract'].address
        to_token_name = Meuna.contract_data[self.client.network.name]['mapple'].address
        print(to_token_name)

        # if await self.approve_interface(
        #         token_address='0x0970C29D31bFcd7ebF803B6C879B36f69fC39f28',
        #         spender='0x0970C29D31bFcd7ebF803B6C879B36f69fC39f28',
        #         amount=100000000000000000000
        # ):
        #     await asyncio.sleep(random.randint(5, 10))
        # else:
        #     return f' | can not approve'

        amount = 2000000000000000000
        min_amount = await self.get_value(amount=amount, from_token=from_token_name, to_token=to_token_name)

        args = TxArgs(
            amountIn=amount,
            amountOutMin=min_amount,
            path=[str(from_token_name), str(to_token_name)],
            to=self.client.account.address,
            deadline=int(time.time() + 60 * 5),
        )

        tx_params = TxParams(
            to=router_contract.address,
            data=router_contract.encodeABI('swapExactTokensForTokens', args=args.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount} {from_token_name} was swaped to {to_token_name} via Meuna: {tx.hash.hex()}'

        return f'failed_text!'

    @staticmethod
    async def get_value(amount: int, from_token: str, to_token: str) -> Optional[TokenAmount]:
        client = Client(network=Networks.Bsctestnet)
        contract = await client.contracts.get(
            contract_address=Contracts.MEUNA_ROUTER.address,
            abi=Contracts.MEUNA_ROUTER.abi
        )
        res = await contract.functions.getAmountsOut(
            amount,
            [from_token,
             to_token]
        ).call()
        return res[1]

    async def swap_meuna2(
            self,
            # to_network_name: str,
            amount: Optional[TokenAmount] = None,
            # slippage: float = 0.5,
            # max_fee: float = 1
    ):
        router_contract = await self.client.contracts.get(
            contract_address=Contracts.MEUNA_ROUTER.address,
            abi=Contracts.MEUNA_ROUTER.abi
        )

        from_token_name = Meuna.contract_data[self.client.network.name]['hay_contract'].address
        to_token_name = Meuna.contract_data[self.client.network.name]['mhkd'].address

        # if not amount:
        #     amount = await self.client.wallet.balance(token=to_token_name.address)

        logger.info(
            f'{self.client.account.address} | Stargate | '
            f'Swap| amount: {amount.Ether}')

        min_amount = await self.get_value(amount=amount.Wei, from_token=from_token_name, to_token=to_token_name)
        args = TxArgs(
            amountIn=amount.Wei,
            amountOutMin=int(min_amount),
            path=[str(from_token_name), str(to_token_name)],
            to=self.client.account.address,
            deadline=int(time.time() + 60 * 5),
        )

        native_balance = await self.client.wallet.balance()
        logger.info(f'Native Balance is {native_balance.Ether}')

        if await self.approve_interface(
                token_address=Contracts.MEUNA_HAY.address,
                spender=Contracts.MEUNA_ROUTER,
                amount=await self.client.wallet.balance(token=to_token_name)
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'can not approve'

        tx_params = TxParams(
            to=router_contract.address,
            data=router_contract.encodeABI('swapExactTokensForTokens', args=args.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swaped to {to_token_name} via Meuna: {tx.hash.hex()}'

        return f'failed_text!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'


    async def pool_meuna(
            self,
            # to_network_name: str,
            amount: Optional[TokenAmount] = None,
            # slippage: float = 0.5,
            # max_fee: float = 1
    ):
        router_contract = await self.client.contracts.get(
            contract_address=Contracts.MEUNA_ROUTER.address,
            abi=Contracts.MEUNA_ROUTER.abi
        )

        from_token_name = Meuna.contract_data[self.client.network.name]['hay_contract'].address
        to_token_name = Meuna.contract_data[self.client.network.name]['mhkd'].address

        # if not amount:
        #     amount = await self.client.wallet.balance(token=to_token_name.address)

        logger.info(
            f'{self.client.account.address} | Stargate | '
            f'Swap| amount: {amount.Ether}')

        min_amount = await self.get_value(amount=amount.Wei, from_token=from_token_name, to_token=to_token_name)
        args = TxArgs(
            amountIn=amount.Wei,
            amountOutMin=int(min_amount),
            path=[str(from_token_name), str(to_token_name)],
            to=self.client.account.address,
            deadline=int(time.time() + 60 * 5),
        )

        native_balance = await self.client.wallet.balance()
        logger.info(f'Native Balance is {native_balance.Ether}')

        if await self.approve_interface(
                token_address=Contracts.MEUNA_HAY.address,
                spender=Contracts.MEUNA_ROUTER,
                amount=await self.client.wallet.balance(token=to_token_name)
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'can not approve'

        tx_params = TxParams(
            to=router_contract.address,
            data=router_contract.encodeABI('swapExactTokensForTokens', args=args.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swaped to {to_token_name} via Meuna: {tx.hash.hex()}'

        return f'failed_text!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'
