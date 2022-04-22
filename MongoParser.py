SPACE = ' '
AND = ' AND '
OR = ' OR '
OPS = {
    "$or": 'OR',
    "$and": 'AND',
}

SIMPLE_OPS = {
    "$lt" : '<',
    "$lte" : '<=',
    "$gt" : '>',
    "$gte" : '>=',
    "$ne" : '!=',
    "$in" : 'in'
}

def iterate(arr, op=AND):
    ans = []
    for val in arr:
        ans.append(dfs(val, op))
    return '('+op.join(ans)+')'

def dfs(obj, op=AND):
    if type(obj) == str:
        return '= '+obj
    ans = []
    for key in obj.keys():
        if key in OPS:
            if key == '$and':
                ans.append(iterate(obj[key]))
            elif key == '$or':
                ans.append(iterate(obj[key], OR))
        elif key in SIMPLE_OPS:
            ans.append(SIMPLE_OPS[key]+SPACE+str(obj[key]))
        else:
            ans.append(key + SPACE + dfs(obj[key]))
    return op.join(ans)
            
class MongoParser:
    def __init__(self, st):
        self.st = st
        self.l = len(st)
        self.i = 0
    
    def parseArray(self):
        a = []
        val = ""
        while self.i<self.l:
            while self.st[self.i]!=',':
                if self.st[self.i]==']':
                    if val:
                        a.append(val)
                    self.i+=1
                    return a
                if self.st[self.i]=='[':
                    self.i+=1
                    a.append(self.parseArray())
                elif self.st[self.i]=='{':
                    self.i+=1
                    a.append(self.parseHashMap())
                elif self.st[self.i]!=',':
                    val+=self.st[self.i]
                    self.i+=1
            if val:
                a.append(val)
            val=''
            self.i+=1
            
            
    def parseHashMap(self):
        m = {}
        key = ""
        value = ""
        while self.i<self.l:
            if self.st[self.i]=='}':
                self.i+=1
                return m
            if self.st[self.i]==',':
                self.i+=1
                continue
            while self.st[self.i]!=':':
                key+=self.st[self.i]
                self.i+=1
            if self.st[self.i]==':':
                self.i+=1
            if self.st[self.i]=='{':
                self.i+=1
                m[key]=self.parseHashMap()
                key=""
            elif self.st[self.i]=='[':
                self.i+=1
                m[key]=self.parseArray()
                key=""
            else:
                while self.st[self.i] not in [',','}']:
                    value+=self.st[self.i]
                    self.i+=1
                m[key]=value
                key=""
                value=""
            
    
    def parse(self):
        if self.st[self.i] == '{':
            self.i+=1
            return self.parseHashMap()
        if self.st[self.i] == '[':
            self.i+=1
            return self.parseArray()

def parseJson(st):
    mp = MongoParser(st)
    return (mp.parse())

def mongoToSql(mongoQuery):
    ct1 = 0
    ct2 = 0
    arr = []
    split = mongoQuery.split('.')
    if len(split)<3:
        return "Error"
    if split[0]!="db":
        return "Error"
    if split[2][:6]!="find({":
        return "Error"
    if split[-1][-3:]!='});':
        return "Error"
    db = split[1]
    st = ".".join(split[2:])[5:-2]
    curSt = ""
    for i in range(len(st)):
        if st[i] == '{':
            ct1+=1
        elif st[i] == '}':
            ct1-=1
        if st[i] == '[':
            ct2+=1
        elif st[i] == ']':
            ct2-=1
        if ct1 < 0 or ct2 < 0:
            return "Error"
        if ct1:
            curSt+=st[i]
            
        if ct1 == 0 and st[i]!=',':
            if ct2 !=0:
                return "Error"
            arr.append(parseJson(curSt+'}'))
            curSt = ""
    if not arr or len(arr)>3:
        return "Error"
    if len(arr)==1:
        return "SELECT * from "+db+" where "+dfs(arr[0])+";"
    else:
        if arr[1]:
            return "SELECT "+", ".join(arr[1].keys())+" from "+db+" where "+dfs(arr[0])+";"
        else:
            return "SELECT * from "+db+" where "+dfs(arr[0])+";"


print(mongoToSql("db.user.find({age:{$gte:21}},{name:1,_id:1});"))
print(mongoToSql("db.user.find({age:{$gte:21}},{});"))
print(mongoToSql("db.collection_name.find({name:'Sushmitha',zip:{$in:[12345,67890]},$and:[{$or:[{province:'nb'},{province:'on'}]},{city:'toronto'},{first_name:'Steven'}],age:{$gte:21},gender:male},{first_name:1,_id:1});"))
print(mongoToSql("db.user.find({name:'julio'});"))
print(mongoToSql("db.user.find({name:'julio'})"))
print(mongoToSql("db.user.({name:'julio'});"))
print(mongoToSql("a.user.find({name:'julio'});"))
print(mongoToSql("db.userfind({name:'julio'});"))