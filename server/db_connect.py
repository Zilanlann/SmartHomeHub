import random
import datetime

import pymysql


def connect_db():
    """创建数据库连接"""
    return pymysql.connect(
        host="localhost",
        db="mysql",
        user="root",
        password="X*TnVEzbKMwHLJ3"
    )


def init_table(cursor):
    """初始化Users, TH表"""
    create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password BLOB NOT NULL
    )
    """
    create_TH = """
    CREATE TABLE IF NOT EXISTS TemperatureHumidity (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        temperature DOUBLE,
        humidity DOUBLE
    );
    """
    cursor.execute(create_users)
    cursor.execute(create_TH)


def add_user(db, cursor, username, password):
    """插入用户名密码，密码使用AES加密"""
    sql = "INSERT INTO users (username, password) VALUES (%s, AES_ENCRYPT(%s, 'usee111'))"
    cursor.execute(sql, (username, password))
    db.commit()


def authenticate_user(cursor, username, password):
    """验证用户账号密码，密码进行相同的AES加密之后与数据库中的密码比对"""
    sql = "SELECT * FROM users WHERE username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    if result:
        sql = "SELECT * FROM users WHERE username=%s and password=AES_ENCRYPT(%s, 'usee111')"
        if cursor.execute(sql, (username, password)):
            print("登录成功")
            return 1
        else:
            print("密码错误")
            return 0
    else:
        print("用户不存在")
        return -1


def change_password(db, cursor, username, old_password, new_password):
    """修改用户密码"""
    # 验证用户身份
    result = authenticate_user(cursor, username, old_password)
    if result == 1:
        # 更新密码
        update_sql = "UPDATE users SET password=AES_ENCRYPT(%s, 'usee111') WHERE username=%s"
        cursor.execute(update_sql, (new_password, username))
        db.commit()
        print("Password updated successfully")
        return 1
    elif result == 0:
        print("Invalid old password")
        return 0
    else:
        print("User not found")
        return -1


def insert_temperature_humidity(db, cursor, timestamp, temperature, humidity):
    """
    向TemperatureHumidity表插入数据
    :param cursor: 数据库游标
    :param timestamp: 时间戳
    :param temperature: 温度
    :param humidity: 湿度
    """
    sql = "INSERT INTO TemperatureHumidity (timestamp, temperature, humidity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (timestamp, temperature, humidity))
    db.commit()


def get_average_temperature_humidity(cursor):
    # 获取当前时间和24小时前的时间
    end_time = datetime.datetime.now()
    print(end_time)
    start_time = end_time - datetime.timedelta(hours=24)

    # SQL查询，按小时分组计算平均温度和湿度
    query = """
    SELECT HOUR(timestamp), AVG(temperature), AVG(humidity)
    FROM TemperatureHumidity
    WHERE timestamp BETWEEN %s AND %s
    GROUP BY HOUR(timestamp)
    ORDER BY HOUR(timestamp);
    """

    cursor.execute(query, (start_time, end_time))

    # 初始化数组
    hours = []
    temperatures = []
    humidities = []

    # 处理查询结果
    for hour, avg_temp, avg_hum in cursor.fetchall():
        hours.append(hour)
        temperatures.append(round(avg_temp, 2))
        humidities.append(round(avg_hum, 2))

    # 格式化为字符串
    str_hour = "hour = " + str(hours)
    str_temperature = "temperature = " + str(temperatures)
    str_humidity = "humidity = " + str(humidities)
    print(str_hour)
    print(str_temperature)
    print(str_humidity)
    return str_hour, str_temperature, str_humidity


def insert_sample_data(cursor):
    # 当前时间
    current_time = datetime.datetime.now()

    for i in range(24):
        # 每个小时的时间点
        timestamp = current_time - datetime.timedelta(hours=i)
        # 生成随机温度和湿度值
        temperature = random.uniform(20, 35)  # 假设温度在20到35度之间
        humidity = random.uniform(30, 90)  # 假设湿度在30%到90%之间

        # 插入数据到数据库
        insert_temperature_humidity(db, cursor, timestamp, temperature, humidity)


def close_db(db, cursor):
    """关闭数据库连接"""
    cursor.close()
    db.close()


def delete_all(cursor):
    cursor.execute("DROP TABLE IF EXISTS users")


if __name__ == '__main__':
    db = connect_db()
    cursor = db.cursor()
    # delete_all(cursor)
    init_table(cursor)
    add_user(db, cursor, "root", "admin")
    # insert_sample_data(cursor)
    get_average_temperature_humidity(cursor)
    # authenticate_user(cursor, "root", "admin")
    close_db(db, cursor)
