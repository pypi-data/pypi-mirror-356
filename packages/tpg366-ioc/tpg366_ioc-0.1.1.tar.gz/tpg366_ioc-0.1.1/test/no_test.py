# There is no test (yet), it depends on a sim-mode which we didn't
# implement yet.

import pytest, time, random, string
import multiprocessing as mp
from tpg366_ioc import main as ioc_main

now = time.time()

@pytest.fixture(scope='session', autouse=True)
def session_prefix():
    sp = ''.join(random.choice(string.ascii_lowercase) \
                for i in range(6))
    print(f'Session IOC prefix: "{sp}"')
    return str(sp)


@pytest.fixture(scope='session')
def ioc_prefix(session_prefix):
    return f'{session_prefix}:'


@pytest.fixture(scope='session')
def tpg_ioc(ioc_prefix):

    p = mp.Process(target=ioc_main, args=[], kwargs={'prefix': ioc_prefix,
                                                     'args': []})

    ## daemon mode will ensure that IOC exits when main process exits

    p.daemon = True
    p.start()

    print(f'Giving the IOC time to come up ({ioc_prefix})...')
    time.sleep(2)
    print(f'I guess we\'re moving: {p}')

    return {'process': p,
            'prefix': ioc_prefix}


def test_nothing():
    assert True
