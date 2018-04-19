import numpy as np
from pyhtml import display

################################ [Sampling] ################################################################

def _check_random_state(seed):
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    return np.random.RandomState(seed)

def split_dataset(data,test_ratio,seed=None):
    rng = _check_random_state(seed)
    shuff = rng.permutation(len(data))
    test_size = int(len(data) * test_ratio)
    test,train = shuff[:test_size],shuff[test_size:]
    return data.iloc[train], data.iloc[test]

from zlib import crc32

def test_set_check(identifier, test_ratio):
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32

import hashlib

def test_set_check(identifier, test_ratio, hash=hashlib.md5):
    #print('test_set_check',identifier)
    return hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio


def split_dataset_id(data,ids,test_ratio):
    if type(ids)==str: ids = data[ids]
    in_test_set = ids.apply(test_set_check,args=(test_ratio,))
    #display({'ids':ids,'in_test':in_test_set,'inv':~in_test_set},'Split Dataset ID')
    return data.loc[~in_test_set], data.loc[in_test_set]


from sklearn.model_selection import StratifiedShuffleSplit

def split_stratified(data,strata,ratio,seed=None):
    split = StratifiedShuffleSplit(n_splits=1,test_size=ratio, random_state=seed)
    if type(strata)==str: strata = data[strata]
    train,test = (a for b in [*split.split(data,strata)] for a in b)
    return data.iloc[train], data.iloc[test]


################################ [Transformer] ################################################################


from sklearn.base import BaseEstimator, TransformerMixin

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, cols):
        self.cols = cols
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.cols].values
