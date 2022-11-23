from resources.handler import TaskHandler
import multiprocessing as context

if __name__ == '__main__':
    p1 = context.Process(target=TaskHandler)
    p1.start()