from pretty_utils.type_functions.classes import Singleton
from py_eth_async.data.models import RawContract, DefaultABIs
from pretty_utils.miscellaneous.files import read_json

from data.config import ABIS_DIR


class Contracts(Singleton):
    ARBITRUM_WOOFI = RawContract(
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30', abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    ARBITRUM_USDC = RawContract(
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831', abi=DefaultABIs.Token
    )

    ARBITRUM_USDC_e = RawContract(
        address='0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8', abi=DefaultABIs.Token
    )

    ARBITRUM_WBTC = RawContract(
        address='0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f', abi=DefaultABIs.Token
    )

    ARBITRUM_STARGATE = RawContract(
        address='0x53bf833a5d6c4dda888f69c22c88c9f356a41614', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    ARBITRUM_ETH = RawContract(
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', abi=DefaultABIs.Token
    )

    POLYGON_STARGATE = RawContract(
        address='0x45a01e4e04f14f7a4a6702c74187c5f6222033cd', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    POLYGON_USDC = RawContract(
        address='0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', abi=DefaultABIs.Token
    )

    AVALANCHE_STARGATE = RawContract(
        address='0x45a01e4e04f14f7a4a6702c74187c5f6222033cd', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    AVALANCHE_USDC = RawContract(
        address='0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E', abi=DefaultABIs.Token
    )

    OPTIMISM_STARGATE = RawContract(
        address='0xB0D502E938ed5f4df2E681fE6E419ff29631d62b', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    OPTIMISM_USDC = RawContract(
        address='0x7f5c764cbc14f9669b88837ca1490cca17c31607', abi=DefaultABIs.Token
    )

    ETHEREUM_STARGATE = RawContract(
        address='0x8731d54E9D02c286767d56ac03e8037C07e01e98', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    ETHEREUM_USDC = RawContract(
        address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', abi=DefaultABIs.Token
    )

    BASE_STARGATE = RawContract(
        address='0x45f1A95A4D3f3836523F5c83673c797f4d4d263B', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    BASE_USDbC = RawContract(
        address='0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA', abi=DefaultABIs.Token
    )

    BSC_STARGATE = RawContract(
        address='0x4a364f8c717cAAD9A442737Eb7b8A55cc6cf18D8', abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    BSC_USDT = RawContract(
        address='0x55d398326f99059ff775485246999027b3197955', abi=DefaultABIs.Token
    )

    BSC_CORE_BRIDGE = RawContract(
        address='0x52e75D318cFB31f9A2EdFa2DFee26B161255B233', abi=read_json(path=(ABIS_DIR, 'corebridge.json'))
    )

    CORE_BINACEPEG = RawContract(
        address='0x55d398326f99059fF775485246999027B3197955', abi=DefaultABIs.Token
    )

    CORE_CORE_ROUTER = RawContract(
        address='0x52e75D318cFB31f9A2EdFa2DFee26B161255B233', abi=read_json(path=(ABIS_DIR, 'corerouter.json'))
    )

    UNISWAP_ETHERIUM_ROUTER = RawContract(
        address='0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad', abi=read_json(path=(ABIS_DIR, 'universalrouter.json'))
    )

    ARBITRUM_GETH_GOERLI = RawContract(
        address='0xdD69DB25F6D620A7baD3023c5d32761D353D3De9', abi=DefaultABIs.Token
    )

    MEUNA_HAY_REQUEST = RawContract(
        address='0x67c03dbd6f8b377345d924726acdb5eb5192f63e', abi=read_json(path=(ABIS_DIR, 'meunarequesthay.json'))
    )

    MEUNA_ROUTER = RawContract(
        address='0x0970C29D31bFcd7ebF803B6C879B36f69fC39f28', abi=read_json(path=(ABIS_DIR, 'meunarouter.json'))
    )

    MEUNA_ERC20MOCK = RawContract(
            address='0xA0C6843CCC4F4219e3e5751D4F93dE17C303D658', abi=read_json(path=(ABIS_DIR, 'meunaerc20mock.json'))
    )

    MEUNA_ERC20MOCK_POOL = RawContract(
            address='0x47034b3c18f17dd89ce1d7f87b9a90235158e4cc', abi=read_json(path=(ABIS_DIR, 'meunaerc20mock.json'))
    )

    MEUNA_PAIR = RawContract(
            address='0xd7931924662d8086160b87d17622b23dff04d129', abi=read_json(path=(ABIS_DIR, 'meunapair.json'))
    )

    MEUNA_STAIKING = RawContract(
            address='0x65cbe6bdc2b07b2e25ef6b53a97899fd4b4f1a8b', abi=read_json(path=(ABIS_DIR, 'stakingcontract.json'))
    )

    MEUNA_MINT_SYNTEST3 = RawContract(
            address='0xb45f6db83bbde9b6aa1dbc688b27c5c2defd6ad0', abi=read_json(path=(ABIS_DIR, 'mintsyntest3.json'))
    )

    MEUNA_HAY = RawContract(
            address='0xA0C6843CCC4F4219e3e5751D4F93dE17C303D658', abi=DefaultABIs.Token
    )

    MEUNA_MAPPLE = RawContract(
            address='0x47034B3c18f17dd89CE1d7F87B9A90235158E4CC', abi=DefaultABIs.Token
    )

    MEUNA_MAMZN = RawContract(
            address='0x5744235b2D4b5e82a0F65a6aC599C50ffB805f75', abi=DefaultABIs.Token
    )

    MEUNA_MXAU = RawContract(
            address='0x3fae7eC38e169a04ca1F0c3001710a4b3AB62ab8', abi=DefaultABIs.Token
    )

    MEUNA_MHKD = RawContract(
            address='0x5C8B2B5F1a57562a66293e59752e1AaAa220A133', abi=DefaultABIs.Token
    )

    MEUNA_MAED = RawContract(
            address='0x59955AB2358b5b8f2eb9a6892a9F529a7b79820D', abi=DefaultABIs.Token
    )

    MEUNA_MULTICALL3 = RawContract(
            address='0xb45f6db83bbde9b6aa1dbc688b27c5c2defd6ad0', abi=read_json(path=(ABIS_DIR, 'multicall3.json'))
    )