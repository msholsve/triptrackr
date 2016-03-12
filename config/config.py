import json

class Config:

    def __init__(self, confFile, verbose=False):
        self.__file = confFile
        self.verbose = verbose

        self.nonConfigKeys = list(self.__dict__.keys())
        self.nonConfigKeys.append('nonConfigKeys')

        self.__readSettings()

    def tryGetWithDefault(self, key, default):
        if not (isinstance(key,str) or isinstance(key, unicode)):
            return default
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            self.__dict__[key] = default
            self.__save()
        return default

    def setConfigValues(self, configDict):
        self.__applyDict(configDict)
        self.__save()

    def __VERBOSE(self, *args):
        if self.verbose:
            msg = ''.join([str(a) for a in args])
            print(msg)

    def __save(self):
        config = dict(self.__dict__)

        for key in self.nonConfigKeys:
            del config[key]

        with open(self.__file, 'w') as f:
            configString = json.dumps(config, sort_keys = True, indent = 4)
            f.write(configString)

    def __readSettings(self):
        try:
            with open(self.__file, 'r') as f:
                configString = f.read()
                if configString != '':
                    self.__applyDict(json.loads(configString))
        except FileNotFoundError:
            self.__save()

    def __applyDict(self, configDict):
        for key, value in configDict.items():
            self.__dict__[key] = value
 
if __name__ == '__main__':
    config = Config('Test.config')
    #config.setConfigValues(defaultConfig)
    for lol in config.__dict__:
        print(lol)