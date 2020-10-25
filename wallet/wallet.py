import subprocess
import json

# load local constants.py file
from constants import *

# for getting local .env mneumonic
import os
from dotenv import load_dotenv
load_dotenv()

# # Starter Code
# command = 'php derive -g --mnemonic="torch floor member tube relax tomorrow museum sample swamp arch furnace burden" --cols=path,address,privkey,pubkey --format=json'

# p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
# output, err = p.communicate()
# p_status = p.wait()

# keys = json.loads(output)
# print(keys)

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


if __name__ == "__main__":
    # get MNEMONIC from .env, else use statically defined alternate mnemonic value
    mnemonic = os.getenv('MNEMONIC', 'junk person hello large abuse expire awful float useful dragon absorb hungry')
    
    # create cointypes list using coin constants, set num of addresses to generate for each cointype
    cointypes = [ETH, BTCTEST]
    address_count = 3

    # init coins dict object to cointain wallets of cointypes
    coins = {}

    # populate coins object with wallets generated with derive_wallets function for each cointype in cointypes
    for cointype in cointypes:
        coins[cointype] = derive_wallets(mnemonic, cointype, address_count)

    # # # testing display output in friendly format
    print(json.dumps(coins[ETH][2]['privkey'], indent=4))
    print(coins[ETH][2]['privkey'])

    