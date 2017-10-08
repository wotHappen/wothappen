
class QueryString:
    @staticmethod
    def fromDict(path, d):
        fullPath = path
        if fullPath[len(fullPath) - 1] == '/' and len(fullPath) > 1:
            fullPath = fullPath[:len(fullPath) - 1]
        fullPath += "?"
        isFirst = True
        for key, value in d.items():
            if isFirst:
                isFirst = False
            else:
                fullPath += '&'
            fullPath += key + '=' + value
        return fullPath

def _TEST():
    print(QueryString.fromDict("http://hello.com/", {"text": "hello", "bye": "ok"}))


