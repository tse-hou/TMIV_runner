# TMIV_script 
These scripts are used to run TMIV and process the output data.

- runTMIV.py
run TMIV encoder and decoder.
```
python3 runTMIV.py {dataset}
```
- WSPSNR.py
calculate WS-PSNR for output of decoder
```
python3 WSPSNR.py {dataset}
```
- grep_frame_***.py
extract specific frame and view from dataset
```
python3 grep_frame_***.py {dataset}
```
- get_order_table.py 
output real source view order 
```
invoke by merge_data.py
```

- merge_data.py
merge outputs from other script into one csv file 
```
python3 merge_data.py {dataset}
```