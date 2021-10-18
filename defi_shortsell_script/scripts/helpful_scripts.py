from brownie import accounts, network, config, Contract, LinkToken, MockV3Aggregator, MockOracle, VRFCoordinatorMock

LOCAL_ENVRONMENTS = ['development','ganache-local']
DECIMALS = 8
STARTING_PRICE = 200
contract_to_mock = {
    "link_token": LinkToken,
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "oracle": MockOracle,
}


def get_account():
    print (network.show_active())
    if network.show_active() in LOCAL_ENVRONMENTS or network.show_active() == "mainnet-fork-dev":
        return accounts[0]
    else:
        account = accounts.load("study-account2")
        return account
