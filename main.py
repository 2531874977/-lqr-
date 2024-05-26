from data_send_api import *

def main():
    conn, address = socket_connect()
    socket_launch(conn, address)

if __name__ == "__main__":
    main()