import os
import sys
import glob
import ntpath
# this file same as jpg version, only different is output .yuv

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def get_frame_10bits(filePath, frame, outputPath, resolution):
    ss = frame/30.0
    os.system(f"ffmpeg -r 30 -ss {ss} -s {resolution[0]}x{resolution[1]} -pix_fmt yuv420p10le -i {filePath} -frames:v 1 {outputPath}")

def get_frame_16bits(filePath, frame, outputPath, resolution):
    ss = frame/30.0
    os.system(f"ffmpeg -r 30 -ss {ss} -s {resolution[0]}x{resolution[1]} -pix_fmt yuv420p16le -i {filePath} -frames:v 1 {outputPath}")

def move_file(filename, source_views, outputPath, destination, frame):
    for source_view in source_views:
        if(f"v{source_view}_" in filename):
            os.system(f"mv {outputPath} {destination}/{source_view}/{frame}.yuv")
        elif(f"v0{source_view}_" in filename):
            os.system(f"mv {outputPath} {destination}/{source_view}/{frame}.yuv")

if __name__=="__main__":
    dataset = sys.argv[1]
    source_views = {
        "IntelFrog": [1,3,5,7,9,11,13],
        "OrangeKitchen": [0,2,10,12,14,22,24],
        "PoznanCarpark": [0,1,2,4,6,7,8],
        "PoznanFencing": [0,1,2,4,6,7,8],
        "PoznanHall": [0,1,2,4,6,7,8],
        "PoznanStreet": [0,1,2,4,6,7,8],
        "TechnicolorPainter": [0,3,5,9,10,12,15],
        "ClassroomVideo": [0,7,8,10,11,12,13],
        "TechnicolorMuseum": [0,1,4,11,12,13,17],
        "TechnicolorHijack": [1,2,3,4,5,8,9]
    }
    target_frames = {
        "IntelFrog": [50,100,150,200,250],
        "OrangeKitchen": [16,32,48,54,72],
        "PoznanCarpark": [40,80,120,160,200],
        "PoznanFencing": [40,80,120,160,200],
        "PoznanHall": [80,160,240,320,400],
        "PoznanStreet": [40,80,120,160,200],
        "TechnicolorPainter": [50,100,150,200,250],
        "ClassroomVideo" : [20,40,60,80,100],
        "TechnicolorMuseum": [50,100,150,200,250],
        "TechnicolorHijack": [50,100,150,200,250]
    }
    resolution = {
        "IntelFrog": (1920,1080),
        "OrangeKitchen": (1920,1080),
        "PoznanCarpark": (1920,1088),
        "PoznanFencing": (1920,1080),
        "PoznanHall": (1920,1088),
        "PoznanStreet": (1920,1088),
        "TechnicolorPainter": (2048,1088),
        "ClassroomVideo": (4096,2048),
        "TechnicolorMuseum": (2048,2048),
        "TechnicolorHijack": (4096,4096)

    }
    os.system(f"mkdir /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}")
    os.system(f"mkdir /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp")
    os.system(f"mkdir /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/imgs")
    os.system(f"mkdir /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/depth")

    for view in source_views[dataset]:
        os.system(f"mkdir /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/imgs/{view}")
        os.system(f"mkdir /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/depth/{view}")
    if(dataset=="ClassroomVideo" or dataset == "TechnicolorMuseum" or dataset == "TechnicolorHijack"):
        filePathList_t = glob.glob(f"/mnt/data1/tsehou/{dataset}/*texture*.yuv")
        filePathList_d = glob.glob(f"/mnt/data1/tsehou/{dataset}/*depth*.yuv")
    else:
        filePathList_t = glob.glob(f"/mnt/data1/tsehou/perspective_dataset/{dataset}/*texture*.yuv")
        filePathList_d = glob.glob(f"/mnt/data1/tsehou/perspective_dataset/{dataset}/*depth*.yuv")


    # texture
    for frame in target_frames[dataset]:
        for filePath in filePathList_t:
            outputfilename = path_leaf(filePath)
            outputfilename = os.path.splitext(outputfilename)
            get_frame_10bits(filePath,frame,f'/home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp/{outputfilename[0]}.yuv',resolution[dataset])
            move_file(f"{outputfilename[0]}.yuv", source_views[dataset], f'/home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp/{outputfilename[0]}.yuv', f"/home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/imgs", frame)
        os.system(f"rm /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp/*")
    # os.system(f"rm -r /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp")
    # depth
    for frame in target_frames[dataset]:
        for filePath in filePathList_d:
            outputfilename = path_leaf(filePath)
            outputfilename = os.path.splitext(outputfilename)
            if(dataset!="OrangeKitchen"):
                get_frame_16bits(filePath,frame,f'/home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp/{outputfilename[0]}.yuv',resolution[dataset])
            else:
                get_frame_10bits(filePath,frame,f'/home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp/{outputfilename[0]}.yuv',resolution[dataset])
            move_file(f"{outputfilename[0]}.yuv", source_views[dataset], f'/home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp/{outputfilename[0]}.yuv', f"/home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/depth", frame)
        os.system(f"rm /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp/*")
    os.system(f"rm -r /home/tsehou/tmiv-3.1/tmiv/script/source_view_frame/{dataset}/temp")
        