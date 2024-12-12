import os
import signal
import asyncio
import threading
from multiprocessing import Process
from threading import Thread
from uvicorn import Config, Server
import uvicorn
import pytest


from api import application
from api.core.logging import logger, TEST_LOG_CONFIG

TESTS_FINISHED = False
uvi_run = uvicorn.run(application, log_level="trace", log_config=TEST_LOG_CONFIG)

# def thread_run_app():
#     thread = Thread(target=uvi_run, daemon=True)
#     thread.start()
#     return thread


def run_tests():
    logger.info("+++++++++++++++ run tests ++++++++++++++++++")
    TESTS_FINISHED = True


def shutdown_app():
    logger.info("+++++++++++++++ shutdown app ++++++++++++++++++")
    # os.kill(os.getpid(), signal.SIGINT)  # Ctrl+C
    # if TESTS_FINISHED == True:
    #     logger.info("+++++++++++++++ stop testing system ++++++++++++++++++")



# async def main():
#     await asyncio.gather(run_app(), run_tests(), shutdown_app())


if __name__ == '__main__':
    proc1 = Process(target=uvi_run, daemon=False)
    proc1.start()

    # proc2 = Process(target=run_tests, daemon=True)
    # proc2.start()
    # proc2.kill()

    proc1.kill()
    # processes = [
    #     Process(target=uvi_run, daemon=True),
    #     Process(target=run_tests, daemon=True),
    #     Process(target=shutdown_app, daemon=True)
    # ]
    #
    # for t in processes:
    #     t.start()
    # for t in processes:
    #     t.join()  # говорим программе: "дожидись выполнения 10 потоков" (а не убивай их)



