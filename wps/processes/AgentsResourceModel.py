"""
WPS interface to Agents-based resource model

2013-10-14, Peter.Kutschera@ait.ac.at
"""

"""
    Copyright (C) 2014  AIT / Austrian Institute of Technology
    http://www.ait.ac.at
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 2 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/gpl-2.0.html
"""


from pywps.Process import WPSProcess                                
import sys
import json
import requests
from xml.sax.saxutils import escape
import time
import uuid
import subprocess
import os

class Process(WPSProcess):
    def __init__(self):
        # init process
        WPSProcess.__init__(
            self,
            identifier="AgentsResourceModel", #the same as the file name
            version = "1.0",
            title="Agents-based resource model",
            storeSupported = True,
            statusSupported = True,
            abstract="Runs resource model starting from a given WorldState",
            grassLocation = False)
        self.WorldState = self.addLiteralInput (identifier = "WorldStateId",
                                                # type = type(""), # default: integer
                                                title = "One particular WorldState")
        self.duration = self.addLiteralInput (identifier = "duration",
                                                title = "Simulated time span [minutes]")
        self.stepduration = self.addLiteralInput (identifier = "stepduration",
                                                title = "Time between created intermediate WorldStates [minutes]")
        self.Answer=self.addLiteralOutput(identifier = "StatusPage",
                                          type = type (""),
                                          title = "URL of status page")

                                           
    def execute(self):
        baseUrl = 'http://193.40.13.83/PilotC/Startup/startup.aspx'

        worldStateId = self.WorldState.getValue();
        self.status.set("Check WorldState {} status".format (worldStateId), 10)
        duration = self.duration.getValue();
        stepduration = self.stepduration.getValue();
        self.status.set("duration = {}, stepduration = {}".format (duration, stepduration), 11)

        self.status.set("Will start model now", 50)

        params = {
            'wsid' :  worldStateId, 
            'intervalsec' : stepduration * 60,
            'totalsimtimesec' : duration * 60
            }

        statusURL = requests.get(baseUrl, params=params) 
        
        self.status.set("request returned {}".format (statusURL.status_code), 90)

        if statusURL.status_code != 200:
            return "Problem staring model: {}".format (statusURL.text)

        result = statusURL.json()

        self.status.set("request returned json: {}".format (result), 91)

        if "error" in result:
            return result["error"]

        if "statusURL" in result:
            self.status.set("Model run started", 99)
            self.Answer.setValue(escape (result["statusURL"]))
            return

        return "Problem staring model: {}".format (statusURL.text)

            

        
def fork_exec_disown(cmd, dir="/tmp"):
    if os.fork() == 0:
        if os.fork():
            sys.exit(0)
        os.chdir(os.path.expanduser(dir))
        os.execvp ("/bin/bash", cmd)
    os.wait()
