class Mysqldb:
    user='root'
    password='root'
    host='127.0.0.1'
    port=3306
    db='week3'
    DB_URI=f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8'