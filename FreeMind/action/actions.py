from FreeMind.action import Action
from FreeMind.config import hddList, actionConfig, baseDir
import re
import os

class __HddSpace(Action): # TODO: better error checking...
    def defaultAction(self):
        # get disk usage
        df = self.runExternal('df').split('\n')

        if df is None:
            return None

        df = list(map(lambda row: re.split(' +', row), df))
        df = list(filter(lambda row: row[0] in hddList, df))

        if len(df) is 0:
            return None

        space = {
            hdd: {
                'total': int(d[1]),
                'free': int(d[3]),
                'full': 100 - int((int(d[3])/int(d[1])) * 100), # TODO: more efficient
                'mount': d[5]
            } for hdd in hddList for d in df if d[0] == hdd}

        return space

    def defaultIsError(self, result):
        if len(result) < len(hddList):
            return 'HDD_NOT_FOUND', [hdd for hdd in hddList if not hdd in result]

        fullHdd = [hdd for hdd in result if \
                            (result[hdd]['full']) > hddList[hdd]['maxFull']]

        return (False if len(fullHdd) is 0 else 'HDD_FULL'), fullHdd

    def __init__(self):
        super().__init__(**actionConfig['hddSpace'])

class __HddHealth(Action):
    def defaultAction(self):
        health = {hdd: self.runExternal(os.path.join(baseDir, 'utils/smartstat.sh')) \
                     for hdd in hddList}

        for hdd in health:
            if health[hdd] is None:
                return None
            else:
                # Remove the trailing \n
                health[hdd] = health[hdd][:-1]

        return health

    def defaultIsError(self, result):
        badHealt = [hdd for hdd in result if result[hdd] != 'PASSED']

        return (False if len(badHealt) is 0 else 'HDD_ILL'), badHealt

    def __init__(self):
        super().__init__(**actionConfig['hddHealth'])


# Export the Handlers
getHddSpace = __HddSpace()
getHddHealth = __HddHealth()
def getHddSumary():
    space, spaceError, spaceErrorDetails = getHddSpace.run()
    health, healthError, healthErrorDetails = getHddHealth.run()

    hdds = {}

    for hdd in hddList:
        if not (space is None or space.get(hdd) is None):
            hdds[hdd] = space[hdd]
        else:
            hdds[hdd] = {}

        if not (space is None or health.get(hdd)is None):
            hdds[hdd]['health'] = health[hdd]

        hdds[hdd]['name'] = hddList[hdd]['name']

        hdds[hdd]['color'] = 'red' if spaceError is 'ACTION_FAILED' \
                      or healthError is 'ACTION_FAILED' \
                      or hdd in healthErrorDetails else 'orange' \
                      if hdd in spaceErrorDetails else 'green'

    return hdds
