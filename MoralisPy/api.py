import requests
import datetime
from pprint import pprint as pp

def Merge(dict1, dict2):
    return(dict2.update(dict1))

class MoralisPy:
    def __init__(self):
        self.url_base = 'https://deep-index.moralis.io/api/v2/'
        self.api_key = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET",data=None, headers_to_add=None):

        headers = {
            "x-api-key": self.api_key
        }
        if headers_to_add:
            Merge(headers_to_add, headers)
        pp(headers)
        response = requests.request(url=self.url_base + endpoint, method=method, headers=headers, data=data )
        if response.status_code == 200:
            response_object = response.json()
            # response_object['status_code'] = 200
            return response_object
        else:
            # response_object = {}
            # response_object['status_code'] = response.status_code
            pp(vars(response))
            pp(vars(response.request))
            return response.json()

    def get_native_balance(self, wallet_address, chain):
        endpoint = wallet_address + "/balance?chain=" + chain
        response = self.api_request(endpoint)
        return float(response['balance'])

    def get_tokens_for_wallet(self, wallet_address, chain):
        endpoint = wallet_address + "/erc20?chain=" + chain
        return self.api_request(endpoint)

    def get_token_price(self, token_address, chain):
        endpoint = 'erc20/' + token_address + "/price?chain=" + chain
        return self.api_request(endpoint)

    def convert_native_amount_to_token_amount(self, token_address, chain, native_price_amount):
        price_api_response = self.get_token_price(token_address, chain)
        native_price = float(price_api_response['nativePrice']['value']) * (
                    10 ** float(-price_api_response['nativePrice']['decimals']))
        native_amount = (1 / native_price) * native_price_amount
        return native_amount

    def convert_token_amount_to_native_amount(self, token_address, chain, token_amount):
        price_api_response = self.get_token_price(token_address, chain)
        native_price = float(price_api_response['nativePrice']['value']) * (
                    10 ** float(-price_api_response['nativePrice']['decimals']))
        token_amount = (native_price) * token_amount
        return token_amount

    def get_token_metadata(self, token_address, chain):
        metadata = self.api_request("/erc20/metadata?chain="+chain+"&addresses="+token_address)[0]
        return metadata

    def get_total_token_assets(self, wallet_address, chains, tokens_to_exclude=None, print_debug= False):
        if tokens_to_exclude is None:
            tokens_to_exclude = ['KK8.io']
        # "native assets" are the chain's native token
        native_token_assets = []

        erc20_token_assets_detail_list = []
        erc20_assets_sum = 0
        for chain in chains:

            try:
                native_balance = self.get_native_balance(wallet_address, chain)
                if print_debug:
                    print(chain+"  "+str(native_balance))
                native_token_assets.append({"chain": chain, "native_balance": native_balance})
            except:
                print("error getting native balance for: "+chain)
                native_balance = 0

            tokens = self.get_tokens_for_wallet(wallet_address, chain=chain)
            print(tokens)
            for token in tokens:
                token_price_object = self.get_token_price(token['token_address'], chain=chain)
                if not token_price_object:
                    if print_debug:
                        print("Error getting token information for: ")
                        pp(token)
                else:
                    token_quantity = float(token['balance'])*(10**-float(token['decimals']))
                    holdings_value = token_quantity*float(token_price_object['usdPrice'])
                    native_price = float(token_price_object['nativePrice']['value'])*(10**-float(token_price_object['nativePrice']['decimals']))
                    native_value = token_quantity*native_price
                    if print_debug:
                        print(chain+"  "+token['symbol']+"  quantity:"+str(token_quantity)+" price:$"+str(token_price_object['usdPrice'])+" extended value:$"+str(holdings_value)+"  "+token['token_address'])
                    erc20_token_assets_detail_list.append({
                        "datetime": datetime.datetime.now()
                        , "chain": chain
                        , "symbol": token['symbol']
                        , "token_address": token['token_address']
                        , "quantity": token_quantity
                        , "usd_price": token_price_object['usdPrice']
                        , "holdings_value_usd": holdings_value
                        , "native_price": native_price
                        , "holdings_value_native": native_value
                        , "price_exchange_address": token_price_object['exchangeAddress']
                        , "price_exchange_name": token_price_object['exchangeName']
                        , "native_price_decimals": token_price_object['nativePrice']['decimals']
                        , "native_price_name": token_price_object['nativePrice']['name']
                        , "native_price_symbol": token_price_object['nativePrice']['symbol']
                        , "native_price_value_raw": int(token_price_object['nativePrice']['value'])
                        , "price_object": token_price_object
                        , "detail_object": token
                    })

                if token['symbol'] not in tokens_to_exclude:
                    erc20_assets_sum += float(holdings_value)

        print("total ERC-20 token assets: ", erc20_assets_sum)
        return erc20_assets_sum, native_token_assets, erc20_token_assets_detail_list

    def ipfs_uploadFolder(self,data):
        endpoint = 'ipfs/uploadFolder'
        headers_to_add = {"Content-Type": "application/json",
                "accept": "application/json"}
        resp = self.api_request(endpoint,method='POST',data=data,headers_to_add=headers_to_add)
        pp(resp)
        return resp