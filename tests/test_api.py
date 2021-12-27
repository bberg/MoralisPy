import pandas as pd
import pytest
import os
import json
from pprint import pprint as pp
from MoralisPy.api import MoralisPy

# setup
configFilePath = os.path.abspath('') + '/test-config.json'

with open(configFilePath, 'r') as configdata:
    data = configdata.read()

# parse file
obj = json.loads(data)
api_key = obj['api_key']

# chain config
all_chains = [
    'eth'
    , 'ropsten'
    , 'rinkeby'
    , 'goerli'
    , 'kovan'
    , 'polygon'
    , 'mumbai'
    , 'bsc'
    , 'bsc testnet'
    , 'avalanche'
    , 'avalanche testnet'
    , 'fantom'
]


if type(obj['test_chains']) == list:
    test_chains = obj['test_chains']
else:
    test_chains = all_chains

test_token_chain_combos_input = obj['test_token_chain_combos']
test_token_chain_combos = []
for i in test_token_chain_combos_input:
    test_token_chain_combos.append((i['token'], i['chain']))


@pytest.fixture
def setup():
    setup = MoralisPy()
    return setup


def test_setting_api_key(setup):
    setup.set_api_key(api_key)
    assert setup.api_key == api_key


def test_get_url_base(setup):
    assert setup.url_base == 'https://deep-index.moralis.io/api/v2/'


@pytest.fixture
def moralis():
    moralis = MoralisPy()
    moralis.set_api_key(api_key)
    return moralis


@pytest.fixture
def wallet_address():
    return obj['wallet_address']

@pytest.fixture
def all_chains():
    return [
    'eth'
    , 'ropsten'
    , 'rinkeby'
    , 'goerli'
    , 'kovan'
    , 'polygon'
    , 'mumbai'
    , 'bsc'
    , 'bsc testnet'
    , 'avalanche'
    , 'avalanche testnet'
    , 'fantom'
]

@pytest.mark.parametrize("chain", test_chains)
def test_get_native_balance(moralis, wallet_address, chain):
    balance = moralis.get_native_balance(wallet_address, chain)
    assert type(balance) == float


@pytest.mark.parametrize("chain", test_chains)
def test_get_tokens_for_wallet(moralis, wallet_address, chain):
    token_list = moralis.get_tokens_for_wallet(wallet_address, chain)
    assert type(token_list) == list

@pytest.mark.parametrize("token,chain", test_token_chain_combos)
def test_get_token_price(moralis, token, chain):
    token_price = moralis.get_token_price(token, chain)
    assert type(token_price) == dict

@pytest.mark.parametrize("token,chain", test_token_chain_combos)
def test_convert_native_amount_to_token_amount(moralis, token, chain):
    token_amount = moralis.convert_native_amount_to_token_amount(token,chain,1)
    pp(token_amount)
    assert type(token_amount) == float

@pytest.mark.parametrize("token,chain", test_token_chain_combos)
def test_convert_token_amount_to_native_amount(moralis, token, chain):
    token_amount = moralis.convert_token_amount_to_native_amount(token,chain,1)
    pp(token_amount)
    assert type(token_amount) == float

@pytest.mark.parametrize("token,chain", test_token_chain_combos)
def test_native_token_conversion(moralis, token, chain):
    token_amount = moralis.convert_native_amount_to_token_amount(token,chain,1)
    native_amount = moralis.convert_token_amount_to_native_amount(token,chain,token_amount)
    print(native_amount,"should be close to 1")
    assert 0.95 < native_amount < 1.05

def test_get_total_token_assets(moralis,wallet_address,all_chains):
    total_token_assets = moralis.get_total_token_assets(wallet_address, all_chains)
    assert type(total_token_assets[0]) == float
    assert type(total_token_assets[1]) == list
    assert type(total_token_assets[1]) == list

@pytest.mark.parametrize("token,chain", test_token_chain_combos)
def test_get_token_metadata(moralis, token, chain):
    token_metadata = moralis.get_token_metadata(token, chain)
    assert  type(token_metadata) == dict