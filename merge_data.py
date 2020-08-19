import csv
import sys
from get_order_table import get_order_table as GOT
# this script merge outputs from other script into one csv file 
# usage:
# python3 merge_data.py {dataset}
# 
dataset = sys.argv[1]

psnr = []
with open(f'/home/tsehou/tmiv-3.1/tmiv/script/PSNR/{dataset}_PSNR.csv',newline='') as csvfile:
    psnrlog = csv.reader(csvfile)
    for row in psnrlog:
        psnr.append(row[0])

title = ["","Dataset","Frame","Synthesized View","X.passes","WS.PSNR","CEL","theo_time","p1","p2","p3","V1","V2","V3","V4","V5","V6","V7"]
with open(f'/home/tsehou/tmiv-3.1/tmiv_output/{dataset}/timelog.csv', newline = '') as csvfile:
    timelog = csv.reader(csvfile)
    with open(f'/home/tsehou/tmiv-3.1/tmiv/script/TMIV_dataset/{dataset}_perspective.csv','w',newline = '') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(title)
        idx = 1
        for row in timelog:
            output_row = []
            if(row[0] == 'Type' or row[0] == 'Encoder'):
                continue
            # idx
            output_row.append(idx)
            # dataset
            output_row.append(f'{dataset}')
            # frame            
            output_row.append(row[1])
            # Synthesized View
            output_row.append(row[2])
            # X.passes
            output_row.append(row[3])
            # WS.PSNR
            output_row.append(psnr[idx])
            # CEL
            output_row.append((float(psnr[idx])-20)/float(row[7]))
            # theo_time
            output_row.append(row[7])
            # num of View Per Pass
            output_row.append(row[4])
            output_row.append(row[5])
            output_row.append(row[6])
            # view order
            ordertable = GOT()
            output_row.append(ordertable[f'{dataset}{row[2]}'][0])
            output_row.append(ordertable[f'{dataset}{row[2]}'][1])
            output_row.append(ordertable[f'{dataset}{row[2]}'][2])
            output_row.append(ordertable[f'{dataset}{row[2]}'][3])
            output_row.append(ordertable[f'{dataset}{row[2]}'][4])
            output_row.append(ordertable[f'{dataset}{row[2]}'][5])
            output_row.append(ordertable[f'{dataset}{row[2]}'][6])
            # write in .csv
            writer.writerow(output_row)
            idx+=1


    
