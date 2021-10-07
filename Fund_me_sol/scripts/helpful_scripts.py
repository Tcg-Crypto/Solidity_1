
from brownie import accounts, network


LOCAL_ENVRONMENTS = ['development','ganache-local']
DECIMALS = 8
STARTING_PRICE = 200



def get_account():
    print (network.show_active())
    if network.show_active() in LOCAL_ENVRONMENTS or network.show_active() == "mainnet-fork-dev":
        return accounts[0]
    else:
        account = accounts.load("study-account2")
        return account