from brownie import accounts, FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import get_account
from web3 import Web3

LOCAL_ENVRONMENTS = ['development','ganache-local']
DECIMALS = 8
STARTING_PRICE = 200



def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_ENVRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
        fund_me = FundMe.deploy(price_feed_address,{"from":account})
        print(f"Deployed to {fund_me.address}")
    else:
        print(f"Active Network: {network.show_active()}")
        print("::::Deploying Mocks:::")
        #if len(MockV3Aggregator) <= 0:
            #MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE , {"from": account})
        #price_feed_address = MockV3Aggregator[-1].address
    
    
    #fund_me = FundMe.deploy(price_feed_address,{"from":account})

    



def main():
    deploy_fund_me()