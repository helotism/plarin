# -*- coding: utf-8 -*-
"""
An implementation of a ring buffer.
"""

#
#http://forum.micropython.org/viewtopic.php?t=601#p3491
#https://forum.micropython.org/viewtopic.php?t=1702
#
import array

class Circularbuffer:
    """A ring buffer that may be queried piecewise or by a threshold value.

    Attributes:
        size (int): How many items the buffer shall hold.
    """

    def __init__(self, size, typecode='f'):
        self.appends = 0
        self.write_pointer = 0
        self.size = size
        self.read_pointer = -1
        self.threshold = self.size // 2
        self.data = array.array(typecode, [0 for i in range(self.size)])
        self.emtpy = True
        self.full = False
        self.avg_exp_decayed = 0

    def append(self, value):
        self.appends += 1
        #print(value, self.avg_exp_decayed, abs(value - self.avg_exp_decayed))
        if self.appends > 10 and abs(value - self.avg_exp_decayed) > 2 *  self.avg_exp_decayed:
            value = self.avg_exp_decayed
            print("rewriting sensor history")
        self.avg_exp_decayed = (0.2 * value) + (0.8 * self.avg_exp_decayed)
        #print()
        self.data[self.write_pointer] = value
        if (self.write_pointer + 1) >= self.size:
            self.full = True
        if self.emtpy is True:
            self.emtpy = False
        self.write_pointer = (self.write_pointer + 1) % self.size

    def sum(self):
        print(sum(self.data))

    def info(self):
        print(self.data)
        print("len: ", len(self.data))
        print("write_pointer: ", self.write_pointer)
        print("full: ", self.full)

    def get_by_threshold(self):
        if self.read_pointer == -1:
            #initial read
            self.read_pointer = (self.write_pointer - 1) % self.size

        for j in range(self.threshold):
            if self.full is False and self.read_pointer > 0 and self.read_pointer >= self.write_pointer:
                print("+++1", self.read_pointer, self.data[self.read_pointer], self.read_pointer - 1)
                self.read_pointer = self.read_pointer - 1
            elif self.full is True:
                print("+++2", self.read_pointer, self.data[self.read_pointer], (self.read_pointer - 1) % self.size)
                if self.read_pointer == 0:
                    self.full = False
                self.read_pointer = (self.read_pointer - 1) % self.size
            else:
                self.emtpy = True
            j += 1

#b = Circularbuffer(8)
#
#for i in [ 1, 2, 1, 3, 2, 4, 1, 3, 2, 4, 2, 12, 1]:
#  b.append(i)




#This also works:
#http://www.onlamp.com/pub/a/python/excerpt/pythonckbk_chap1/index1.html
#class RingBuffer(object):
#    def __init__(self,size_max):
#        self.max = size_max
#        self.data = [  ]
#    def _full_append(self, x):
#        print("f", x)
#        self.data[self.cur] = x
#        self.cur = (self.cur+1) % self.max
#    def _full_get(self):
#        return self.data[self.cur:]+self.data[:self.cur]
#    def append(self, x):
#        print("_", x)
#        self.data.append(x)
#        if len(self.data) == self.max:
#            self.cur = 0
#            # Permanently change self's methods from non-full to full
#            self.append = self._full_append
#            self.tolist = self._full_get
#    def tolist(self):
#        return self.data
