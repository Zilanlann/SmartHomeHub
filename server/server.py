import socket
import threading
import datetime

from db_connect import authenticate_user, connect_db, close_db, change_password, get_average_temperature_humidity, \
    insert_temperature_humidity


def handle_client(client_socket):
    db = connect_db()
    cursor = db.cursor()
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("客户端已断开连接")
                break
            if message.startswith("checkLogin:"):
                try:
                    # 解析用户名和密码
                    username, password = message.split("checkLogin:")[1].strip().strip("()").split(",")
                    # 调用认证方法
                    auth_result = authenticate_user(cursor, username, password)
                    # 发送认证结果回客户端
                    client_socket.send(str(auth_result).encode('utf-8'))
                except Exception as e:
                    print(f"处理登录请求时出错: {e}")
                    client_socket.send("登录处理错误".encode('utf-8'))
            elif message.startswith("changePassword:"):
                try:
                    cmd, user_info = message.split(":")
                    username, old_password, new_password = [item.strip() for item in user_info.split(",")]
                    result = change_password(db, cursor, username, old_password, new_password)
                    client_socket.send(str(result).encode('utf-8'))
                except Exception as e:
                    print(f"处理更改密码请求时出错: {e}")
                    client_socket.send("更改密码处理错误".encode('utf-8'))
            elif message.startswith("getTH"):
                try:
                    # 调用获取温湿度平均值的函数
                    str_hour, str_temperature, str_humidity = get_average_temperature_humidity(cursor)
                    # 将结果发送回客户端
                    client_socket.send(str_hour.encode('utf-8'))
                    client_socket.send(str_temperature.encode('utf-8'))
                    client_socket.send(str_humidity.encode('utf-8'))
                except Exception as e:
                    print(f"处理获取温湿度平均值请求时出错: {e}")
                    client_socket.send("获取温湿度平均值处理错误".encode('utf-8'))
            elif message.startswith("Temperature:"):
                try:
                    # 解析温度和湿度数据
                    temp_hum_data = message.split(" ")
                    temperature = temp_hum_data[0].split(":")[1]
                    humidity = temp_hum_data[1].split(":")[1]

                    # 获取当前时间戳
                    timestamp = datetime.datetime.now()

                    # 调用函数将数据插入数据库
                    insert_temperature_humidity(db, cursor, timestamp, temperature, humidity)
                    client_socket.send("数据已存储".encode('utf-8'))
                except Exception as e:
                    print(f"处理温湿度数据存储请求时出错: {e}")
                    client_socket.send("存储温湿度数据处理错误".encode('utf-8'))
    except ConnectionResetError:
        print("连接被客户端断开")
    finally:
        close_db(db, cursor)
        client_socket.close()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("服务器启动，等待连接...")

    client_sock, addr = server_socket.accept()
    print(f"来自 {addr} 的连接")
    client_thread = threading.Thread(target=handle_client, args=(client_sock,))
    client_thread.start()

    try:
        while True:
            client_sock, addr = server_socket.accept()
            print(f"来自 {addr} 的连接")
            client_thread = threading.Thread(target=handle_client, args=(client_sock,))
            client_thread.start()

    except KeyboardInterrupt:
        print("服务器关闭")
    finally:
        client_sock.close()
        server_socket.close()


if __name__ == '__main__':
    server()
