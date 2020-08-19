# output real source view order 
def get_order_table():
    # the source view order output by TMIV
    output= [
    [1,0,2,3,4,5,6],
    [1,2,0,3,4,5,6],
    [3,2,1,4,0,5,6],
    [3,4,5,2,1,6,0],
    [4,5,3,6,2,1,0],
    [6,5,4,3,2,1,0],
    [0,1,2,3,4,5,6],
    [1,4,3,0,2,5,6],
    [1,4,3,0,6,2,5],
    [0,2,1,3,5,4,6],
    [0,1,2,3,5,4,6],
    [1,3,0,2,4,5,6],
    [1,4,3,0,6,2,5],
    [4,1,3,6,5,0,2],
    [2,3,0,1,5,4,6],
    [4,3,6,1,5,2,0],
    [2,3,5,0,1,4,6],
    [2,3,5,0,1,4,6],
    [3,5,2,4,6,1,0],
    [4,6,3,5,2,1,0],
    [4,6,3,5,1,2,0],
    [2,5,3,0,6,1,4],
    [5,2,3,6,4,0,1],
    [6,5,4,3,2,1,0],
    [3,2,1,4,0,5,6],
    [4,3,5,2,6,1,0],
    [2,1,0,3,4,5,6],
    [3,4,5,2,1,0,6],
    [6,5,4,3,2,1,0],
    [3,2,1,4,0,5,6],
    [4,3,5,2,6,1,0],
    [3,2,1,4,0,5,6],
    [4,3,5,2,6,1,0],
    [2,0,1,3,4,5,6],
    [1,2,0,4,3,6,5],
    [2,0,3,5,4,1,6],
    [2,4,1,3,0,6,5],
    [1,4,2,6,3,0,5],
    [5,3,2,4,0,6,1],
    [4,6,1,3,2,5,0],
    [3,5,4,6,2,0,1],
    [4,6,3,5,2,1,0]
    ]
    # the source view Idx of each dataset 
    source_views = {
        "IntelFrog": [1,3,5,7,9,11,13],
        "OrangeKitchen": [0,2,10,12,14,22,24],
        "PoznanCarpark": [0,1,2,4,6,7,8],
        "PoznanFencing": [0,1,2,4,6,7,8],
        "PoznanHall": [0,1,2,4,6,7,8],
        "PoznanStreet": [0,1,2,4,6,7,8],
        "TechnicolorPainter": [0,3,5,9,10,12,15]
    }
    # the target view Idx of each dataset 
    target_view = {
        "OrangeKitchen":['v01','v03','v04','v05','v06','v07','v08','v09','v11','v13','v15','v16','v17','v18','v19','v20','v21','v23'],
        "TechnicolorPainter":['v1','v2','v4','v6','v7','v8','v11','v13','v14'],
        "IntelFrog":['v2','v4','v6','v8','v10','v12'],
        "PoznanFencing":['v03','v05','v09'],
        "PoznanStreet":["v3","v5"],
        "PoznanCarpark":["v3","v5"],
        "PoznanHall":["v3","v5"]
    }

    idx = 0
    order = []
    dataset_list = []
    target_view_list = []
    for dataset in ["IntelFrog","OrangeKitchen","PoznanCarpark","PoznanFencing","PoznanHall","PoznanStreet","TechnicolorPainter"]:
        for i in range(len(target_view[dataset])):
            dataset_list.append(dataset)
            target_view_list.append(target_view[dataset][i])
            temp = []
            for j in output[idx]:
                temp.append(source_views[dataset][j])
            order.append(temp)
            idx+=1

    print(len(order))
    print(len(dataset_list))
    print(len(target_view_list))


    # dataset_list,target_view,order
    table = {}
    for i in range(42):
        table[f'{dataset_list[i]} {target_view_list[i]}'] = order[i]
    return table

