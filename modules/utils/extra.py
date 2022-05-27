def isfloat(self)->bool:
    ssplit = self.split('.')
    length: int = len(ssplit)
    FloatList: list = []
    if 0 < length <= 2:
        for x in ssplit:
            FloatList.append(x.isdecimal())
        if False in FloatList:
            return False
        else:
            return True
    else:
        return False