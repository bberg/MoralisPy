# Introduction
A simple Python wrapper for the Molaris REST API. Useful for getting ERC-20 token prices, getting general token information and getting information about all tokens in a wallet. 

## Molaris
Use requires a Molaris API key which is currently available with the free Molaris service tier. 
- https://moralis.io/
- https://deep-index.moralis.io/api-docs/#/
- https://docs.moralis.io/moralis-server/web3-sdk/moralis-web3-api-rest

# Usage
## Setup

Replace YOUR_API_KEY with the Moralis API Key.

    from MoralisPy import MoralisPy
    moralis = MoralisPy()
    moralis.set_api_key("YOUR_API_KEY")

## ERC-20 Tokens 
### Get Token Metadata

    from pprint import pprint as pp
    token_address = "0x8430146cFd6F29c2B580c1004787b7d3c9F9F3b8"
    pp(moralis.get_token_metadata(token_address, "avalanche"))

```
{'address': '0x8430146cfd6f29c2b580c1004787b7d3c9f9f3b8',
 'block_number': '8540191',
 'decimals': '18',
 'logo': None,
 'logo_hash': None,
 'name': 'VaporNodes',
 'symbol': 'VPND',
 'thumbnail': None,
 'validated': 1 }
```
### Get Token Price
    pp(moralis.get_token_price(token_address,"avalanche"))
```
{'exchangeAddress': '0x9ad6c38be94206ca50bb0d90783181662f0cfa10',
 'exchangeName': 'TraderJoe',
 'nativePrice': {'decimals': 18,
                 'name': 'Avalanche',
                 'symbol': 'AVAX',
                 'value': '151093980928143'},
 'usdPrice': 0.017792376973093486}
```
## Wallets
Get information about all the ERC-20 tokens in a wallet, get the price of those tokens and calculate the total value of the wallet. 

Native token prices (e.g. Eth, Avalanche etc.) are not provided by the Molaris API so aren't included in the sum   

    import pandas as pd
    wallet = "YOUR_WALLET_ADDRESS"
    erc20_assets, native_token_assets, erc20_token_assets = moralis.get_total_token_assets(wallet, ['eth','avalanche'])
    erc20_df = pd.DataFrame(erc20_token_assets)
    erc20_df.to_csv("erc20.csv")


