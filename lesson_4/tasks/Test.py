@staticmethod
    async def get_network_with_usdc(private_key1) -> Networks:
        # Create Client for WEB3 work
        all_networks = [
            Networks.Ethereum,
            Networks.Arbitrum,
            Networks.Polygon,
            Networks.Avalanche,
            Networks.BSC,
            Networks.Optimism,
            Networks.CoinBase,
        ]

        client = Client(private_key=private_key1, network=all_networks[2])

        for i in all_networks[0:6]:
            # Balance Checker
            token_address = await client.contracts.default_token(
                        contract_address=Stargate.contract_data[client.network.name]['usdc_contract'].address)
            symbol = await token_address.functions.symbol().call()
            amount = await client.wallet.balance(token=token_address.address)
            logger.info(f'{client.account.address}In {client.network.name} you have {amount.Ether}{symbol}')

        return logger.success(f'In {client.network.name} you have the greatest amount of {amount.Ether} {symbol}')



'''
Function: bridge(address token,uint256 amountLD,address to,tuple callParams,bytes adapterParams)

MethodID: 0xfe359a0d
[0]:  00000000000000000000000055d398326f99059ff775485246999027b3197955
[1]:  00000000000000000000000000000000000000000000000016345785d8a00000
[2]:  0000000000000000000000007e87852b24271d9b1ceab796ad97d40562e4c7ae
[3]:  0000000000000000000000007e87852b24271d9b1ceab796ad97d40562e4c7ae
[4]:  0000000000000000000000000000000000000000000000000000000000000000
[5]:  00000000000000000000000000000000000000000000000000000000000000c0
[6]:  0000000000000000000000000000000000000000000000000000000000000000


Function: bridge(address, uint256, address, (address,address), bytes)    
#	Name	                              Type	                                  Data
1	token	                              address     	                          0x55d398326f99059fF775485246999027B3197955
2	amountLD	                          uint256 	                              1600000000000000000
3	to	                                  address	                              0x7E87852b24271D9b1CEAB796AD97d40562e4c7AE
3	callParams.refundAddress	          address                                 0x7E87852b24271D9b1CEAB796AD97d40562e4c7AE
3	callParams.zroPaymentAddress          address	                              0x0000000000000000000000000000000000000000
5	adapterParams	                      bytes	                                  0x
'''