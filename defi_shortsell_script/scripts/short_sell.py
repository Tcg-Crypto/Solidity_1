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


def getLendingPool():
    lending_pool_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["Lending_pool_address"]
    )
    lending_pool_address = lending_pool_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def get_user_lending_data(lending_pool,address):
    (total_collateral_eth, debt_eth, availabe_to_borrow, liquidation_threshhold, LTVratio, heath_factor)= lending_pool.getUserAccountData(address)
    availabe_to_borrow = Web3.fromWei(availabe_to_borrow,"ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth,"ether")
    debt_eth = Web3.fromWei(debt_eth,"ether")
    print(availabe_to_borrow)
    print(":::: availabe_to_borrow")
    return(float(availabe_to_borrow),float(debt_eth))

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
    weth_address = config["networks"][network.show_active()]["weth_token"]
    dai_address = config["networks"][network.show_active()]["aave_dai_token"]
    sushiswap02_router02 = config["networks"][network.show_active()][
        "sushi_router"
    ]
    price_feed = config["networks"][network.show_active()]["dai_eth_price_feed"]
    #account = accounts.load("study-account2")
    account = accounts[0]
    if network.show_active() in ["mainnet-fork-alc"]:
        get_weth()
    lendingPool = getLendingPool()
    print(lendingPool)
    ammount = 0.1 * 10**18
    approve_erc20(ammount, lendingPool.address, weth_address,account)
    tx = lendingPool.deposit(weth_address,ammount,account.address,0, {"from": account})
    tx.wait(1)
    print("Deposited")
    availabe_to_borrow, debt_eth = get_user_lending_data(lendingPool,account.address)
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    print(f"Dai eth price is {dai_eth_price}")
    ammount_dai_to_borrow = (1/dai_eth_price) * (availabe_to_borrow * 0.6)
    tx = lendingPool.borrow(config["networks"][network.show_active()]["aave_dai_token"],Web3.toWei(ammount_dai_to_borrow,"ether"),1,0, account.address, {"from":account})
    tx.wait(1)
    print(f"Congratulations! We have just borrowed {ammount_dai_to_borrow}")
    tx = approve_erc20(Web3.toWei(ammount_dai_to_borrow,"ether"), sushiswap02_router02, dai_address, account)
    tx.wait(1)
    amount_dai_to_borrow = int(ammount_dai_to_borrow * (10 ** 18))
    print(
        f"The balance of DAI in {account.address} is now {interface.IERC20(dai_address).balanceOf(account.address)}"
    )
    swap(dai_address,weth_address,amount_dai_to_borrow,account,price_feed, sushiswap02_router02)
    print("SOLD")
    print(
        f"The balance of DAI in {account.address} is now {interface.IERC20(dai_address).balanceOf(account.address)}"
    )
