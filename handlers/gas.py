from web3 import Web3
from web3.middleware import geth_poa_middleware

def get_gas_price_gwei():
    w3 = Web3(Web3.HTTPProvider("https://scroll-mainnet.chainstacklabs.com"))

    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    gas_price = w3.eth.gas_price

    gas_price_gwei = w3.from_wei(gas_price, 'gwei')

    return gas_price_gwei
