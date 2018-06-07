#from tingyp import *
from typing import *
from random import shuffle, Random
import pandas as pd
import time

R = Random(421)

T = TypeVar('T', bound=Tuple)  # Declare type variable

def run(params: Iterable[T], action: Callable[[T], pd.DataFrame]):
    paramList = list(params)
    shuffle(paramList, R.random)
    for params in paramList:
        # if params not computed
        df = action(params)
        # store params
        #print (df)


if __name__ == "__main__":

    def action(a: int, b: str) -> pd.DataFrame:
        print(a, b)
        return pd.DataFrame({
            'a': [a],
            'b': [b]
        })

    x = [
        (a, b)  #
        for a in (1, 5, 7, 9)  #
        for b in ("a", "b", "c", "d")
    ]

    run(x, lambda t: action(*t))
