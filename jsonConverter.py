

class json:
    @staticmethod
    def StrToDict(string):
        #getting curlie brackets

        curlies = list()
        curlies.append(list())
        index = 0
        char = '{'
        while True:
            index = string.find(char, index)
            if index == -1:
                if char == '{':
                    char = '}'
                    curlies.append(list())
                    index = 0
                    continue
                if char == '}':
                    index = 0
                    break
            else:
                curlies[len(curlies)-1].append(index)
                index += 1
        #finding apostrophies
        index = 0 
        char = "'"
        apostrophies = [[]]
        while True:
            index = string.find(char, index)
            if index == -1:
                if char == "'":
                    char = '"'
                    index = 0
                    apostrophies.append([])
                    continue
                else:
                    index = 0
                    break
            else:
                temp = string.find(char, index+1)
                if index == -1:
                    raise ValueError("something went wrong")
                else:
                    apostrophies[len(apostrophies)-1].append((index, temp))
                index = temp +1
        #matching the curlies
        #this is a matching algorithm written by me and designed by me in 30  mins
        fCurlies = list()
        temp = list()
        i = 0
        while True:
            if len(curlies[0]) == 0:
                break
            for i in range(len(curlies[0])):
                if curlies[0][i] < curlies[1][0]:
                    if i == len(curlies[0])-1:
                        fCurlies += [(curlies[0][len(curlies[0])-i-1],curlies[1][i]) for i in range(len(curlies[0]))]
                        curlies = [[],[]]
                        break
                    else:
                        temp.append(i)
                else:
                    fCurlies.append((curlies[0][temp[-1]], curlies[1][0]))
                    
                    curlies[1].pop(0); curlies[0].pop(temp[-1])
                    temp.clear()
                    break
        #sorting curlies
        main = json.GetMainCurlies(fCurlies)
        lists = json.getLists(string)
        #getting all commas and all valid two points
        stringClone = string
        index = 0
        res = [[]]
        coms = []
        tpoints = list()
        char = ','
        while True:
            index = string.find(char, index)
            if index == -1:
                if char == ',':
                    char = ":"
                    index = 0
                    res.append(list())
                    continue
                else:
                    break
            else:
                if (not (json.isInside(index, apostrophies[0]) or json.isInside(index, apostrophies[1]))) and not json.isInside(index, main[1]) and not json.isInside(index, lists):
                    res[-1].append(index)
                index +=1

        coms = res[0]; tpoints = res[1]
        #breaking the list into segments
        segments = list()
        stringClone = ''.join([i for (e,i) in enumerate(string) if e != main[0][0] and e!=main[0][1]])
        del res
        for i,e in enumerate(coms):
            if i != 0:
                segments.append(stringClone[coms[i-1]:e-1])
            else:
                segments.append(stringClone[:e-1])
        try:
            segments.append(stringClone[coms[-1]:])
        except:
            segments = [stringClone]
        #splitting each segment into name and value
        dif = 0
        splitSegments = []
        for (i,e) in enumerate(segments):
            #print(f"e: {e}, diff: {dif}")
            if dif == 0:
                splitSegments.append([e[:tpoints[i]-1],e[tpoints[i]:]])
                dif += len(e)+1
            else:
                splitSegments.append([e[:tpoints[i]-dif-1],e[tpoints[i]-dif:]])
                dif += len(e)+1
        out = {}
        for segment in splitSegments:
            name = segment[0]
            temp = name.replace(' ', '')
            firstChar = temp[0]
            name = name[name.index(firstChar)+1:]
            name = name[::-1]
            firstChar = name.replace(' ', '')[0]
            name = name[name.index(firstChar)+1:]
            name = name[::-1]
            value = segment[1]
            out[name] = json.tf(value)
        return out
    @staticmethod
    def GetMainCurlies(curliesList):
        opened = [e[0] for e in curliesList]
        closed = [e[1] for e in curliesList]
        wanted = (min(opened), max(closed))
        if wanted not in curliesList:
            raise ValueError("unknown error in the string") 
        else:
            return [wanted, [e for e in curliesList if e != wanted]]
    
    @staticmethod
    def isInside(inIndex, array):
        for element in array:
            if inIndex < element[1] and inIndex > element[0]:
                return True
        return False
    @staticmethod
    def getStrings(string):
        index = 0
        res = []
        char = '"'
        while True:
            index = string.find(char, index)
            if index == -1 and char == '"':
                char = "'"
                index = 0
                continue
            elif index == -1 and char == "'":
                index = 0
                break
            else:
                temp = string.find(char, index+1)
                if temp == -1:
                    raise ValueError("strings not matching")
                else:
                    res.append((index, temp))
                    index = temp +1
        return res
    def getLists(string):
        index = 0
        res = [[]]
        char = "["
        while True:
            index = string.find(char, index)
            if index == -1 and char == "[":
                char = "]"
                index = 0
                res.append([])
            elif index == -1 and char == "]":
                index = 0
                char = "("
                res.append([])
            elif index == -1 and char == "(":
                index = 0
                char = ")"
                res.append([])
            elif index == -1 and char == ")":
                index = 0
                break
            else:
                res[-1].append(index)
                index +=1
        lis = [res[0], res[1]]
        tup = [res[2], res[3]]
        res.clear()
        #sorting the lists:
        temp = list()
        curr = lis
        while True:
            if len(curr[0]) == 0:
                if len(tup[0]) == 0:
                    break
                else:
                    curr = tup
                    tup.clear(); tup = [[], []]
            for i in range(len(curr[0])):
                if curr[0][i] < curr[1][0]:
                    if i == len(curr[0])-1:
                        res += [(curr[0][len(curr[0])-i-1],curr[1][i]) for i in range(len(curr[0]))]
                        curr = [[],[]]
                        break
                    else:
                        temp.append(i)
                else:
                    res.append((curr[0][temp[-1]], curr[1][0]))
                    curr[1].pop(0); curr[0].pop(temp[-1])
                    temp.clear()
                    break
        return res
    @staticmethod
    def cut(string):
        strings = json.getStrings(string)
        index = 0
        coms = []
        while True:
            index = string.find(',', index)
            if index == -1:
                index = 0
                break
            else:
                coms.append(index)
                index +=1
        temp = string.replace(' ', '')
        firstChar = temp[0]
        string = string[string.index(firstChar)+1:]
        string = string[::-1]
        firstChar = string.replace(' ', '')[0]
        string = string[string.index(firstChar)+1:]
        string = string[::-1]
        segments = list()
        for i,e in enumerate(coms):
            if i != 0:
                segments.append(string[coms[i-1]:e-1])
            else:
                segments.append(string[:e-1])
        segments.append(string[coms[-1]:])
        return segments
    @staticmethod 
    def type(string):
        string = string.replace(' ', '')
        if string[0] == '"' or string[0] == "'":
            return 'string'
        if string[0] == "[":
            return 'list'
        if string[0] == '{':
            return "dict"
        if string[0] == "(":
            return 'tuple'
        if "True" in string or "False" in string:
            return 'bool'
        if int(string):
            return 'int'
        else:
            return None
    @staticmethod
    def tf(string):
        t = json.type(string)
        if t == 'int':
            return int(string)
        elif t == 'string':
            quotes = json.getStrings(string)
            main = (len(string), len(string))
            for q in quotes:
                if q[0] < main[0]:
                    main = q
            return string[main[0] + 1: main[1]]
        elif t == 'list' or t == 'tuple':
            output = list()
            l_str = json.cut(string)
            for st in l_str:
                output.append(json.tf(st))
            if t == 'tuple':
                return tuple(*output)
            return output
        elif t == 'dict':
            output = json.StrToDict(string)
            return output
        elif t == 'bool':
            if "True" in string:
                return True
            else:
                return False
        else:
            return None

dic = {
    "name": ["achraf", "moha"],
    "age": 16,
    "good": True

}

print(json.StrToDict(str(dic))['good'])