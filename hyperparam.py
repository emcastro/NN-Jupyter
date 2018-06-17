from typing import *
from random import shuffle, Random
import pandas as pd

import gcs
import time
from urllib.parse import quote
from pathlib import Path
import inspect

R = Random(421)

T = TypeVar('T', bound=tuple)  # Declare type variable


def run(
        paramSets: Iterable[T],  # 
        action: Callable[..., Dict[str, pd.DataFrame]],
        target: str,
        log_prefix='hyperparam-',
        use_gcs=False,
        reset=False):

    BASE = Path(target)

    log_file_name = Path(log_prefix + action.__name__ + '.log')

    if log_file_name.exists() and not reset:
        with open(log_file_name) as log_file:
            processed = set((line.strip() for line in log_file.readlines()))
        print(f"Reloading existing log: {log_file_name}")
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
        dfs: Dict[str, pd.DataFrame] = action(*params)

        assert type(dfs) == dict, f"action '{action.__name__}' must return a dict"

        for path, df in dfs.items():
            assert isinstance(df, pd.DataFrame), f"Invalid type {type(df)} for path '{path}'"

            for i, k in enumerate(inspect.signature(action).parameters.keys()):
                df['$' + k] = params[i]
            df['$key'] = key

            # store params
            csv = df.to_csv(index=False)

            storage_name = Path(BASE, path, key, 'data.csv')
            if use_gcs:
                ## distant storage
                gcs.mk_blob_to_GCS(str(storage_name)).upload_from_string(csv)
            else:
                ## local storage
                storage_name.parent.mkdir(parents=True, exist_ok=True)
                with open(storage_name, 'w') as store:
                    store.write(csv)

        # mark params as processed
        processed.add(key)
        with open(log_file_name, 'a') as log_file:
            log_file.write(key)
            log_file.write('\n')


if __name__ == "__main__":

    def action(a: int, b: str) -> pd.DataFrame:
        print(a, b)
        return {'result': pd.DataFrame({'a': [a, 1, 2, 3], 'b': [b, 10, 11, 12]})}

    x = [
        (a, b)  #
        for a in (1, 5, 7, 9)  #
        for b in ("a", "b,c", "c:*", "d")
    ]

    run(x, action, 'test-target', use_gcs=False)
