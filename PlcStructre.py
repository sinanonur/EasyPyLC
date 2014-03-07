baseTypes = { 'double': 0.0 ,'int':0, 'bool':True}
#Just dummy structres for test
dataTypes = {'pair':{'lc':'LC','a2':'LL'}, #Just dummy structres for test
             'Altitude':{'al':'double','ti':'double'}, 
             'LL':['bool',10], 
             'LC':{'alt':'Altitude','temp':'Temp' },
             'Temp':{'C':'double','F':'double'}}


class PlcDataType(object):
    
    data = None;
    baseTag = None;
    
    def setData(self,data):
        if(not isinstance(data,dict)):
            print 'exception1'
            return;
        for i in data:
            hasatrbi = hasattr(self,i);
            if(hasatrbi):
                attr = getattr(self,i);
            
            res = data[i]
            if(isinstance(res,dict)):
                if(hasatrbi):
                    if(isinstance(attr,PlcDataType)):
                        attr.setData(res);
                    else:
                        setattr(self,i,res)
                else:
                    print 'No such Arrtibute '+ i + 'ignoring';
                    return;
            else:
                setattr(self,i,res);
            self.data = data;
    
    
    
    
    def getByStringAddress(self, address):
        if(address == ''):
            return self;
        n = address.find('.')
        remote = None;
        if (n < 0):
            return getattr(self,address);
        else:
            localAddr = address[:n];
            remoteAddr = address[n+1:];
            remoteObj =  getattr(self,localAddr);
            return remoteObj.getByStringAddress(remoteAddr);
        
    def setByStringAddress(self, address,newVal):
        if(address == ''):
            self.setData(newVal);
        n = address.find('.')
        remoteObj = None;
        remoteAddr = ''
        if (n < 0): #No sub address
            if(isinstance(remoteObj,PlcDataType)):
                remoteObj =  getattr(self,address);
            else:
                setattr(self,address,newVal);
                return;
        else:
            localAddr = address[:n];
            remoteAddr = address[n+1:];
            remoteObj =  getattr(self,localAddr);
        remoteObj.setByStringAddress(remoteAddr,newVal);
    
    def getNew(self,dataType):
        if(baseTypes.has_key(dataType)):
           return baseTypes[dataType];
        elif(dataTypes.has_key(dataType)):
            res = dataTypes[dataType];
            if(isinstance(res,list)):
                d = res[0];
                size = res[1];
                return [self.getNew(d) for i in range(size)]
            if(isinstance(res,dict)):
                return PlcDataType(dataType);
        raise Exception("Unknown dataType")
    
    
    
    def __init__(self,dataType):
        assert(dataTypes.has_key(dataType));
        valueTypes = dataTypes[dataType];
        assert(isinstance(valueTypes,dict));
        for key in valueTypes:
            subType = valueTypes[key];
            setattr(self,key,self.getNew(subType));
        
