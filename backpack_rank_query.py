import requests
import gzip
import json
import re

def backpack_rank_query(rank: int, your_valume: int, ensure_query_rank_amount: bool):
    def require_header():
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cookie': 'Your cookies',
            'Dnt': '1',
            'Origin': 'https://backpack.exchange',
            'Referer': 'https://backpack.exchange/',
            'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        return headers
    
    def entry():
        api_url = f"https://api.cf.backpack.exchange/wapi/v1/statistics/volume/asset?assetSymbol=USDC&limit={rank}&offset=0&since=1707865200000&leaderboard=true"
        if ensure_query_rank_amount:
            resp = requests.get(api_url, headers=require_header())
            resp_dict = json.loads(resp.text)
            print("============== TOTAL RANK AMOUNT {} ==============".format(len(resp_dict)))
        else:
            try:
                resp = requests.get(api_url, headers=require_header())
                #unzip_resp_content = gzip.decompress(resp.content).decode('utf-8')
                resp_dict = json.loads(resp.text)
                for index, info in enumerate(resp_dict):
                    integer_part = integer_part = info['volume'].split('.')[0]
                    if your_valume == int(integer_part):
                        print("============== YOUR RANK IS {} ==============".format(index))
                        break
                        
            except requests.exceptions.RequestException as e:
                print("Request failed {}".format(e))
            
    entry()
## ============== YOUR RANK IS 3146 ==============    
backpack_rank_query(100000, 144470, False)


## ============== TOTAL RANK AMOUNT 95506 ==============
backpack_rank_query(100000, 144470, True)
