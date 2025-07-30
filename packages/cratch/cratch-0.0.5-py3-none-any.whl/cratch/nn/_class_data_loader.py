#coding:UTF-8

"""
# Name    : _class_data_loader.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Neural netrwork tool of data loader.
"""

import numpy as np
import random

#-----------------------------------------------------------------------------#
class DataLoader:
    """
    Original data loader class

    Parameters
    ----------
    dataset : list
        [input data(ndarray,2-D) and output data (ndarray, 2-D)]
    batch_size : int
        number of batch size (default:128)
    shuffle : bool
        True : shuffle(default), False : not shuffle
    """
    def __init__(self, dataset, batch_size=128, shuffle=True):
        self.dataset = dataset
        self.shuffle = shuffle
        self.batch_size = batch_size
        assert all([dataset[i].shape[0] == dataset[0].shape[0]\
            for i in range(len(dataset))]),\
            'All the element must have the same length ...'
        self.data_size = dataset[0].shape[0]
        self.shuffled_idx = np.arange(self.data_size, dtype=np.int32)

    def __iter__(self):
        self.n = 0
        if self.shuffle:
            random.shuffle(self.shuffled_idx)
            self.dataset = [v[self.shuffled_idx] for v in self.dataset]
        return self

    def __next__(self):
        idx1 = self.batch_size*self.n
        idx2 = min(self.batch_size*(self.n + 1), self.data_size)
        if idx1 >= self.data_size:
            raise StopIteration()
        value = [v[idx1:idx2] for v in self.dataset]
        self.n += 1
        return value

    def __del__(self):
        return 0

#-----------------------------------------------------------------------------#
