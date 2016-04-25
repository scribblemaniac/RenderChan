

__author__ = 'scribblemaniac'

from renderchan.module import RenderChanModule
import subprocess
import os.path
import random
import tempfile

try:
    import defusedxml.ElementTree as ElementTree
except ImportError:
    print("Warning: It is recommended you install the defusedxml python module for additional security")
    import xml.ElementTree as ElementTree

class RenderChanNatronModule(RenderChanModule):
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
        # Actual supported output formats depends on the output node type
        return ["mp4", "bmp", "cin", "dpx", "fits", "hdr", "ico", "iff", "jpg", "jpe", "jpeg", "jif", "jfif", "jfi", "jp2", "j2k", "exr", "png", "pbm", "pgm", "ppm", "pfm", "psd", "pdd", "psb", "rla", "sgi", "rgb", "rgba", "bw", "int", "inta", "pic", "tga", "tpic", "tif", "tiff", "tx", "env", "sm", "vsm", "zfile", "3gp", "3g2", "avi", "h264", "m4v", "matroska", "mov", "mpeg", "mpegts", "mxf", "pfm"]

    def analyze(self, filename):
        info={"dependencies":[]}

        tree = ElementTree.parse(filename)

        for item in tree.getroot():
            if type == item.find("Type") and type.find("*") and type.text == "InputFile":
                for subitem in item.findall(".//item/Value"):
                    info["dependencies"].append("".join(subitem.itertext()))

        return info

    def render(self, filename, outputPath, startFrame, endFrame, format, updateCompletion, extraParams={}):
        updateCompletion(0.0)
        
        random_string = "%08d" % (random.randint(0,99999999))
        renderscript=os.path.join(tempfile.gettempdir(),"renderchan-"+os.path.basename(filename)+"-"+random_string+".py")
        
        script=open(os.path.join(os.path.dirname(__file__),"natron","render.py")).read()
        script=script.replace("params[WIDTH]", str(int(extraParams["width"])))\
           .replace("params[HEIGHT]", str(int(extraParams["height"])))\
           .replace("params[FORMAT]", '"'+format+'"')\
           .replace("params[INPUT_PATH]", '"'+filename+'"')\
           .replace("params[OUTPUT_DIR]", '"'+os.path.dirname(outputPath)+'"')\
           .replace("params[OUTPUT_NAME]", '"'+os.path.splitext(os.path.basename(filename))[0]+'"')
        
        f = open(renderscript,'w')
        f.write(script)
        f.close()

        commandline=[self.conf['binary'], "-t", renderscript]
        subprocess.check_call(commandline)

        updateCompletion(1.0)
