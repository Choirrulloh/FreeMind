import sys
sys.path.append('../server')

from flask import Flask
from flask import request

import config
import bridge

app = Flask(__name__)


@app.route('/bridge', methods=['GET'])
def handleBridge():
    action = request.args.get('action')
    status = request.args.get('status')

    # Did an OS Update
    if action == "OS_UPDATE":
        return bridge.handleOsUpdate(status)

    elif action == "FM_UPDATE":
        return bridge.handleOsUpdate(status)

    elif action == "BACKUP":
        return bridge.handleBackup(status)

    elif action == "DO_BACKUP":
        return bridge.doBackUp()

    elif action == "HDD_ERROR":
        return bridge.handleHddError()




