SpaceFiABI = [
    {
        'constant': False,
        'inputs': [
            {'name': 'amountOut', 'type': 'uint256'},
            {'name': 'paths', 'type': 'address[]'},
            {'name': 'to', 'type': 'address'},
            {'name': 'deadline', 'type': 'uint256'},
        ],
        'name': 'swapEthToToken',
        'outputs': [],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }
]
'''

Function: withdraw(address _l1Receiver)   0x51cff8d9

_l1Receiver	address	0xF76d5879EbE6CDf5dc7d89aF0b233F9A0cf49fB8

0123456789012345678901234567890123456789012345678901234567891234
000000000000000000000000f76d5879ebe6cdf5dc7d89af0b233f9a0cf49fb8 - address

Value = 0.00001 ETH $0.02

contract  =  0x000000000000000000000000000000000000800A



'''
swapExactTokensForETH
params = TxArgs(
    amountIn=token_balance.Wei,
    amountOut=amount_out_min.Wei,
    path=[from_token.address, Contracts.WETH.address],
    to=self.client.account.address,
    deadline=int(time.time() + 20 * 60),
)

