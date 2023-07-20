import multiprocessing as mp


def listen_queue(queue):
    while True:
        new_message = queue.get()
        process_message(new_message)


def process_message(message):
    print("Get message:", message)


if __name__ == "__main__":
    queue = mp.Queue()

    listener = mp.Process(target=listen_queue, args=(queue,))
    listener.start()
