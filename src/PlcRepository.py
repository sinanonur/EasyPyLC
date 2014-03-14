# -*- coding: utf-8 *-*

from PlcDataType import PlcDataType


class PlcRepository(object):
    baseTypes = {'double': 0.0, 'int': 0, 'bool': True}
    dataTypes = {'pair': {'lc': 'Compartment', 'list': 'LL'},
             'LL': ['double', 10],
             'Compartment': {'Altitude': 'double', 'Temp': 'double'},
             'Temp': {'C': 'double', 'F': 'double'},
             'Chamber': {'LC': 'Compartment', 'ML': 'Compartment'}}
    __objectAddressDict = {}

    def __findTagIndex(self, tagName):
        if tagName in self.__tagDictionary:
             return self.__tagDictionary[tagName]
        return None
        
    def __addTag(self, tagName):
        if tagName in self.__tagDictionary:
            return  #already exists
        index = len(self.__tagList)
        self.__tagList.append(tagName)
        self.__tagDictionary[tagName] = index

    def __init__(self, opcConnection, baseAddress):
        self._opc = opcConnection
        self.__baseAddress = baseAddress
        self.__tagList =[]
        self.__tagDictionary = []
        
    def getBaseAddress(self, forListing = False):
        if forListing:
            return self.__baseAddress + '.online.'
        return '['+ self.__baseAddress + ']'

    def createNode(self, name, caller, plcType):
        if (caller in self.__objectAddressDict):
            address = self.__objectAddressDict[caller] + '.' + name
        else:
            address = name
        node = PlcDataType(plcType, self)
        self.__objectAddressDict[node] = address
        node._initChildren()
        return node

    def readPlc(self, plcData):
        if plcData in self.__objectAddressDict:
            address = self.__objectAddressDict[plcData]
            return self._readPlcDataRecursive(address, plcData.type)
        else:
            raise Error("Plc data not in repo")
    
    def writePlc(self, plcData, attributeName, value):
        print 'write plc'
        if plcData in self.__objectAddressDict:
            address = self.__objectAddressDict[plcData]
            pair = [self.getBaseAddress() + address+ '.' + attributeName, value]
            self._opc.write(pair)
        else:
            raise Error("Plc data not in repo")

    def _readPlcDataRecursive(self, plcAddress, dataType):
        #print 'dataType: {}'.format(dataType)
        if dataType in self.baseTypes:
            result = self._opc.read(self.getBaseAddress() + plcAddress)
            #print '--base type'
            return result
        elif dataType in self.dataTypes:
            #print '--dataType'
            nameType = self.dataTypes[dataType]
            if isinstance(nameType, list):
                return [
                    self._readPlcDataRecursive(
                        plcAddress + '[' + str(i) + ']', nameType[0])
                        for i in range(nameType[1])
                        ]
            else:
                return {
                    name: self._readPlcDataRecursive(
                        plcAddress + '.' + name, nameType[name])
                        for name in nameType}

