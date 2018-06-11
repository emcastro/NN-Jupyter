#from tingyp import *
from typing import *
from random import shuffle, Random
import pandas as pd
import gcs
import time
from urllib.parse import quote
from pathlib import Path

R = Random(421)

T = TypeVar('T', bound=tuple)  # Declare type variable

BASE = Path('.')


def run(paramSets: Iterable[T], action: Callable[[T], pd.DataFrame],
        target: str):
    log_file_name = Path(BASE, 'log')

    if log_file_name.exists():
        with open(log_file_name) as log_file:
            processed = set((line.strip() for line in log_file.readlines()))
    else:
        processed = set()

    paramList = list(paramSets)
    shuffle(paramList, R.random)
    for params in paramList:
        # if params not computed
        key = '/'.join((quote(str(param)) for param in params))
        if key in processed:
            continue

        # compute the action
        df = action(params)

        # store params
        csv = df.to_csv(index=False)

        ## local storage
        storage_name = Path(BASE, 'store', key)
        storage_name.mkdir(parents=True)
        with open(Path(storage_name, 'data.csv'), 'w') as store:
            store.write(csv)
        ## distant storage
        #gcs.mk_blob_to_GCS('abcd').upload_from_string(csv)

        # mark params as processed
        processed.add(key)
        with open(log_file_name, 'a') as log_file:
            log_file.write(key)
            log_file.write('\n')


if __name__ == "__main__":

    def action(a: int, b: str) -> pd.DataFrame:
        print(a, b)
        return pd.DataFrame({'a': [a], 'b': [b]})

    x = [
        (a, b)  #
        for a in (1, 5, 7, 9)  #
        for b in ("a", "b,c", "c:*", "d")
    ]

    run(x, lambda t: action(*t), './tatarget')
