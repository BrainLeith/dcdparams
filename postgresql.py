import psycopg2
import psycopg2.pool

# 创建一个数据库连接池
pool = psycopg2.pool.SimpleConnectionPool(
    host='localhost',
    port=5432,
    dbname='mine',
    user='postgres',
    password='postgres',
    maxconn=128,
    minconn=8,
)

if __name__ == '__main__':
    # 获取一个数据库连接
    conn = pool.getconn()

    # 创建一个游标对象
    cur = conn.cursor()

    # 执行一些SQL查询语句
    cur.execute("SELECT * FROM public.dcd_car_params order by 1")
    rows = cur.fetchall()

    # 输出查询结果
    for row in rows:
        print(row)

    # 关闭游标和连接
    cur.close()
    conn.close()

    # 释放连接池资源
    pool.putconn(conn)
    # 关闭连接池
    pool.closeall()
    print('关闭连接池')
