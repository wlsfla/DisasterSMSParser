# DisasterSMSParser


    동작 예시.
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
