import numpy as np
import pandas as pd
from functools import reduce

# I=PAT
# P,A,T分别对应三个文件的三个字段
# 所以每一个变量需要文件的真实路径和字段进行对应


class MathModel_PAT():
    def __init__(self,
                 ) -> None:
        self.readDict = {}
        self.valuesDict = {}

    def setenv(self,
               path: str,
               coefficient: list,
               variables: list):
        for variable in variables:
            k = None
            if variable['val'][1] == '_csv_':
                k = variable['val'][0]
                if k not in self.readDict:
                    real_path = path+k
                    self.readDict[k] = pd.read_csv(real_path)
            else:
                k = variable['val'][0]+'-*-'+variable['val'][1]
                if k not in self.readDict:
                    if variable['val'][0].split('.')[1] in ['xlsx']:
                        self.readDict[k] = pd.read_excel(
                            path+variable['val'][0], sheet_name=variable['val'][1],engine='openpyxl')
                    else:
                        self.readDict[k] = pd.read_excel(
                            path+variable['val'][0], sheet_name=variable['val'][1])
            self.valuesDict[variable['key']] = {}
            self.valuesDict[variable['key']]['key'] = variable['val'][2]
            self.valuesDict[variable['key']]['reader'] = self.readDict[k]
        # print(self.readDict)
        # print(self.valuesDict)

    def counter(self,
                path: str,
                coefficient: list,
                variables: list
                ):
        self.setenv(path, coefficient, variables)
        tmp = []
        for i in self.valuesDict.keys():
            value = self.valuesDict[i]
            v = value['reader'][value['key']]
            if v.dtype.name == 'object':
                v = pd.to_numeric(v, errors='coerce')
            tmp.append(v.fillna(method='ffill'))
        tmpr = reduce(lambda x, y: x*y, tmp)
        tmpr = tmpr.dropna()
        # r = tmpr.tolist()
        # x = list(zip(range(len(r)),r))
        return tmpr


if __name__ == '__main__':
    import json
    s = "{\"pk\":2,\"coefficient\":[],\"variable\":[{\"key\":\"P\",\"val\":[\"excel/99.xls\",\"Sheet1\",\"1段QUALITY\"]},{\"key\":\"A\",\"val\":[\"excel/sc.csv\",\"_csv_\",\"工厂\"]},{\"key\":\"T\",\"val\":[\"excel/99.xls\",\"Sheet1\",\"1段PRICE\"]}]}"
    l = json.loads(s)
    path = '/mnt/code/djcode/teserver/media/'
    coefficient = []
    t = MathModel_PAT()
    r = t.counter(path, coefficient, variables=l['variable'])
