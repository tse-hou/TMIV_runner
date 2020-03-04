import json
import sys
import csv
# This function produce the .csv file of ad-hoc posetrace.
def pose_parser(PoseTraceSource, PoseTraceName, num_pose, dataset, dataset_folder):
    Allpose = []
    input_address = PoseTraceSource
    output_address = "/".join((dataset_folder,dataset,PoseTraceName))
    with open(input_address,'r') as csvfile:
        rows = csv.reader(csvfile,delimiter=',')
        for row in rows:
            Allpose.append(row)

    pose = []
    pose.append(Allpose[0])
    pose.append(Allpose[num_pose])

    with open(output_address,'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(pose)):
            writer.writerow(pose[i])
    
# This function modify the parameters in configuration file of TMIV.
def config_TMIV_ram(cfg_address, dataset, dataset_folder, file_folder, num_frame, PoseTraceName, num_pose, NumberOfViewsPerPass):
    # loda the setting according to dataset
    # Classroom
    if (dataset == "ClassroomVideo"):
        list_frame = [20,40,60,80,100]
        # 
        AtlasDepthPathFmt = "ATL_SA_R0_Td_c%02d_4096x3072_yuv420p10le.yuv"
        AtlasMetadataPath = "ATL_R0_Tm_c00.bit"
        AtlasTexturePathFmt = "ATL_SA_R0_Tt_c%02d_4096x3072_yuv420p10le.yuv"
        AtlasResolution = [4096,3072]
        MaxLumaSamplesPerFrame = 25165824
        SourceCameraParameters = "ClassroomVideo.json"
        SourceDepthPathFmt= "%s_depth_4096x2048_yuv420p16le.yuv"
        SourceTexturePathFmt= "%s_texture_4096x2048_yuv420p10le.yuv"
        OmafV1CompatibleFlag= True
        # 
        OutputTexturePath= str(num_pose)+"pose_"+str(len(NumberOfViewsPerPass))+"p_"
        for i in range(len(NumberOfViewsPerPass)):
            OutputTexturePath=OutputTexturePath+str(NumberOfViewsPerPass[i])+"_"
        OutputTexturePath= OutputTexturePath + "4096x2048_yuv420p10le.yuv"
        # 
        SourceDirectory = "/".join((dataset_folder,dataset))
        OutputDirectory = file_folder
        startFrame = list_frame[num_frame-1]
        SourceCameraNames = ["v0", "v7", "v8", "v10", "v11", "v12", "v13"]
        PoseTracePath = PoseTraceName
    # Museum
    elif (dataset == "TechnicolorMuseum"):
        list_frame = [50,100,150,200,250]
        # 
        AtlasDepthPathFmt = "ATL_SB_R0_Td_c%02d_2048x2368_yuv420p10le.yuv"
        AtlasMetadataPath = "ATL_R0_Tm_c00.bit"
        AtlasTexturePathFmt = "ATL_SB_R0_Tt_c%02d_2048x2368_yuv420p10le.yuv"
        AtlasResolution = [2048,2368]
        MaxLumaSamplesPerFrame = 29097984
        SourceCameraParameters = "TechnicolorMuseum.json"
        SourceDepthPathFmt= "%s_depth_2048x2048_yuv420p16le.yuv"
        SourceTexturePathFmt= "%s_texture_2048x2048_yuv420p10le.yuv"
        OmafV1CompatibleFlag= False
        # 
        OutputTexturePath= str(num_pose)+"pose_"+str(len(NumberOfViewsPerPass))+"p_"
        for i in range(len(NumberOfViewsPerPass)):
            OutputTexturePath=OutputTexturePath+str(NumberOfViewsPerPass[i])+"_"
        OutputTexturePath= OutputTexturePath + "2048x2048_yuv420p10le.yuv"
        # 
        SourceDirectory = "/".join((dataset_folder,dataset))
        OutputDirectory = "/".join((output_folder,dataset,str(num_frame)+"_frame"))
        startFrame = list_frame[num_frame-1]
        SourceCameraNames = ["v0","v1","v4","v11","v12","v13","v17"]
        PoseTracePath = PoseTraceName
    # Hijack
    elif (dataset == "TechnicolorHijack"):
        list_frame = [50,100,150,200,250]
        # 
        AtlasDepthPathFmt = "ATL_SC_R0_Td_c%02d_4096x5120_yuv420p10le.yuv"
        AtlasMetadataPath = "ATL_R0_Tm_c00.bit"
        AtlasTexturePathFmt = "ATL_SC_R0_Tt_c%02d_4096x5120_yuv420p10le.yuv"
        AtlasResolution = [4096,5120]
        MaxLumaSamplesPerFrame = 83886080
        SourceCameraParameters = "TechnicolorHijack.json"
        SourceDepthPathFmt= "%s_depth_4096x4096_yuv420p16le.yuv"
        SourceTexturePathFmt= "%s_texture_4096x4096_yuv420p10le.yuv"
        OmafV1CompatibleFlag= True
        # 
        OutputTexturePath= str(num_pose)+"pose_"+str(len(NumberOfViewsPerPass))+"p_"
        for i in range(len(NumberOfViewsPerPass)):
            OutputTexturePath=OutputTexturePath+str(NumberOfViewsPerPass[i])+"_"
        OutputTexturePath= OutputTexturePath + "4096x4096_yuv420p10le.yuv"
        # 
        SourceDirectory = "/".join((dataset_folder,dataset))
        OutputDirectory = "/".join((output_folder,dataset,str(num_frame)+"_frame"))
        startFrame = list_frame[num_frame-1]
        SourceCameraNames = ["v1","v2","v3","v4","v5","v8","v9"]
        PoseTracePath = PoseTraceName
    # 
    # load setting in json file
    with open(cfg_address,'r') as load_f:
        load_dict = json.load(load_f)
        load_dict['Decoder']['MultipassRenderer']['NumberOfPasses'] = len(NumberOfViewsPerPass)
        load_dict['Decoder']['MultipassRenderer']['NumberOfViewsPerPass'] = NumberOfViewsPerPass
        load_dict['AtlasDepthPathFmt'] = AtlasDepthPathFmt
        load_dict['AtlasMetadataPath'] = AtlasMetadataPath
        load_dict['AtlasTexturePathFmt'] = AtlasTexturePathFmt
        load_dict['GroupBasedEncoder']['AtlasConstructor']['AtlasResolution'] = AtlasResolution
        load_dict['GroupBasedEncoder']['AtlasConstructor']['MaxLumaSamplesPerFrame'] = MaxLumaSamplesPerFrame
        load_dict['OutputTexturePath'] = OutputTexturePath
        load_dict['startFrame'] = startFrame
        load_dict['SourceCameraNames'] = SourceCameraNames
        load_dict['SourceCameraParameters'] = SourceCameraParameters
        load_dict['SourceDepthPathFmt'] = SourceDepthPathFmt
        load_dict['SourceTexturePathFmt'] = SourceTexturePathFmt
        load_dict['OmafV1CompatibleFlag'] = OmafV1CompatibleFlag
        load_dict['PoseTracePath'] = PoseTracePath
        load_dict['SourceDirectory'] = SourceDirectory
        load_dict['OutputDirectory'] = OutputDirectory

        
        print("conf. address: "+cfg_address)
        print("dataset: " +dataset)
        print("NumberOfViewsPerPass:")
        print(NumberOfViewsPerPass)
        print("Frame:")
        print(startFrame)
        print("Decoder output file name:")
        print(OutputTexturePath)
    #save json file
    with open(cfg_address,"w") as dump_f:
        json.dump(load_dict,dump_f)

# This function modify the parameters in configuration file of HM.
def config_HM(cfg_address, file_folder, dataset, numYUV, mode):
    # load Template of cfg 
    cfg = open(cfg_address,"r")
    lines = cfg.readlines()
    cfg.close()
    numYUV=str(numYUV)
    # 
    if (mode == "T"):
        if (dataset == "ClassroomVideo"):
            lines[0]= "InputFile: "+file_folder+"/ATL_SA_R0_Tt_c0"+numYUV+"_4096x3072_yuv420p10le.yuv\n"
            lines[1]= "BitstreamFile: ./h265/bitstream_T"+numYUV+"\n"
            lines[2]= "ReconFile: "+file_folder+"/h265/ATL_SA_R0_Tt_c0"+numYUV+"_4096x3072_yuv420p10le.yuv\n" 
            lines[3]= "SourceWidth: 4096\n"
            lines[4]= "SourceHeight: 3072\n"
        elif (dataset == "TechnicolorMuseum"):
            lines[0]= "InputFile: "+file_folder+"/ATL_SB_R0_Tt_c0"+numYUV+"_2048x2368_yuv420p10le.yuv\n"
            lines[1]= "BitstreamFile: ./h265/bitstream_T"+numYUV+"\n"
            lines[2]= "ReconFile: "+file_folder+"/h265/ATL_SB_R0_Tt_c0"+numYUV+"_2048x2368_yuv420p10le.yuv\n"   
            lines[3]= "SourceWidth: 2048\n"
            lines[4]= "SourceHeight: 2368\n"
        elif (dataset == "TechnicolorHijack"):
            lines[0]= "InputFile: "+file_folder+"/ATL_SC_R0_Tt_c0"+numYUV+"_4096x5120_yuv420p10le.yuv\n"
            lines[1]= "BitstreamFile: ./h265/bitstream_T"+numYUV+"\n"
            lines[2]= "ReconFile: "+file_folder+"/h265/ATL_SC_R0_Tt_c0"+numYUV+"_4096x5120_yuv420p10le.yuv\n"    
            lines[3]= "SourceWidth: 4096\n"
            lines[4]= "SourceHeight: 5120\n"
    elif (mode == "D"):
        if (dataset == "ClassroomVideo"):
            lines[0]= "InputFile: "+file_folder+"/ATL_SA_R0_Td_c0"+numYUV+"_4096x3072_yuv420p10le.yuv\n"
            lines[1]= "BitstreamFile: ./h265/bitstream_T"+numYUV+"\n"
            lines[2]= "ReconFile: "+file_folder+"/h265/ATL_SA_R0_Td_c0"+numYUV+"_4096x3072_yuv420p10le.yuv\n" 
            lines[3]= "SourceWidth: 4096\n"
            lines[4]= "SourceHeight: 3072\n"
        elif (dataset == "TechnicolorMuseum"):
            lines[0]= "InputFile: "+file_folder+"/ATL_SB_R0_Td_c0"+numYUV+"_2048x2368_yuv420p10le.yuv\n"
            lines[1]= "BitstreamFile: ./h265/bitstream_T"+numYUV+"\n"
            lines[2]= "ReconFile: "+file_folder+"/h265/ATL_SB_R0_Td_c0"+numYUV+"_2048x2368_yuv420p10le.yuv\n"     
            lines[3]= "SourceWidth: 2048\n"
            lines[4]= "SourceHeight: 2368\n"
        elif (dataset == "TechnicolorHijack"):
            lines[0]= "InputFile: "+file_folder+"/ATL_SC_R0_Td_c0"+numYUV+"_4096x5120_yuv420p10le.yuv\n"
            lines[1]= "BitstreamFile: ./h265/bitstream_T"+numYUV+"\n"
            lines[2]= "ReconFile: "+file_folder+"/h265/ATL_SC_R0_Td_c0"+numYUV+"_4096x5120_yuv420p10le.yuv\n"  
            lines[3]= "SourceWidth: 4096\n"
            lines[4]= "SourceHeight: 5120\n"
    # write new cfg. to file
    cfg_n = open(cfg_address,"w")
    cfg_n.writelines(lines)
    cfg_n.close()
    print("HM setting: done")

# This function modify the parameters in configuration file of PSNR.
def config_PSNR_ram(cfg_address, dataset, GT_folder, RE_folder, num_Frame, num_pose, NumberOfViewsPerPass):
    if (dataset == "ClassroomVideo"):
        f_list = ['20','40','60','80','100']
        # Original_file_path = GT_folder+"/A"+num_pose+"_f"+f_list[num_Frame-1]+"_yuv420p10le.yuv"
        Original_file_path = "/".join((GT_folder,"A"+str(num_pose)+"_f"+f_list[num_Frame-1]+"_yuv420p10le.yuv"))
        Start_frame_of_original_file = 0
        # Reconstructed_file_path = RE_folder+"/"+dataset+"/"+str(frame)+"_frame/h265/"+pose+"pose_"+str(NumberOfPasses)+"p_"
        Reconstructed_file_path = "/".join((RE_folder,  \
                                            dataset,    \
                                            str(num_Frame)+"_frame",    \
                                            "h265",   \
                                            str(num_pose)+"pose_"+str(len(NumberOfViewsPerPass))+"p_"))
        for i in range(len(NumberOfViewsPerPass)):
            Reconstructed_file_path=Reconstructed_file_path+str(NumberOfViewsPerPass[i])+"_"
        Reconstructed_file_path= Reconstructed_file_path + "4096x2048_yuv420p10le.yuv"
        Video_width = 4096
        Video_height = 2048
        Latitude_range_of_ERP = 180
        Longitude_range_of_ERP = 360

    elif (dataset == "TechnicolorMuseum"):
        f_list = ['50','100','150','200','250']
        # Original_file_path = "/mnt/data/tsehou/TMIV_output/exp_eval/exp_GT/"+dataset+"/f"+f_list[frame-1]+"/B"+pose+"_f"+f_list[frame-1]+"_yuv420p10le.yuv"
        Original_file_path = "/".join((GT_folder,"B"+str(num_pose)+"_f"+f_list[num_Frame-1]+"_yuv420p10le.yuv"))
        Start_frame_of_original_file = 0
        # Reconstructed_file_path = "/home/tsehou/tmiv/output/exp_moredata/"+dataset+"/"+str(frame)+"_frame/h265/"+pose+"pose_"+str(NumberOfPasses)+"p_"
        Reconstructed_file_path = "/".join((RE_folder,  \
                                            dataset,    \
                                            str(num_Frame)+"_frame",    \
                                            "h265",   \
                                            str(num_pose)+"pose_"+str(len(NumberOfViewsPerPass))+"p_"))
        for i in range(len(NumberOfViewsPerPass)):
            Reconstructed_file_path=Reconstructed_file_path+str(NumberOfViewsPerPass[i])+"_"
        Reconstructed_file_path= Reconstructed_file_path + "2048x2048_yuv420p10le.yuv"    
        Video_width = 2048
        Video_height = 2048
        Latitude_range_of_ERP = 180
        Longitude_range_of_ERP = 180

    elif (dataset == "TechnicolorHijack"):
        f_list = ['50','100','150','200','250']
        # Original_file_path = "/mnt/data/tsehou/TMIV_output/exp_eval/exp_GT/"+dataset+"/f"+f_list[frame-1]+"/C"+pose+"_f"+f_list[frame-1]+"_yuv420p10le.yuv"
        Original_file_path = "/".join((GT_folder,"C"+str(num_pose)+"_f"+f_list[num_Frame-1]+"_yuv420p10le.yuv"))
        Start_frame_of_original_file = 0
        # Reconstructed_file_path = "/home/tsehou/tmiv/output/exp_moredata/"+dataset+"/"+str(frame)+"_frame/h265/"+pose+"pose_"+str(NumberOfPasses)+"p_"
        Reconstructed_file_path = "/".join((RE_folder,  \
                                            dataset,    \
                                            str(num_Frame)+"_frame",    \
                                            "h265",   \
                                            str(num_pose)+"pose_"+str(len(NumberOfViewsPerPass))+"p_"))        
        for i in range(len(NumberOfViewsPerPass)):
            Reconstructed_file_path=Reconstructed_file_path+str(NumberOfViewsPerPass[i])+"_"
        Reconstructed_file_path= Reconstructed_file_path + "4096x4096_yuv420p10le.yuv"    
        Video_width = 4096
        Video_height = 4096
        Latitude_range_of_ERP = 180
        Longitude_range_of_ERP = 180

    with open(cfg_address,'r') as load_f:
        load_dict = json.load(load_f)
        load_dict['Original_file_path'] = Original_file_path
        load_dict['Start_frame_of_original_file'] = Start_frame_of_original_file
        load_dict['Reconstructed_file_path'] = Reconstructed_file_path
        load_dict['Video_width'] = Video_width
        load_dict['Video_height'] = Video_height
        load_dict['Latitude_range_of_ERP'] = Latitude_range_of_ERP
        load_dict['Longitude_range_of_ERP'] = Longitude_range_of_ERP
        
    with open(cfg_address,"w") as dump_f:
        json.dump(load_dict,dump_f)
    print("PSNR setting: done")

# def log_parser(log_address, output):
    