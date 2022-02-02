from distutils.log import error
import json
import sys
from traceback import print_tb

import requests
from pandas import json_normalize

from datetime import datetime

class Appinfo:
    bgnDate = '2022-01-01'
    endDate = '2022-01-01'
    msgSuc = '[+] request success!!!'
    dateFormatStr = '%Y-%m-%d'


'''
지정한 url에 요청
'''
def doReq(payload):
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
    url = 'https://www.safekorea.go.kr/idsiSFK/sfk/cs/sua/web/DisasterSmsList.do'
    return requests.post(url, headers=headers, data=payload).json()

def getTodayDate():
    return datetime.today().strftime(Appinfo.dateFormatStr)

'''
checkout argument.
set datetime format.
'''
def chkArgValue():
    if len(sys.argv) < 2:
        # help msg
        print(
            '''
    예시.
        Format
            >> disasterSmsList.py --date::{날짜}
        
        *필수
        --date
            Ex.1) 오늘 하루의 sms list 추출
                --date::today

            Ex.2) 1일만 입력
                --date::2022-01-01

            Ex.3) 기간 입력. 최대 7일
                --date::2022-01-01~2022-01-07
        

        << 동작 순서 >>
        1) payload, header setting, and post request
        2) checkout request success
            [2]의 response json 중 ['rtnResult']['resultCode']
            2-1) 'resultCode'가 0이면 success. 계속 진행.
            2-2) 그 외에는 application quit.
        3) reset payload
            - ['pageUnit'] :: 한 번에 보여줄 Unit page 개수에 전체 값 Count를 입력.['rtnResult']['totCnt']
        4) post request again.
            response의 결과 excel 저장
            - 순서 :: response json obj -> dataframe -> export(excel)
    '''
        )
        quit()

    for info in sys.argv[1:]:
        # info = item.split(' ')
        if info.find('--date') != -1:
            value = info.split('::')[1]
            try:
                if value.lower()=='today': # Ex.1)
                    tmp = getTodayDate()
                    Appinfo.bgnDate = tmp
                    Appinfo.endDate = tmp
                elif value.find('~') == -1: # Ex.2)
                    Appinfo.bgnDate = info[1]
                    Appinfo.endDate = info[1]
                elif value.find('~') != -1: # Ex.3)
                    tmp = value.split('~')
                    # check datetime format
                    datetime.strptime(tmp[0], Appinfo.dateFormatStr)
                    datetime.strptime(tmp[1], Appinfo.dateFormatStr)
                    Appinfo.bgnDate = tmp[0]
                    Appinfo.endDate = tmp[1]
            except ValueError:
                printOutLog('[-] Check out argument :: --date')
                quit()
        else:
            pass

def printOutLog(str):
    print(f'\t{str}')

def main():
    payload = '{"searchInfo":{"pageIndex":"1","pageUnit":"10","pageSize":10,"firstIndex":"1","lastIndex":"1","recordCountPerPage":"10","searchBgnDe":"2022-01-28","searchEndDe":"2022-01-29","searchGb":"1","searchWrd":"","rcv_Area_Id":"","dstr_se_Id":"","c_ocrc_type":"","sbLawArea1":"","sbLawArea2":""}}'

    # 1) payload, header setting, and post request
    re = doReq(payload)['rtnResult']

    # 2) checkout request success.
    if re['resultCode'] != '0':
        printOutLog('[-] request failed. checkout network state or website[\'www.safekorea.go.kr\']')
        quit()
    printOutLog(Appinfo.msgSuc)

    # 3) reset payload.
    payjs = json.loads(payload)
    payjs['searchInfo']['pageUnit'] = re['totCnt']
    payload = json.dumps(payjs)

    # 4) post request again. and save result(excel format)
    fileName = f'disasterSmsList_{Appinfo.bgnDate}_{Appinfo.endDate}.xlsx'
    json_normalize(doReq(payload)['disasterSmsList']).to_excel(fileName, sheet_name='disasterSmsList', index=False)
    printOutLog(f'[+] result Saved. path : {fileName}')

if __name__ == '__main__':
    chkArgValue()
    main()

    print('\n\n>>> End Application <<<')