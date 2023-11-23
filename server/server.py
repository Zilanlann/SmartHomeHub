import socket
import threading


def handle_client(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("客户端已断开连接")
                break
            print(f"客户端说: {message}")
    except ConnectionResetError:
        print("连接被客户端断开")
    finally:
        client_socket.close()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("服务器启动，等待连接...")

    client_sock, addr = server_socket.accept()
    print(f"来自 {addr} 的连接")
    client_thread = threading.Thread(target=handle_client, args=(client_sock,))
    client_thread.start()

    try:
        while True:
            reply = input("回复: ")
            if not reply:
                print("没有输入，服务器准备关闭连接")
                break
            client_sock.send(reply.encode('utf-8'))
    except KeyboardInterrupt:
        print("服务器关闭")
    finally:
        client_sock.close()
        server_socket.close()


if __name__ == '__main__':
    server()
