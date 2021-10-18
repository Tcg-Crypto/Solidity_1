
from brownie import interface, accounts, network, config

def get_weth():
    account = accounts.load("study-account2")
    if network.show_active() in ["mainnet-fork-alc"]:
        account = accounts[0]
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account,"value": 0.1 * 10**18})
    print("Received 0.1 weth")


def main():
    get_weth()
