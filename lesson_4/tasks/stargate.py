import asyncio
import random
from typing import Optional
from web3.types import TxParams
from web3.contract import AsyncContract

from tasks.base import Base
from py_eth_async.data.models import TxArgs, TokenAmount
from py_eth_async.data.models import Networks
from py_eth_async.client import Client


from data.config import logger
from data.models import Contracts


class Stargate(Base):
    contract_data = {
        Networks.Ethereum.name: {
            'usdc_contract': Contracts.ETHEREUM_USDC,
            'stargate_contract': Contracts.ETHEREUM_STARGATE,
            'stargate_chain_id': 101,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Arbitrum.name: {
            'usdc_contract': Contracts.ARBITRUM_USDC_e,
            'stargate_contract': Contracts.ARBITRUM_STARGATE,
            'stargate_chain_id': 110,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Avalanche.name: {
            'usdc_contract': Contracts.AVALANCHE_USDC,
            'stargate_contract': Contracts.AVALANCHE_STARGATE,
            'stargate_chain_id': 106,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Polygon.name: {
            'usdc_contract': Contracts.POLYGON_USDC,
            'stargate_contract': Contracts.POLYGON_STARGATE,
            'stargate_chain_id': 109,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.BSC.name: {
            # USDC = USDT *** To to prevent mistakes
            'usdc_contract': Contracts.BSC_USDT,
            'stargate_contract': Contracts.BSC_STARGATE,
            'stargate_chain_id': 102,
            'src_pool_id': 1,
            'dst_pool_id': 2,
        },
        Networks.Optimism.name: {
            'usdc_contract': Contracts.OPTIMISM_USDC,
            'stargate_contract': Contracts.OPTIMISM_STARGATE,
            'stargate_chain_id': 111,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.CoinBase.name: {
            'usdc_contract': Contracts.BASE_USDbC,
            'stargate_contract': Contracts.BASE_STARGATE,
            'stargate_chain_id': 184,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
    }

    async def send_usdc(
            self,
            to_network_name: str,
            amount: Optional[TokenAmount] = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        failed_text = f'Failed to send {self.client.network.name} USDC to {to_network_name} USDC via Stargate'
        # try:
        if self.client.network.name == to_network_name:
            return f'{failed_text}: The same source network and destination network'

        usdc_contract = await self.client.contracts.default_token(
            contract_address=Stargate.contract_data[self.client.network.name]['usdc_contract'].address)
        stargate_contract = await self.client.contracts.get(
            contract_address=Stargate.contract_data[self.client.network.name]['stargate_contract'])

        if not amount:
            amount = await self.client.wallet.balance(token=usdc_contract.address)

        logger.info(
            f'{self.client.account.address} | Stargate | '
            f'send USDC from {self.client.network.name} to {to_network_name} | amount: {amount.Ether}')

        lz_tx_params = TxArgs(
            dstGasForCall=0,
            dstNativeAmount=0,
            dstNativeAddr='0x0000000000000000000000000000000000000001'
        )

        args = TxArgs(
            _dstChainId=Stargate.contract_data[to_network_name]['stargate_chain_id'],
            _srcPoolId=Stargate.contract_data[to_network_name]['src_pool_id'],
            _dstPoolId=Stargate.contract_data[to_network_name]['dst_pool_id'],
            _refundAddress=self.client.account.address,
            _amountLD=amount.Wei,
            _minAmountLD=int(amount.Wei * (100 - slippage) / 100),
            _lzTxParams=lz_tx_params.tuple(),
            _to=self.client.account.address,
            _payload='0x'
        )

        value = await self.get_value(
            router_contract=stargate_contract,
            to_network_name=to_network_name,
            lz_tx_params=lz_tx_params
        )
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
                token_address=usdc_contract.address,
                spender=stargate_contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | can not approve'

        tx_params = TxParams(
            to=stargate_contract.address,
            data=stargate_contract.encodeABI('swap', args=args.tuple()),
            value=value.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} USDC was send from {self.client.network.name} to {to_network_name} via Stargate: {tx.hash.hex()}'
        return f'{failed_text}!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'

    async def get_value(self, router_contract: AsyncContract, to_network_name: str,
                        lz_tx_params: TxArgs) -> Optional[TokenAmount]:
        res = await router_contract.functions.quoteLayerZeroFee(
            Stargate.contract_data[to_network_name]['stargate_chain_id'],
            1,
            self.client.account.address,
            '0x',
            lz_tx_params.list()
        ).call()
        return TokenAmount(amount=res[0], wei=True)

    async def send_usdc_from_avalanche_to_usdt_bsc(
            self,
            amount: Optional[TokenAmount] = None,
            dest_fee: Optional[TokenAmount] = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        failed_text = 'Failed to send Avalanche USDC to BSC USDT via Stargate'
        try:
            to_network_name = Networks.BSC.name
            if self.client.network.name != Networks.Avalanche.name:
                return f'{failed_text}: This feature only works from avalanche network'

            usdc_contract = await self.client.contracts.default_token(
                contract_address=Stargate.contract_data[self.client.network.name]['usdc_contract'].address)
            stargate_contract = await self.client.contracts.get(
                contract_address=Stargate.contract_data[self.client.network.name]['stargate_contract'])

            if not amount:
                await self.client.wallet.balance(token=usdc_contract.address)

            logger.info(
                f'{self.client.account.address} | Stargate | '
                f'send USDC from {self.client.network.name} to {to_network_name} | amount: {amount.Ether}')

            lz_tx_params = TxArgs(
                dstGasForCall=0,
                dstNativeAmount=dest_fee.Wei,
                dstNativeAddr=self.client.account.address
            )

            args = TxArgs(
                _dstChainId=Stargate.contract_data[to_network_name]['stargate_chain_id'],
                _srcPoolId=Stargate.contract_data[to_network_name]['src_pool_id'],
                _dstPoolId=Stargate.contract_data[to_network_name]['dst_pool_id'],
                _refundAddress=self.client.account.address,
                _amountLD=amount.Wei,
                _minAmountLD=int(amount.Wei * (100 - slippage) / 100),
                _lzTxParams=lz_tx_params.tuple(),
                _to=self.client.account.address,
                _payload='0x'
            )
            value = await self.get_value(
                router_contract=stargate_contract,
                to_network_name=to_network_name,
                lz_tx_params=lz_tx_params
            )
            if not value:
                return f'{failed_text} | can not get value ({self.client.network.name})'

            native_balance = await self.client.wallet.balance()
            if native_balance.Wei < value.Wei:
                return f'{failed_text}: To low native balance: balance: {native_balance.Ether}; value: {value.Ether}'

            token_price = await self.get_token_price(token=self.client.network.coin_symbol)
            dest_native_token_price = await self.get_token_price(token='BNB') # костыль
            dst_native_amount_dollar = float(dest_fee.Ether) * dest_native_token_price
            network_fee = float(value.Ether) * token_price
            if network_fee - dst_native_amount_dollar > max_fee:
                return f'{failed_text} | too high fee: {network_fee - dst_native_amount_dollar} ({self.client.network.name})'

            if await self.approve_interface(
                    token_address=usdc_contract.address,
                    spender=stargate_contract.address,
                    amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                return f'{failed_text} | can not approve'

            tx_params = TxParams(
                to=stargate_contract.address,
                data=stargate_contract.encodeABI('swap', args=args.tuple()),
                value=value.Wei
            )

            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
            if receipt:
                return f'{amount.Ether} USDC was send from {self.client.network.name} to {to_network_name} via Stargate: {tx.hash.hex()}'
            return f'{failed_text}!'

        except Exception as e:
            return f'{failed_text}: {e}'

    async def send_usdc_from_optimism_to_usdt_bsc(
            self,
            amount: Optional[TokenAmount] = None,
            # dest_fee: Optional[TokenAmount] = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        failed_text = 'Failed to send Optimism USDC to BSC USDT via Stargate'
        try:
            to_network_name = Networks.BSC.name
            if self.client.network.name != Networks.Optimism.name:
                return f'{failed_text}: This feature only works from avalanche network'

            usdc_contract = await self.client.contracts.default_token(
                contract_address=Stargate.contract_data[self.client.network.name]['usdc_contract'].address)
            stargate_contract = await self.client.contracts.get(
                contract_address=Stargate.contract_data[self.client.network.name]['stargate_contract'])

            if not amount:
                await self.client.wallet.balance(token=usdc_contract.address)

            logger.info(
                f'{self.client.account.address} | Stargate | '
                f'send USDC from {self.client.network.name} to {to_network_name} | amount: {amount.Ether}')


            lz_tx_params = TxArgs(
                dstGasForCall=0,
                dstNativeAmount=0,
                dstNativeAddr='0x0000000000000000000000000000000000000001'
            )

            args = TxArgs(
                _dstChainId=Stargate.contract_data[to_network_name]['stargate_chain_id'],
                _srcPoolId=Stargate.contract_data[to_network_name]['src_pool_id'],
                _dstPoolId=Stargate.contract_data[to_network_name]['dst_pool_id'],
                _refundAddress=self.client.account.address,
                _amountLD=amount.Wei,
                _minAmountLD=int(amount.Wei * (100 - slippage) / 100),
                _lzTxParams=lz_tx_params.tuple(),
                _to=self.client.account.address,
                _payload='0x'
            )
            value = await self.get_value(
                router_contract=stargate_contract,
                to_network_name=to_network_name,
                lz_tx_params=lz_tx_params
            )
            if not value:
                return f'{failed_text} | can not get value ({self.client.network.name})'

            native_balance = await self.client.wallet.balance()
            if native_balance.Wei < value.Wei:
                return f'{failed_text}: To low native balance: balance: {native_balance.Ether}; value: {value.Ether}'

            token_price = await self.get_token_price(token=self.client.network.coin_symbol)
            dest_native_token_price = await self.get_token_price(token='BNB')  # костыль

            # dst_native_amount_dollar = float(dest_fee.Ether) * dest_native_token_price
            network_fee = float(value.Ether) * token_price
            # if network_fee - dst_native_amount_dollar > max_fee:
            #     return f'{failed_text} | too high fee: {network_fee - dst_native_amount_dollar} ({self.client.network.name})'

            if await self.approve_interface(
                    token_address=usdc_contract.address,
                    spender=stargate_contract.address,
                    amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                return f'{failed_text} | can not approve'

            tx_params = TxParams(
                to=stargate_contract.address,
                data=stargate_contract.encodeABI('swap', args=args.tuple()),
                value=value.Wei
            )

            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
            if receipt:
                return f'{amount.Ether} USDC was send from {self.client.network.name} to {to_network_name} via Stargate: {tx.hash.hex()}'
            return f'{failed_text}!'

        except Exception as e:
            return f'{failed_text}: {e}'

    @staticmethod
    async def get_network_with_usdc(private_key1) -> Networks:
        # All Network for Stargate
        all_networks = [
            Networks.Ethereum,
            Networks.Arbitrum,
            Networks.Polygon,
            Networks.Avalanche,
            Networks.BSC,
            Networks.Optimism,
            # Networks.CoinBase,
        ]

        max_balance = 0
        network_with_max_balance = None
        max_balance_symbol = None

        for network in all_networks:
            # Create Client for WEB3 work
            client = Client(private_key=private_key1, network=network)

            # Balance Checker
            token_address = await client.contracts.default_token(
                        contract_address=Stargate.contract_data[client.network.name]['usdc_contract'].address)
            symbol = await token_address.functions.symbol().call()
            amount = await client.wallet.balance(token=token_address.address)
            logger.info(f'{client.account.address}In {client.network.name} you have {amount.Ether} {symbol}')

            if amount.Ether > max_balance:
                max_balance = amount.Ether
                network_with_max_balance = client.network.name
                max_balance_symbol = symbol

        return logger.success(f'In {network_with_max_balance} you have the greatest amount of {max_balance} {max_balance_symbol}')




