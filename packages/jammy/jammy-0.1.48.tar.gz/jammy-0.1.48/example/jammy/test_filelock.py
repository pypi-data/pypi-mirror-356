# pylint: skip-file
import time
from multiprocessing import Pool

from jammy.utils.filelock import try_filelock, TryFileLock

w_file = "writing.log"


def work(pid):
    global w_file

    def fn():
        with open(w_file, "a") as f:
            f.write(f"{pid}\n")
        print(f"{pid} start sleep")
        time.sleep(1)
        a = 1.0
        b = 1
        c = a / b
        print(f"{pid} end sleep")

    try_filelock(
        fn,
        w_file,
        is_soft=False,
        timeout=10,
    )

def work2(pid):
    global w_file
    with TryFileLock(w_file, is_soft=False, timeout=1) as flock:
        print(pid, flock)
        if flock is None:
            return
        with open(w_file, "a") as f:
            f.write(f"{pid}\n")
        print(f"{pid} start sleep")
        time.sleep(10)
        a = 1.0
        b = 1
        print(f"{pid} end sleep")

if __name__ == "__main__":
    # with Pool(5) as p:
    #     print(p.map(work, [1, 2, 3, 4, 5]))
    print("===" * 10)
    with Pool(5) as p:
        print(p.map(work2, [1, 2, 3, 4, 5]))
