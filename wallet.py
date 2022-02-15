import time
import json
import consts as c
import requests
from web3 import Web3, HTTPProvider

wallet_address = c.WALLET

url = c.HOST

w3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com/"))


balance = w3.eth.get_balance(wallet_address)

print(balance)

balances = {}

def getBalances():
    for k, t in c.TOKENS.items():
        contract_address = w3.toChecksumAddress(t)
        # print(contract_address)
        # url_eth = "https://api.bscscan.com/api"
        url_eth = 'https://api.polygonscan.com/api'
        # url_eth = 'https://mumbai.polygonscan.com/api'
        # url_eth = 'https://localhost:4000/api'
        # contract_address = web3.toChecksumAddress(TokenAddress)
        API_ENDPOINT = url_eth+"?module=contract&action=getabi&address="+str(contract_address)
        # API_ENDPOINT = url+"?module=contract&action=getabi&address="+str(contract_address)
        # api_endpoint = f'''https://api.polygonscan.com/api
        #                 ?module=contract
        #                 &action=getabi
        #                 &address={str(contract_address)}'''
        # print(api_endpoint)
        r = requests.get(url=API_ENDPOINT)
        # print(r)
        response = r.json()
        # print(response)
        abi = json.loads(response['result'])
        # print(len(abi))
        # print(abi[0])
        contract = w3.eth.contract(address=contract_address, abi=abi)
        address = w3.toChecksumAddress(wallet_address)
        # totalSupply = contract.functions.totalSupply().call()
        # print(totalSupply)
        token_balance = contract.functions.balanceOf(address).call()
        
        print(k, token_balance)
        balances[k] = token_balance
        time.sleep(5)  #call rate limited without API key

def swap():
    swapParams = {
        'fromTokenAddress': None, 
        'toTokenAddress': w3.toChecksumAddress(c.DAI), 
        'amount': None,
    }

    quote_url = 'https://api.1inch.io/v4.0/137/quote'

    for k, t in c.TOKENS.items():
        contract_address = w3.toChecksumAddress(t)
        swapParams.update({
            'fromTokenAddress': contract_address, 
            'amount': str(balances[k]),
            'protocol': 'POLYGON_APESWAP'
        })
        
        r = requests.get(quote_url, params=swapParams)
        print(r.url)
        print(r.json())


getBalances()
swap()