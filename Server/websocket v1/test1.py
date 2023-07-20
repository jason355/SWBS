import multiprocessing as mp
import time


def send_message(queue):
    for i in range(10):
        new_message = True
        queue.put(new_message)
        print("I think it put")
        time.sleep(2)


if __name__ == '__main__':
    queue = mp.Queue()

    process = mp.Process(target=send_message, args=(queue,))
    process.start()

    process.join()
