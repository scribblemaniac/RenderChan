__author__ = 'scribblemaniac'

import sys
import os.path

import NatronEngine

WIDTH = "width"
HEIGHT = "height"
FORMAT = "format"
INPUT_PATH = "input_path"
OUTPUT_DIR = "output_dir"
OUTPUT_NAME = "output_name"

params = {WIDTH: 480,
          HEIGHT: 270,
          FORMAT: "png",
          INPUT_PATH: "",
          OUTPUT_DIR: "",
          OUTPUT_NAME: ""}

write_oiio_exts = ["png", "bmp", "cin", "dpx", "fits", "hdr", "ico", "iff", "jpg", "jpe", "jpeg", "jif", "jfif", "jfi", "jp2", "j2k", "exr", "pbm", "pgm", "ppm", "pfm", "psd", "pdd", "psb", "rla", "sgi", "rgb", "rgba", "bw", "int", "inta", "pic", "tga", "tpic", "tif", "tiff", "tx", "env", "sm", "vsm", "zfile"]
write_ffmpeg_exts = ["mp4", "3gp", "3g2", "avi", "h264", "m4v", "matroska", "mov", "mpeg", "mpegts", "mxf"]
write_pfm_exts = ["pfm"] # Could be missing some here

oiio_nodes = []
ffmpeg_nodes = []
pfm_nodes = []
other_render_nodes = []

app.loadProject(params[INPUT_PATH])

def scanNodes(nodes):
    for node in nodes:
        if node.getPluginID() == "fr.inria.built-in.Group":
            scanNodes(node.getChildren())
        elif node.getPluginID() == "fr.inria.openfx.WriteOIIO":
            oiio_nodes.append(node)
        elif node.getPluginID() == "fr.inria.openfx.WriteFFmpeg":
            ffmpeg_nodes.append(node)
        elif node.getPluginID() == "fr.inria.openfx.WritePFM":
            pfm_nodes.append(node)
        else:
            # Heuristics to catch custom output nodes
            render_button = None
            file_output = None
            
            # TODO refactor this to use getParam
            for param in node.getParams():
                if isinstance(param, NatronEngine.ButtonParam) and (param.getLabel() == 'Render' or param.getScriptName() == 'startRender'):
                    render_button = param
                elif isinstance(param, NatronEngine.OutputFileParam) and (param.getLabel() == 'File' or param.getScriptName() == 'filename'):
                    file_output = param
            
            if render_button and file_output:
                other_render_nodes.append(node)

scanNodes(app.getChildren())

file_counter = 1

for node in oiio_nodes:
    if not isinstance(node.getParam("filename"), NatronEngine.OutputFileParam) or not isinstance(node.getParam("startRender"), NatronEngine.ButtonParam):
        print("Warning: Could not render WriteOIIO node '" + node.getLabel() + "', internal error occured.")
        continue
    orig_path = node.getParam("filename").get()
    
    if params[FORMAT] in write_oiio_exts:
        ext = params[FORMAT]
    else:
        orig_ext = os.path.splitext(orig_path)[1]
        if orig_ext in write_oiio_exts:
            ext = orig_ext
        else:
            ext = write_oiio_exts[0]
    
    path = os.path.join(params[OUTPUT_DIR], "%s-%d.%s" % (params[OUTPUT_NAME], file_counter, ext), "%s-%d.####.%s" % (params[OUTPUT_NAME], file_counter, ext))
    file_counter += 1
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    node.getParam("filename").set(path)
    node.getParam("startRender").trigger()

for node in ffmpeg_nodes:
    if not isinstance(node.getParam("filename"), NatronEngine.OutputFileParam) or not isinstance(node.getParam("startRender"), NatronEngine.ButtonParam):
        print("Warning: Could not render WriteFFMPEG node '" + node.getLabel() + "', internal error occured.")
        continue
    orig_path = node.getParam("filename").get()
    
    if params[FORMAT] in write_ffmpeg_exts:
        ext = params[FORMAT]
    else:
        orig_ext = os.path.splitext(orig_path)[1]
        if orig_ext in write_ffmpeg_exts:
            ext = orig_ext
        else:
            ext = write_ffmpeg_exts[0]
    
    path = os.path.join(params[OUTPUT_DIR], "%s-%d.%s" % (params[OUTPUT_NAME], file_counter, ext))
    file_counter += 1
    node.getParam("filename").set(path)
    node.getParam("startRender").trigger()

for node in pfm_nodes:
    if not isinstance(node.getParam("filename"), NatronEngine.OutputFileParam) or not isinstance(node.getParam("startRender"), NatronEngine.ButtonParam):
        print("Warning: Could not render WritePFM node '" + node.getLabel() + "', internal error occured.")
        continue
    orig_path = node.getParam("filename").get()
    
    if params[FORMAT] in write_pfm_exts:
        ext = params[FORMAT]
    else:
        orig_ext = os.path.splitext(orig_path)[1]
        if orig_ext in write_pfm_exts:
            ext = orig_ext
        else:
            ext = write_pfm_exts[0]
    
    path = os.path.join(params[OUTPUT_DIR], "%s-%d.%s" % (params[OUTPUT_NAME], file_counter, ext), "%s-%d.####.%s" % (params[OUTPUT_NAME], file_counter, ext))
    file_counter += 1
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    node.getParam("filename").set(path)
    node.getParam("startRender").trigger()
    
sys.exit()