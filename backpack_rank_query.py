import requests
import json
import re

def backpack_rank_query(rank: int, your_valume: int, ensure_query_rank_total: bool, ensure_query_rank_phase: bool):
    def require_header():
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cookie': 'Your Cookies',            
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

    def check_rank_phase(data: dict):
        phase_low = (1000, 10000) # 1000 ~ 1w
        phase_middle = (10000, 100000) # 1w ~ 10w
        phase_high = (100000, 1000000) # 10w ~ 100w
        phase_higest = (1000000, 10000000) # 100w ~ 1000w
        
        low, middle, high, higest = [], [], [], []
        print(data)
        for i in data:
            if phase_low[0] < float(i['volume']) < phase_low[1]:
                low.append(float(i['volume']))
            if phase_middle[0] < float(i['volume']) < phase_middle[1]:
                middle.append(float(i['volume']))
            if phase_high[0] < float(i['volume']) < phase_high[1]:
                high.append(float(i['volume']))
            if phase_higest[0] < float(i['volume']) < phase_higest[1]:
                higest.append(float(i['volume']))            
            
        print("============== 1000~1W Volume Amount {} ==============".format(len(phase_low)))
        print("============== 1w~10W Volume Amount {} ==============".format(len(middle)))
        print("============== 10w~100W Volume Amount {} ==============".format(len(high)))
        print("============== 100w~1000w Volume Amount {} ==============".format(len(higest)))
    
    
    def check_rank_total(data: dict): 
        print("============== TOTAL RANK AMOUNT {} ==============".format(len(data)))
    
    def entry():
        api_req_limit, api_req_count = 100, rank // 100
        api_req_limit_total = api_req_limit
        api_url = "https://api.cf.backpack.exchange/wapi/v1/statistics/volume/asset?assetSymbol=USDC&limit={}&offset=0&since=1707865200000&leaderboard=true"
        
        resp_dict = []
        for _ in range(api_req_count):
            #unzip_resp_content = gzip.decompress(resp.content).decode('utf-8')
            api_req_limit_total += api_req_limit
            resp = requests.get(api_url.format(api_req_limit_total), headers=require_header())
            resp_dict.append(json.loads(resp.text))
            print(api_url.format(api_req_limit_total))
            
        if ensure_query_rank_total: check_rank_total(resp_dict)
        if ensure_query_rank_phase: check_rank_phase(resp_dict)
        
        if not ensure_query_rank_phase and not ensure_query_rank_total:
            try:
                for index, info in enumerate(resp_dict):
                    integer_part = integer_part = info['volume'].split('.')[0]
                    if your_valume == int(integer_part):
                        print("============== YOUR RANK IS {} ==============".format(index))
                        break
                        
            except requests.exceptions.RequestException as e:
                print("Request failed {}".format(e))
                
    entry()
## ============== YOUR RANK IS 3146 ==============    
backpack_rank_query(100000, 144470, True, False)


## ============== TOTAL RANK AMOUNT 95506 ==============
## backpack_rank_query(100000, 144470, True)
