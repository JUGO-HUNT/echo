#!/usr/bin /env python
# -*- coding :utf8 -*-

import os
import yaml

#读取yml配置
class DealYML:
    __yamlPath = './config.yml'
    __cfgList  = {}
    

    def __init__(self):
        filePath = os.path.split(os.path.realpath(__file__))[0]
        self.__yamlPath = os.path.join(filePath, 'config.yml')

        # readYML
        f = open(self.__yamlPath, 'r', encoding='utf-8')
        cont = f.read()
        self.__cfgList = yaml.load(cont, Loader=yaml.FullLoader)

    def getCfg(self):
        return self.__cfgList

    def WriteYML(self, data):
        fw = open(self.__yamlPath, 'w', encoding='utf-8')
        yaml.dump(data, fw, allow_unicode=True, sort_keys=False)


# 获取配置dict
cfg = DealYML().getCfg()

if __name__ == '__main__':
    do = DealYML()
    cfgDict = do.getCfg()
    print (cfgDict['weather']['location']['usr3'][0])
    # dict的get方法可以设置默认值
    print(cfgDict.get('cookie',{}).get('bad', 2.2))