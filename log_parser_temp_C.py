import csv
log_address="PSNR_C.log"
output="TechnicolorHijack_ran_no.csv"
# open log file
cfg = open(log_address,"r")
lines = cfg.readlines()
cfg.close()
# 
list_dataset=[]
list_frame=[]
list_view=[]
list_pass=[]
list_RunningTime=[]
list_PSNR=[]
list_CEL=[]
list_p1=[]
list_p2=[]
list_p3=[]
# Colunm name
list_csv=[  ["",
            'Dataset',
            'Frame',
            'Synthesized View',
            'X.passes',
            'WS.PSNR',
            'CEL',
            'theo_time',
            'p1',
            'p2',
            'p3']]
# 
# Process data
# dataset
# for i in range(25*63):
#     list_dataset.append("ClassroomVideo")
# for i in range(25*63):
    # list_dataset.append("TechnicolorMuseum")
for i in range(25*63):
    list_dataset.append("TechnicolorHijack")
# frame
# for i in [20,40,60,80,100]:
#     for j in range(5*63):
#         list_frame.append(i)
for i in [50,100,150,200,250]:
    for j in range(5*63):
        list_frame.append(i)
# for i in [50,100,150,200,250]:
#     for j in range(5*63):
#         list_frame.append(i)
# view
# for d in range(3):
for f in range(5):
    for i in range(1,6):
        for j in range(63):
            list_view.append(i)
# pass
for n in range(25):
    for i in range(7):
        list_pass.append(1)
    for i in range(21):
        list_pass.append(2)
    for i in range(35):
        list_pass.append(3)
# PSNR
for i in (range(len(lines))):
    if(lines[i][0:7]=="Frame:0"):
        list_PSNR.append(float(lines[i][9:16]))
# Running time
Theo_T_M=[17.128,20.394,74.244,102.824,116.523,159.902,159.423]
Theo_T_H=[52.831,274.456,278.205,289.202,333.302,517.57,518.947]
Theo_T_C=[134.975,142.678,143.185,143.392,144.997,146.603,151.553]
# for n in range(25):
#     for i in range(7):
#         list_RunningTime.append(Theo_T_C[i])
#     for i in range(7):
#         for j in range(i+1,7):
#         list_RunningTime.append(Theo_T_C[j])    
#     for i in range(7):
#         for j in range(i+1,7):
#             for k in range(j+1,7):
#             list_RunningTime.append(Theo_T_C[k])
# for n in range(25):
#     for i in range(7):
#         list_RunningTime.append(Theo_T_M[i])
#     for i in range(7):
#         for j in range(i+1,7):
#             list_RunningTime.append(Theo_T_M[j])    
#     for i in range(7):
#         for j in range(i+1,7):
#             for k in range(j+1,7):
#                 list_RunningTime.append(Theo_T_M[k])
for n in range(25):
    for i in range(7):
        list_RunningTime.append(Theo_T_H[i])
    for i in range(7):
        for j in range(i+1,7):
            list_RunningTime.append(Theo_T_H[j])    
    for i in range(7):
        for j in range(i+1,7):
            for k in range(j+1,7):
                list_RunningTime.append(Theo_T_H[k])
# 
# CEL
# for n in range(25*63*3):
for n in range(25*63*1):
    list_CEL.append((list_PSNR[n]-20)/list_RunningTime[n])
# 
# for n in range(3*25):
for n in range(1*25):
    for i in range(1,8):
        list_p1.append(i)
        list_p2.append(0)
        list_p3.append(0)
    for i in range(1,8):
        for j in range(i+1,8):
            list_p1.append(i)
            list_p2.append(j)
            list_p3.append(0)
    for i in range(1,8):
        for j in range(i+1,8):
            for k in range(j+1,8):
                list_p1.append(i)
                list_p2.append(j)
                list_p3.append(k)
# 
for n in range(len(list_dataset)):
    list_csv.append([n+1,
                    list_dataset[n],
                    list_frame[n],
                    list_view[n],
                    list_pass[n],
                    list_PSNR[n],
                    list_CEL[n],
                    list_RunningTime[n],
                    list_p1[n],
                    list_p2[n],
                    list_p3[n]
                    ])
with open(output,'w') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(list_csv)):
        writer.writerow(list_csv[i])
# 
print("csv output done")