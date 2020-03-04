import os

os.system("python Runner_TMIV_ram.py    --TMIV              /home/tsehou/tmiv/ctc_config/TMIV_exp/TMIV_MP.json\
                                        --HM                /home/tsehou/tmiv/TMIV_runner/HM.cfg\
                                        --PSNR              /home/tsehou/wspsnr/config_files/Full_ERP.json\
                                        --PoseTraceSource   /home/tsehou/ClassroomVideo/moredata.csv\
                                        --PoseTraceName     temp.csv\
                                        --dataset_folder    /home/tsehou\
                                        --output_folder     /home/tsehou/tmiv/output/moredata\
                                        --GT_folder         X\
                                        --dataset           1\
                                        --numofpose         3\
                                        ")