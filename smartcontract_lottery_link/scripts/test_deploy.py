from brownie import accounts, config, network, Lottery
from scripts.helpful_scripts import get_account, get_contract

def deploy_lottery():
    VRF = "0xdD3782915140c8f3b190B5D67eAc6dc5760C46E9"
    
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        {"from":account}
    )

    print(lottery.getEntranceFee())


def main():
    deploy_lottery()