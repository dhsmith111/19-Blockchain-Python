import subprocess
import json

# for getting local .env mneumonic
import os
from dotenv import load_dotenv

# import bit, web3, etc to leverage keys in coins object later
from bit import wif_to_key, PrivateKeyTestnet
from bit.network import NetworkAPI
from eth_account import Account
from web3 import Web3

# Below ommited as geth was not used in favor of ganache
# from web3.middleware import geth_poa_middleware

# load local constants.py file
from constants import *

# Define functions
def derive_wallets(mnemonic, coin, derive_count=5): 
    """
    Returns a list of wallet keys(dict).  wallet coin type speficied in coin (str), in quantity derive_count (int), using mnemonic (str) as seed.
    """
    
    # Create string for command to be passed to subprocess shell using mnemonic, coin, and derive_count
    command = f'php derive -g --mnemonic="{mnemonic}" --coin="{coin}" --numderive={derive_count} --format=json'

    # create prc subprocess object and call Popen, passing command variable which includes command parameters defined above
    prc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    # read data from STDOUT (set to output variable) and then wait for child process to terminate
    output, err = prc.communicate()
    prc_status = prc.wait()

    # parse output as JSON
    keys = json.loads(output)
    
    return keys


def priv_key_to_account(coin, priv_key):
    """
    return account object from private key string, based on coin (BTCTEST, ETC, etc. from constants.py)
    """
    # Determine coin type and return appropriate account/wallet object based on coin
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
        # return web3.eth.accounts.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    return


def create_tx(coin, account, to, amount):
    """
    For ETH coin, returns dict with to, from, value, gas, gasPrice, nonce, and chainID. Utilitizes web3.py functions.\n
    For BTCTEST coin, returns PrivateKeyTestNet.prepare_transaction with appropriate values.
    """
    # determine coin type
    if coin == ETH:
        # 'eth' coin type:
        # create gas estimate
        gasEst = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )

        # return raw ETH transaction info
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEst,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
    elif coin == BTCTEST:
        # 'btc-test' coin type:
        # return BTCTEST formed transaction
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    return


def send_tx(coin, account, to, amount):
    """
    Calls create_tx, signs the transaction, and sends to designated network based on coin type.
    Valid coin types from constants.py
    """
    
    # create raw unsigned transaction
    raw_tx = create_tx(coin, account, to, amount)
    
    # determine coin type
    if coin == ETH:
        # create signed_transaction object
        ETH_signed_tx = account.sign_transaction(raw_tx)
        
        # send signed raw transaction
        ETH_result = w3.eth.sendRawTransaction(ETH_signed_tx.rawTransaction)
        return ETH_result.hex()

    elif coin == BTCTEST:
        # create, sign, and broadcast BTCTEST transaction
        # tx_hash = my_key.send([('mkH41dfD4S8DEoSfcVSvEfpyZ9siogWWtr', 1, 'usd')])
        BTCTEST_signed_tx = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(BTCTEST_signed_tx)
    return


# Run below when wallet.py is imported

# get mnemonic from .env, else use statically defined alternate mnemonic value
load_dotenv()
mnemonic = os.getenv('MNEMONIC', 'torch floor member tube relax tomorrow museum sample swamp arch furnace burden')

# Create Web3 object and connect to local ETH test chain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# create cointypes list using coin constants, set num of addresses to generate for each cointype
cointypes = [ETH, BTCTEST]
address_count = 3

# init coins dict to cointain wallets of cointypes
coins = {}

# populate coins object with wallets generated with derive_wallets function for each cointype in cointypes
for cointype in cointypes:
    coins[cointype] = derive_wallets(mnemonic, cointype, address_count)

# print out coins info in friendly indented format for visual reference
print(json.dumps(coins, indent=4))







    