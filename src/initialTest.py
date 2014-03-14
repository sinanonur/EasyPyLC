# -*- coding: utf-8 *-*
from PlcRepository import PlcRepository




class DummyOpc(object):
    def read(self, adr):
        print('read.....' + str(adr))
    def write(self,pair):
        print 'write.... ' + str(pair[1]) + ' ---> ' + pair[0]




repo = PlcRepository(DummyOpc(), 'S103201_Chamber2')
Ch = repo.createNode('Ch', None, 'Chamber')

repo.readPlc(Ch)
#pair = repo.createNode('pair', None, 'pair')

Ch.setByStringAddress('LC.Altitude', 5)

Ch.ML.Altitude = 1

#repo.readPlc(pair)
