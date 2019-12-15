from time import ctime, sleep
import threading


def move(name):
    print("I was at the movies! %s %s" %(ctime(),name))
    sleep(5)


threads = []
t1 = threading.Thread(target=move, args=('钢铁侠',))
threads.append(t1)
t2 = threading.Thread(target=move, args=("蜘蛛侠",))
threads.append(t2)


if __name__ == '__main__':
    for t in threads:
        t.start()
    # for t in threads:
    #     t.join()

    print("做其他事情")

# 防止堵塞
