import os
import json
import glob
import sys
# calculate WS-PSNR for each output of TMIV decoder
# usage:
# python3 WSPSNR.py {dataset}
# 


def run_psnr(target_frames,target_views,dataset_PATH,output_PATH,w,h):
    for frame in target_frames:
        for TV in target_views:
            for PP in numofViewPerPass:
                # modify cfg
                with open(WSPSNR_cfg,'r') as load_f:
                    cfg = json.load(load_f)
                    if(len(PP)==1):
                        cfg['Reconstructed_file_path'] = f"{output_PATH}/f{frame}/output/{TV}_{len(PP)}p_{PP[0]}_1920x1080_yuv420p10le.yuv"
                    if(len(PP)==2):
                        cfg['Reconstructed_file_path'] = f"{output_PATH}/f{frame}/output/{TV}_{len(PP)}p_{PP[0]}_{PP[1]}_1920x1080_yuv420p10le.yuv"
                    if(len(PP)==3):
                        cfg['Reconstructed_file_path'] = f"{output_PATH}/f{frame}/output/{TV}_{len(PP)}p_{PP[0]}_{PP[1]}_{PP[2]}_1920x1080_yuv420p10le.yuv"
                    cfg['Original_file_path'] = f"{dataset_PATH}/{TV}_texture_{w}x{h}_yuv420p10le.yuv"
                    cfg['Video_width'] = w
                    cfg['Video_height'] = h
                    cfg['Start_frame_of_original_file'] = frame
                with open(WSPSNR_cfg,"w") as dump_f:
                    json.dump(cfg,dump_f)
                # run ws-psnr
                os.system(f"{WSPSNR_bin} {WSPSNR_cfg}")
def psnr(dataset):
    target_frames = {
        "IntelFrog": [50,100,150,200,250],
        "OrangeKitchen": [16,32,48,54,72],
        "PoznanCarpark": [40,80,120,160,200],
        "PoznanFencing": [40,80,120,160,200],
        "PoznanHall": [80,160,240,320,400],
        "PoznanStreet": [40,80,120,160,200],
        "TechnicolorPainter": [50,100,150,200,250]
    }
    target_views = {
            "OrangeKitchen":['v01','v03','v04','v05','v06','v07','v08','v09','v11','v13','v15','v16','v17','v18','v19','v20','v21','v23'],
            "TechnicolorPainter":['v1','v2','v4','v6','v7','v8','v11','v13','v14'],
            "IntelFrog":['v2','v4','v6','v8','v10','v12'],
            "PoznanFencing":['v03','v05','v09'],
            "PoznanStreet":["v3","v5"],
            "PoznanCarpark":["v3","v5"],
            "PoznanHall":["v3","v5"]
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
    dataset_PATH = f"/mnt/data1/tsehou/perspective_dataset/{dataset}"
    output_PATH = f"/home/tsehou/tmiv-3.1/tmiv_output/{dataset}"
    run_psnr(target_frames[dataset],target_views[dataset],dataset_PATH,output_PATH,resolution[dataset][0],resolution[dataset][1])

if __name__ == "__main__":
    # init.
    WSPSNR_cfg = "/home/tsehou/tmiv-3.1/tmiv/ctc_config/exp_config/multipass/WSPSNR.json"
    WSPSNR_bin = "/home/tsehou/wspsnr/ws-psnr"
    numofViewPerPass = []
    for p1 in range(1,8):
        temp = []
        temp.append(p1)
        numofViewPerPass.append(temp)
    for p1 in range(1,8):
        for p2 in range(p1+1,8):
            temp = []
            temp.append(p1)
            temp.append(p2)
            numofViewPerPass.append(temp)
    for p1 in range(1,8):
        for p2 in range(p1+1,8):
            for p3 in range(p2+1,8):
                temp = []    
                temp.append(p1)
                temp.append(p2)
                temp.append(p3)
                numofViewPerPass.append(temp)
    psnr(sys.argv[1])

