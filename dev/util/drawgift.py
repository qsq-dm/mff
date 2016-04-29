# -*- coding: utf-8 -*-

import random
import bisect




class DrawGift(object):
    ''' 抽奖 '''
    def __init__(self, items):  
        weights = [w for _,w in items]  
        self.goods = [x for x,_ in items]  
        self.total = sum(weights)  
        self.acc = list(self.accumulate(weights))  
  
    def accumulate(self, weights):#累和.如accumulate([10,40,50])->[10,50,100]  
        cur = 0  
        for w in weights:  
            cur = cur+w  
            yield cur  
  
    def __call__(self):
        if not self.total: return None
        return self.goods[bisect.bisect_right(self.acc , random.uniform(0, self.total))] 



def draw_prize(prize_list):
    ''' 抽奖 '''
    wr = DrawGift(prize_list)  
    return wr()


def test_drawprize():
    prize_list  = [('iphone', 10), ('ipad', 40), ('itouch', 50)]
    print draw_prize(prize_list)