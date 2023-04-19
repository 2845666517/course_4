import threading

# 互斥锁
lock = threading.Lock()
if __name__ == '__main__':
    song=input('请输入音乐名称:')
    url = f'https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord={song}'
