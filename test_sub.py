import matlab.engine
import time
import random
from datetime import date, datetime
date_str_fmt = "%d/%m/%Y %H:%M:%S"
MATLAB_ENG = matlab.engine.start_matlab('-nodesktop -nodisplay')

TIMES = 50
SETS = 200
TOTAL_SEC = 0
time.sleep(2)
random.seed(20)
for _ in range(TIMES):
    futures = []
    beg_time = datetime.now()
    # for i in range(SETS):
    #     futures.append(
    #         MATLAB_ENG.SINR_Channel_Model_5G_mex(
    #             float(random.randrange(500, 1000, 1)),
    #             float(25),
    #             float(1.5),
    #             float(2),
    #             float(23),
    #             float(180000),
    #             matlab.double([10 for _ in range(3)]),
    #             matlab.double([1.5 for _ in range(3)]),
    #             matlab.double([random.randrange(100, 600, 1) for _ in range(3)]),
    #             matlab.double([10 for _ in range(3)]),
    #             float(0.1 * 1000),  # us->ns
    #             float(4.69 * 1000),  # us->ns
    #             True,
    #             float(0.001),
    #             float(23 - 3.01029995664),
    #             False,
    #             True,
    #             nargout=9,
    #             background=True
    #         )
    #     )
    # for f in futures:
    #     f.result()
    for i in range(SETS):
        MATLAB_ENG.SINR_Channel_Model_5G_mex(
            float(random.randrange(500, 1000, 1)),
            float(25),
            float(1.5),
            float(2),
            float(23),
            float(180000),
            matlab.double([10 for _ in range(3)]),
            matlab.double([1.5 for _ in range(3)]),
            matlab.double([random.randrange(100, 600, 1) for _ in range(3)]),
            matlab.double([10 for _ in range(3)]),
            float(0.1 * 1000),  # us->ns
            float(4.69 * 1000),  # us->ns
            True,
            float(0.001),
            float(23 - 3.01029995664),
            False,
            True,
            nargout=9,
            background=False
        )
    end_time = datetime.now()
    total_secs = (end_time - beg_time).total_seconds()
    print(total_secs)
    TOTAL_SEC += total_secs
print("Average:{}".format(TOTAL_SEC / TIMES))
