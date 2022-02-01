import pymysql.cursors
import pymysql
from sshtunnel import SSHTunnelForwarder

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from _Userinfo import Userinfo

def way1(remote_ip, remote_port, dbUserID, dbUserPW):
    with SSHTunnelForwarder(
        (Userinfo.REMOTE_SERVER_IP, Userinfo.REMOTE_SERVER_SSH_PORT),
        ssh_username=Userinfo.SSH_USERNAME,
        ssh_pkey=Userinfo.SSH_PKEY,
        remote_bind_address=('127.0.0.1', 3306)) as tunnel:
            conn = pymysql.connect(
                host='127.0.0.1',
                user=Userinfo.DB_ID,
                password=Userinfo.DB_PW,
                port=tunnel.local_bind_port,
                db=Userinfo.DB_SCHEME,
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)
            
            print('\t[+] DBMS connected')

            cur = conn.cursor()
            sqlstr = 'select host, password from user'
            cur.execute(sqlstr)
            
            print('\t[+] Exec Query')
            for result in cur.fetchall():
                print(result)

            conn.close()
                # with conn.cursor() as cur:
                #     sqlstr = 'select host, password from user'
                #     cur.execute(sqlstr)
                #     while result:
                #         result = cur.fetchone()
                #         print(result)
                #     print('\t[+] DBMS connected')

def way2():
    # https://blog.dork94.com/194
    engine = sqlalchemy.create_engine("mysql+pymysql://kbo_user01:ds@1q2w3e4r!@132.226.225.56:3306/kbo")
    engine.connect()



if __name__ == "__main__":
    
    print('>>> FINISH <<<')