# -*- coding: utf-8 *-*


class PlcDataType(object):

    data = None
    baseTag = None
    __counter = 0

    def setData(self, data):
        if(not isinstance(data, dict)):
            print 'exception1'
            return
        for i in data:
            hasatrbi = hasattr(self, i)
            if(hasatrbi):
                attr = getattr(self, i)

            res = data[i]
            if(isinstance(res, dict)):
                if(hasatrbi):
                    if(isinstance(attr, PlcDataType)):
                        attr.setData(res)
                    else:
                        setattr(self, i, res)
                else:
                    print 'No such Arrtibute ' + i + 'ignoring'
                    return
            else:
                setattr(self, i, res)
            self.data = data

    def getByStringAddress(self, address):
        if(address == ''):
            return self
        n = address.find('.')
        if (n < 0):
            return getattr(self, address)
        else:
            localAddr = address[:n]
            remoteAddr = address[n + 1:]
            remoteObj = getattr(self, localAddr)
            return remoteObj.getByStringAddress(remoteAddr)

    def setByStringAddress(self, address, newVal):
        if(address == ''):
            self.setData(newVal)
        n = address.find('.')
        remoteObj = None
        remoteAddr = ''
        if (n < 0):
        #No sub address
            if(isinstance(remoteObj, PlcDataType)):
                remoteObj = getattr(self, address)
            else:
                setattr(self, address, newVal)
                return
        else:
            localAddr = address[:n]
            remoteAddr = address[n + 1:]
            remoteObj = getattr(self, localAddr)
        remoteObj.setByStringAddress(remoteAddr, newVal)

    def __getNew(self, dataType, name):
        if(dataType in self.repo.baseTypes):
            return self.repo.baseTypes[dataType]
        elif(dataType in self.repo.dataTypes):
            res = self.repo.dataTypes[dataType]
            if(isinstance(res, list)):
                d = res[0]
                size = res[1]
                return [self.__getNew(d, name +
                '[{}]'.format(i)) for i in range(size)]
            if(isinstance(res, dict)):
                return self.repo.createNode(name, self, dataType)
        raise Exception("Unknown dataType")

    def __init__(self, dataType, _repo):
        assert(dataType in _repo.dataTypes)
        valueTypes = _repo.dataTypes[dataType]
        assert(isinstance(valueTypes, dict))
        setattr(self,'plcWriteList',[])
#        self.plcWriteList = []
        self.repo = _repo
        self.type = dataType
    
#    @Override  
    def __setattr__(self, name, value):
        if hasattr(self,"plcWriteList") and name in self.plcWriteList:
            self.repo.writePlc(self, name, value)
#        super(object,self).__setattr__(name,value)
        self.__dict__[name] = value


    def _initChildren(self):

        valueTypes = self.repo.dataTypes[self.type]
        for key in valueTypes:
            subType = valueTypes[key]
            newAttrib = self.__getNew(subType, key)
            
            setattr(self, key, newAttrib)
            self.plcWriteList.append(key)
# -*- coding: utf-8 -*-

