import os
import argparse
import sys
import config_unit as cu
sentence= "Write in 2020 Feb. 28.\nThis script run Encoder ,HM & Decoder of TMIV."
parser = argparse.ArgumentParser(description=sentence)
parser.add_argument('--TMIV', '-T', type=str, required=True,                \
                    help='cfg. address of TMIV', dest='TMIV_cfg')
parser.add_argument('--HM', '-H', type=str, required=True,                  \
                    help='cfg. address of HM', dest='HM_cfg')
parser.add_argument('--PSNR', '-P', type=str, required=True,                \
                    help='cfg. address of TMIV', dest='PSNR_cfg')
parser.add_argument('--PoseTraceSource', '-PTS', type=str, required=True,   \
                    help='address of PoseTraceSource', dest='PTS')
parser.add_argument('--PoseTraceName', '-PTN', type=str, required=True,     \
                    help='address of PoseTraceName', dest='PTN')
parser.add_argument('--dataset_folder', '-DF', type=str, required=True,     \
                    help='address of dataset folder', dest='DF')
parser.add_argument('--output_folder', '-OF', type=str, required=True,      \
                    help='address of output folder', dest='OF')
parser.add_argument('--GT_folder', '-GTF', type=str, required=True,         \
                    help='address of ground truth folder', dest='GTF')  
parser.add_argument('--dataset', '-D', type=str, required=True,         \
                    help='dataset want to run (option:0(all), 1(C), 2(M), 3(H))', dest='D')
parser.add_argument('--numofpose', '-NoP', type=str, required=True,         \
                    help='total number of pose', dest='NoP')

args = parser.parse_args()

cfg_address_TMIV = args.TMIV_cfg
cfg_address_HM = args.HM_cfg
cfg_address_PSNR = args.PSNR_cfg
PoseTraceSource = args.PTS
PoseTraceName = args.PTN
dataset_folder = args.DF
output_folder = args.OF
GT_folder = args.GTF
NoP = int(args.NoP)
datasets = []
if(args.D == '0'):
    datasets = ["ClassroomVideo", "TechnicolorMuseum", "TechnicolorHijack"]
elif(args.D == '1'):
    datasets = ["ClassroomVideo"]
elif(args.D == '2'):
    datasets = ["TechnicolorMuseum"]
elif(args.D == '3'):
    datasets = ["TechnicolorHijack"]
else:
    sys.exit("--dataset/-D have wrong input")

# (datasets -> frames -> poses)
for dataset in datasets:
    os.system("mkdir "+ "/".join((output_folder, dataset)))
    os.system("mkdir h265/"+dataset)
    # 
    for num_frame in range(1,6):
        file_folder = "/".join((output_folder, dataset, str(num_frame)+"_frame"))
        os.system("mkdir "+ file_folder)
        # Run Encoder
        cu.config_TMIV_ram(cfg_address_TMIV,   \
                        dataset,            \
                        dataset_folder,     \
                        file_folder,        \
                        num_frame,          \
                        PoseTraceName,      \
                        1,                  \
                        [1])
        os.system("Encoder -c " + cfg_address_TMIV)
        # 
        # h.265
        os.system("mkdir " + "/".join((file_folder, "h265")))
        for t in range(10):
            cu.config_HM(cfg_address_HM, file_folder, dataset, t, "T")
            os.system("~/HM/bin/TAppEncoderStatic -c " + cfg_address_HM)
        for d in range(10):
            cu.config_HM(cfg_address_HM, file_folder, dataset, d, "D")
            os.system("~/HM/bin/TAppEncoderStatic -c " + cfg_address_HM)
        # 
        # copy .bit file
        os.system("cp "+                                                \
                  "/".join((file_folder, "ATL_R0_Tm_c00.bit"))+" "+     \
                  "/".join((file_folder, "h265", "ATL_R0_Tm_c00.bit")))
        # 
        for num_pose in range(1,NoP+1):
            # extract pose from PoseTraceSource
            cu.pose_parser(PoseTraceSource, PoseTraceName, num_pose, dataset, dataset_folder)
            # 
            # Run Decoder pass #1
            for p1 in range(1,8):
                cu.config_TMIV_ram(cfg_address_TMIV,   \
                                dataset,            \
                                dataset_folder,     \
                                file_folder,        \
                                num_frame,          \
                                PoseTraceName,      \
                                num_pose,           \
                                [p1])
                os.system("Decoder -c " + cfg_address_TMIV)
            # 
            # Run Decoder pass #2
            for p1 in range(1,8):
                for p2 in range(p1+1,8):
                    cu.config_TMIV_ram(cfg_address_TMIV,    \
                                    dataset,            \
                                    dataset_folder,     \
                                    file_folder,        \
                                    num_frame,          \
                                    PoseTraceName,      \
                                    num_pose,           \
                                    [p1, p2])
                    os.system("Decoder -c " + cfg_address_TMIV) 
            # 
            # Run Decoder pass #3
            for p1 in range(1,8):
                for p2 in range(p1+1,8):
                    for p3 in range(p2+1,8):
                        cu.config_TMIV_ram(cfg_address_TMIV,   \
                                        dataset,            \
                                        dataset_folder,     \
                                        file_folder,        \
                                        num_frame,          \
                                        PoseTraceName,      \
                                        num_pose,           \
                                        [p1, p2, p3])
                        os.system("Decoder -c " + cfg_address_TMIV) 
            # 

