import sys
import requests
import json
import pandas as pd
from pandas import json_normalize

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://www.safekorea.go.kr',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?emgPage=Y&menuSeq=679',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,ja;q=0.5,pt;q=0.4',
}

payload = '{"searchInfo":{"pageIndex":"1","pageUnit":"10","pageSize":10,"firstIndex":"1","lastIndex":"1","recordCountPerPage":"10","searchBgnDe":"2022-01-28","searchEndDe":"2022-01-29","searchGb":"1","searchWrd":"","rcv_Area_Id":"","dstr_se_Id":"","c_ocrc_type":"","sbLawArea1":"","sbLawArea2":""}}'

bgnDate = '2022-01-28'
endDate = '2022-01-29'
fileName = f'disasterSmsList_{bgnDate}_{endDate}.xlsx'

url = 'https://www.safekorea.go.kr/idsiSFK/sfk/cs/sua/web/DisasterSmsList.do'


if __name__ == '__main__':
    pay = json.loads(payload)
    re = requests.post(url, headers=headers, data=payload).json()['rtnResult']

    if re['resultCode'] != '0': # resultCode가 0이면 success, 아니면 종료
        print('')
        quit()

    # payload의 pageUnit을 다시 지정하여 request
    pay['searchInfo']['pageUnit'] = re['totCnt']
    payload = json.dumps(pay)

    resultjson = requests.post(url, headers=headers, data=payload).json()

    # json obj를 excel로 export.
    json_normalize(resultjson['disasterSmsList']).to_excel(fileName, sheet_name='disasterSmsList')

