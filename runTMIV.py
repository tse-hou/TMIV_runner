import json
import sys
import csv
import os
import time
# usage:
# python3 runTMIV.py dataset
# 
dataset = sys.argv[1]
# init. parameter
Encoder_PATH = "/home/tsehou/tmiv-3.1/tmiv/install.gcc/bin/Encoder"
Decoder_PATH = "/home/tsehou/tmiv-3.1/tmiv/install.gcc/bin/Decoder"
target_frames = {
    "IntelFrog": [50,100,150,200,250],
    "OrangeKitchen": [16,32,48,54,72],
    "PoznanCarpark": [40,80,120,160,200],
    "PoznanFencing": [40,80,120,160,200],
    "PoznanHall": [80,160,240,320,400],
    "PoznanStreet": [40,80,120,160,200],
    "TechnicolorPainter": [50,100,150,200,250]
}
target_view = {
        "OrangeKitchen":['v01','v03','v04','v05','v06','v07','v08','v09','v11','v13','v15','v16','v17','v18','v19','v20','v21','v23'],
        "TechnicolorPainter":['v1','v2','v4','v6','v7','v8','v11','v13','v14'],
        "IntelFrog":['v2','v4','v6','v8','v10','v12'],
        "PoznanFencing":['v03','v05','v09'],
        "PoznanStreet":["v3","v5"],
        "PoznanCarpark":["v3","v5"],
        "PoznanHall":["v3","v5"]
}
TIMELOG_PATH = f"/home/tsehou/tmiv-3.1/tmiv_output/{dataset}/timelog.csv"
TMIV_CONFIG_PATH= f"/home/tsehou/tmiv-3.1/tmiv/ctc_config/exp_config/multipass/TMIV_{dataset}.json"
TMIV_DATASET_PATH= f"/mnt/data1/tsehou/perspective_dataset/{dataset}"
TMIV_OUTPUT_PATH= f"/home/tsehou/tmiv-3.1/tmiv_output/{dataset}"
HM_CONFIG_PATH = f"/home/tsehou/tmiv-3.1/tmiv/ctc_config/exp_config/multipass/TMIV_{dataset}_HM.cfg"


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

with open(TIMELOG_PATH,'a') as log:
    log.write("Type, frame, target view, numofPass, numofViewPerPass, time\n")
#

for TF in target_frames:
    # Encoder
    # modify cfg
    with open(TMIV_CONFIG_PATH,'r') as load_f:
        cfg = json.load(load_f)
        cfg['startFrame'] = TF
    with open(TMIV_CONFIG_PATH,"w") as dump_f:
        json.dump(cfg,dump_f)
    
    # run encoder
    os.system(f"mkdir {TMIV_OUTPUT_PATH}/f{TF}")
    os.system(f"mkdir {TMIV_OUTPUT_PATH}/f{TF}/raw_output")
    os.system(f"mkdir {TMIV_OUTPUT_PATH}/f{TF}/output")
    time_start = time.time()
    os.system(f"{Encoder_PATH} -c {TMIV_CONFIG_PATH} \
 		                    -p SourceDirectory {TMIV_DATASET_PATH} \
 		                    -p OutputDirectory {TMIV_OUTPUT_PATH}/f{TF}/raw_output")
    time_end = time.time()
    totalTime = time_end - time_start
    # log
    with open(TIMELOG_PATH,'a') as log:
        log.write(f"Encoder, {TF}, X, X, X, {totalTime}\n")
    
    # HEVC reconstruction
    os.system(f"mv {TMIV_OUTPUT_PATH}/f{TF}/raw_output/*.bit {TMIV_OUTPUT_PATH}/f{TF}/output")
    all_output = os.listdir(f"{TMIV_OUTPUT_PATH}/f{TF}/raw_output")    
    for output in all_output:
        os.system(f"TAppEncoderStatic -c {HM_CONFIG_PATH} \
                                    -b {TMIV_OUTPUT_PATH}/f{TF}/output/bitstream \
                                    -i {TMIV_OUTPUT_PATH}/f{TF}/raw_output/{output} \
                                    -o {TMIV_OUTPUT_PATH}/f{TF}/output/{output}")

    # Decoder
    for TV in target_views:
        for PP in numofViewPerPass:
            # modify cfg
            with open(TMIV_CONFIG_PATH,'r') as load_f:
                cfg = json.load(load_f)
                cfg['Decoder']['MultipassRenderer']['NumberOfPasses'] = len(PP)
                cfg['Decoder']['MultipassRenderer']['NumberOfViewsPerPass'] = PP
                cfg['OutputCameraName'] = TV
                if(len(PP)==1):
                    cfg['OutputTexturePath'] = f"{TV}_{len(PP)}p_{PP[0]}_1920x1080_yuv420p10le.yuv"
                if(len(PP)==2):
                    cfg['OutputTexturePath'] = f"{TV}_{len(PP)}p_{PP[0]}_{PP[1]}_1920x1080_yuv420p10le.yuv"
                if(len(PP)==3):
                    cfg['OutputTexturePath'] = f"{TV}_{len(PP)}p_{PP[0]}_{PP[1]}_{PP[2]}_1920x1080_yuv420p10le.yuv"
            with open(TMIV_CONFIG_PATH,"w") as dump_f:
                json.dump(cfg,dump_f)
            # run decoder
            time_start = time.time()
            os.system(f"{Decoder_PATH} -c {TMIV_CONFIG_PATH} \
                                    -p SourceDirectory {TMIV_DATASET_PATH} \
                                    -p OutputDirectory {TMIV_OUTPUT_PATH}/f{TF}/output")
            time_end = time.time()
            totalTime = time_end - time_start
            # log
            with open(TIMELOG_PATH,'a') as log:
                log.write(f"Decoder, {TF}, {TV}, {len(PP)}, {PP}, {totalTime}\n")


