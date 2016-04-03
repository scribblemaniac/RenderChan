

__author__ = 'scribblemaniac'

from renderchan.module import RenderChanModule
import subprocess
import os
import defusedxml.ElementTree as ElementTree

class RenderChanInkscapeModule(RenderChanModule):
    def __init__(self):
        RenderChanModule.__init__(self)
        if os.name == 'nt':
            self.conf['binary']=os.path.join(os.path.dirname(__file__),"..\\..\\..\\natron\\natron.exe")
        else:
            self.conf['binary']="natron"
        self.conf["packetSize"]=0

    def getInputFormats(self):
        return ["ntp"]

    def getOutputFormats(self):
        # Natron can output practially any standard movie/image sequence format
        # But they are not worth including here because it is impossible to change which one is used
        return []

    def analyze(self, filename):
        info={"dependencies":[]}

        tree = ElementTree.parse(filename)

        for item in tree:
            if type = item.find("Type") and type.find("*") and type.text == "InputFile":
                for subitem in item.findall(".//item/Value"):
                    info["dependencies"].append(ElementTree.tostring(subitem).decode().split(">", 1)[1].rsplit("<", 1)[0])

        return info

    def render(self, filename, outputPath, startFrame, endFrame, format, updateCompletion, extraParams={}):
        updateCompletion(0.0)

        commandline=[self.conf['binary'], filename, "-b"]
        subprocess.check_call(commandline)

        updateCompletion(1.0)
