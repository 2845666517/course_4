import datetime
import json
import time
import pandas as pd
from utils.datebase import Mogodb
from pyecharts.charts import Pie

if __name__ == '__main__':
    # 1. 写一个Python程序，在MongoDB中插入多条数据，
    # 包含如下字段：职位标题，发布者，内容，发表时间，职位关键字(Python或Java或C++)，职位城市，公司名称，薪水。
    info=[
        {'职位标题':'Python开发工程师','发布者':'刘奇梦','内容':'负责睡觉','发表时间':datetime.datetime.now(),'职位关键字':'Python',
         '职位城市':'北京','公司名称':'北京八维','薪水':18000},
        {'职位标题': 'c语言开发', '发布者': '刘奇梦', '内容': '负责睡觉', '发表时间': datetime.datetime.now(),'职位关键字':'c',
         '职位城市': '湖南', '公司名称': '北京八维', '薪水': 16000},
        {'职位标题': 'Java', '发布者': '刘奇梦', '内容': '负责睡觉', '发表时间': datetime.datetime.now(),'职位关键字':'Java',
         '职位城市': '上海', '公司名称': '北京八维', '薪水': 1800},
        {'职位标题': 'C++', '发布者': '刘奇梦', '内容': '负责睡觉', '发表时间': datetime.datetime.now(),'职位关键字':'c++',
         '职位城市': '江西', '公司名称': '北京八维', '薪水': 17000},
        {'职位标题': 'Python开发工程师', '发布者': '刘奇梦', '内容': '负责睡觉', '发表时间': datetime.datetime.now(),'职位关键字':'Python',
         '职位城市': '北京', '公司名称': '北京八维', '薪水': 19000}
    ]
    # Mogodb.talbe.drop()
    # for i in info:
    #     Mogodb.talbe.insert_one(i)

    # 2. 1题的数据必须以JSON形式插入到MongoDB中。
    # 3. 在1题创建的集合中插入一个新文档。
    Mogodb.talbe.insert_one({'name':'liuqimeng'})

    # 4. 删除3题插入的新文档。
    Mogodb.talbe.delete_one({'name':'liuqimeng'})

    # 5. 修改第一个职位关键字为Python的数据，改为职位为Java。
    Mogodb.talbe.update_one({'职位关键字':'Python'},{'$set':{'职位关键字':'Java'}})
    print(list(Mogodb.talbe.find()))

    # 6. 计算Java和C++岗位的数量。
    res=Mogodb.talbe.find(
        {'$or':[{'职位关键字':'Java'},{'职位关键字':'python'}]}
    )
    print(len(list(res)))

    # 7. 查询出所有Python岗位。
    print(list(Mogodb.talbe.find({'职位标题':{'$regex':'Python'}})))

    # 8. 查询出所有时间大于今天0点的岗位。
    today_0=datetime.datetime(2023,3,28,0,0,0)
    print(list(Mogodb.talbe.find({'发表时间':{'$gte':today_0}})))

    # 9. 查询出所有时间大于今天12点，小于今天18点的岗位。
    print(list(Mogodb.talbe.find({'发表时间':{'$gte':datetime.datetime(2023,3,28,12,0,0),'$lte':datetime.datetime(2023,3,28,12,0,0)}})))

    # 10. 使用Type操作符查询公司名称为String的数据。
    print(list(Mogodb.talbe.find({'公司名称':{'$type':'string'}})))

    # 11. 使用limit和skip来查询第三条数据。
    print(list(Mogodb.talbe.find().limit(1).skip(2)))

    # 12. 按照发表时间排序和输出所有招聘数据。
    print(list(Mogodb.talbe.find().sort('发表时间',1)))

    # 13. 给title字段创建一个索引。
    Mogodb.talbe.create_index(keys='职位标题')
    print('*'*30)
    # 14. 计算每个发布者发布的岗位数量。
    dom14=[
        {'$group':
            {'_id':'$发布者',
                'gs':{'$sum':1}
            }
        }
    ]
    w14=Mogodb.talbe.aggregate(
        dom14
    )
    print(list(w14))

    # 15. 计算每个城市的岗位数量。
    dom15 = [
        {'$group':
             {'_id': '$职位城市',
              'gs': {'$sum': 1}
              }
         }
    ]
    w15 = Mogodb.talbe.aggregate(
        dom15
    )
    print(list(w15))

    # 16. 计算每个公司的岗位数量。
    dom16 = [
        {'$group':
             {'_id': '$公司名称',
              'gs': {'$sum': 1}
              }
         }
    ]
    w16 = Mogodb.talbe.aggregate(
        dom16
    )
    print(list(w16))

    # 17. 查询出薪水在10000到15000之间的数字。然后以公司分组计算每个公司的岗位数量。必须使用聚合加管道操作完成。
    dom17=[
        {'$match':{'薪水':{'$gte':100,'$lte':15000}}},
        {'$group':{
            '_id':'$公司名称',
            'gs':{'$sum':1}
        }}
    ]
    w17=Mogodb.talbe.aggregate(
        dom17
    )
    print('17:',list(w17))

    # 18. 查询工资在[0, 10000), [10000, 15000), [15000, 20000)三个区间的数量。
    bins=[0,1000,15000,20000,50000]
    labels=['0-10000','10000-15000','15000-20000','2万以上']
    df=pd.DataFrame(list(Mogodb.talbe.find()))
    df['qj']=pd.cut(df['薪水'],bins=bins,labels=labels)
    print(df)

    # 19. 计算每个城市岗位数量占有岗位总量的百分比。
    df19=df.groupby('职位城市')['公司名称'].count()
    pie=(
        Pie()
        .add('',list(zip(df19.index.tolist(),df19.values.tolist())))
    )
    pie.render('./19.html')