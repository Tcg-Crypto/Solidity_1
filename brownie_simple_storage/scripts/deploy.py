from brownie import accounts, SimpleStorage

def deploy_simple_storage():
    account = accounts.load("study-account2")
    print(account)
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    stored_value = simple_storage.retrieve()
    print(stored_value)
    tx = simple_storage.store(15, {"from": account})
    tx.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def main():
    deploy_simple_storage()
