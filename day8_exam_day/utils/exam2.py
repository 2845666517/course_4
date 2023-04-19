import time

from playwright.sync_api import sync_playwright


def run(p):
    chrom=p.chromium.launch(headless=False)

    page=chrom.new_page()

    page.goto(url='https://movie.douban.com/top250',wait_until='domcontentloaded')

    time.sleep(3)

    page.wait_for_load_state(timeout=40000)
    s = page.inner_html('id=content')
    with open('res2.html', 'w', encoding='utf-8') as f:
        f.write(s)

    page.close()
    chrom.close()

if __name__ == '__main__':
    # 1）爬取豆瓣电影，https: // movie.douban.com / top250
    with sync_playwright() as p:
        run(p)
    # 2）响应体信息合理的方式存入本地
    # 3）获取每部电影的详细信息（包括：电影名称，电影评分，电影评论人数）
    # 4）将以上每部电影的详细信息存入到本地mongodb中
    # 5）每个地区的电影评分的平均值以及评分人数的总和如何分布，请以多维柱状图进行可视化展示
    # 6）统计所有电影的评分的所有指标项
    # 7）电影评论人数由多到少，电影评分由高到低的数据怎么分布
    # 8）获取评分最高的电影名称
