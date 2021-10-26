from multiprocessing import Process, Semaphore
from od.misc.interest import InterestConfig
import multiprocessing
from od.network.types import ResourceAllocatorType
import single


def Worker(s, target, *args):
    target(*args)
    s.release()


def main():
    s = multiprocessing.Semaphore(0)
    p = []
    for i in range(20):
        p.append(
            Process(
                target=Worker,
                args=(
                    s,
                    single.main,
                    InterestConfig(True, ResourceAllocatorType.NOMA_OPT, True, 1.4, i)
                )
            )
        )
        p[-1].start()
    for _p in p:
        s.acquire()
        _p.join()


if __name__ == "__main__":
    multiprocessing.set_start_method("forkserver")
    main()
