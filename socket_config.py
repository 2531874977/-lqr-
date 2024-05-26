import socket
import sys
import json
from sceneInfo import APIList
import sceneInfo



def socket_connect():
    # 建立websocket连接
    try:
        x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        x.bind(("127.0.0.1", 5061))
        x.listen(10)

        conn, address = x.accept()
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    return conn, address

def socket_launch(conn):
    result = conn.recv(4096 * 500)
    dataList = result.split(b"|end")  # 使用|end作为分隔符
    data = dataList[0]
    data_json = json.loads(data)
    apiList = []
    dataState = False
    if data != None:
        dataState = True
        apiList = APIList(data_json['SimCarMsg'])

    return dataState, apiList

def socket_respond(conn):
    conn.send(bytes('{"code":2,"UserInfo":null,"SimCarMsg":null, "messager":""}',
                    encoding="utf-8"))

def socket_send(conn, control_dict_demo):
    conn.send(bytes(control_dict_demo, encoding="utf-8"))