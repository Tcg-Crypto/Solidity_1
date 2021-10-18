import brownie
from brownie import accounts, config, network, interface,chain
from scripts.get_weth import get_weth
from web3 import Web3

def approve_erc20(ammount, spender, erc20_address, account):
    print("ApprovingERC20")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, ammount,{"from": account})
    tx.wait(1)
    print("Approved")
    return tx

def get_asset_price(price_feed_address):
    asset_price_feed = interface.AggregatorV3Interface(price_feed_address)
    print("Price feed contrast is " + str(asset_price_feed))
    latest_price = asset_price_feed.latestRoundData()[1]
    price = Web3.fromWei(latest_price, "ether")
    return float(price)


def swap(tokenInAddress, tokenOutAddress,ammount, account, price_feed, router_address, reverse_feed=False):
    path = [tokenInAddress, tokenOutAddress]
    exchange = interface.IUniswapV2Router02(router_address)
    eth_dai_price = get_asset_price(price_feed)
    if reverse_feed:
        eth_dai_price = 1 / eth_dai_price
    ammountOutMin = int((eth_dai_price * 0.9) * ammount)
    timeStamp = chain[brownie.web3.eth.get_block_number()]["timestamp"] + 120
    tx = exchange.swapExactTokensForTokens(
        ammount, ammountOutMin,path, account.address, timeStamp, {"from": account}
    )
    tx.wait(1)

    



def main():
    #account = accounts.load("study-account2")
    account = accounts[0]
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork-alc"]:
        get_weth()

    weth_address = config["networks"][network.show_active()]["weth_token"]
    dai_address = config["networks"][network.show_active()]["aave_dai_token"]
    sushiswap02_router02 = config["networks"][network.show_active()][
        "sushi_router"
    ]
    price_feed = config["networks"][network.show_active()]["dai_eth_price_feed"]
    amount_to_swap = Web3.toWei(0.1, "ether")
    tx = approve_erc20(amount_to_swap, sushiswap02_router02, weth_address, account)
    tx.wait(1)
    print(
        f"The starting balance of DAI in {account.address} is now {interface.IERC20(dai_address).balanceOf(account.address)}"
    )
    
    swap(weth_address,dai_address,amount_to_swap,account,price_feed, sushiswap02_router02)



    print(
        f"The ending balance of DAI in {account.address} is now {interface.IERC20(dai_address).balanceOf(account.address)}"
    )
    