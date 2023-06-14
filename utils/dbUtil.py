def save_to_db(connection_pool, name, param_text):
    # 创建连接池，这里将创建连接池放在最外层，以免每来一条数据就要创建一次连接池
    # connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20, database="mine", user="postgres",
    #                                                      password="postgres", host="localhost", port="5432")
    # 从连接池中获取连接
    conn = connection_pool.getconn()
    # 创建游标
    cur = conn.cursor()
    # 查询车型是否存在
    cur.execute("SELECT * FROM public.dcd_car_params WHERE car_type = '" + name + "'")
    if cur.fetchone() is None:
        # 如果不存在，则插入数据
        cur.execute("INSERT INTO public.dcd_car_params (car_type, params, operator) VALUES (%s, %s, %s)",
                    (name, param_text, 'System'))
    # 提交更改
    conn.commit()
    # 将连接放回连接池
    connection_pool.putconn(conn)
    # 关闭游标
    cur.close()
