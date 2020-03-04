import config_unit as cu
import os

cfg_address = "/home/tsehou/wspsnr/config_files/Full_ERP.json"
GT_folder = "/mnt/data/tsehou/TMIV_output/TD_GT"
RE_folder = "/home/tsehou/tmiv/output/exp_testingdata"
datasets = ["ClassroomVideo","TechnicolorMuseum","TechnicolorHijack"]

for dataset in datasets:
    for num_Frame in range(1,6):
        for num_pose in range(1,6):
            for i in range(1,8):
                cu.config_PSNR_ram(cfg_address, dataset, GT_folder, RE_folder, num_Frame, num_pose, [i])
                os.system('/home/tsehou/wspsnr/ws-psnr /home/tsehou/wspsnr/config_files/Full_ERP.json' )
            for i in range(1,8):
                for j in range(i+1,8):
                    cu.config_PSNR_ram(cfg_address, dataset, GT_folder, RE_folder, num_Frame, num_pose, [i,j])
                    os.system('/home/tsehou/wspsnr/ws-psnr /home/tsehou/wspsnr/config_files/Full_ERP.json' )
            for i in range(1,8):
                for j in range(i+1,8):
                    for k in range(j+1,8):
                        cu.config_PSNR_ram(cfg_address, dataset, GT_folder, RE_folder, num_Frame, num_pose, [i,j])
                        os.system('/home/tsehou/wspsnr/ws-psnr /home/tsehou/wspsnr/config_files/Full_ERP.json' )
