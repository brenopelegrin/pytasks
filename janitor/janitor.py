from resources.janitor import RunTaskCleaner
import multiprocessing as context

if __name__ == '__main__':
    janitor1 = context.Process(target=RunTaskCleaner)
    janitor1.start()