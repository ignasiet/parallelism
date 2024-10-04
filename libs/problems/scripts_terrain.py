added=set()
def create_predicates(pos: str,
                      size: int,
                      pred_name: str):
    coordinates = pos[pos.find('_')+1:]
    x = int(coordinates.split('_')[0])
    y = int(coordinates.split('_')[1])

    ops = [-1,0,1]
    for i in ops:
        if x+i >=1 and x+i<=size:
            for j in ops:
                if y+j >=1 and y+j<=size:
                    if i==0 and j==0:
                        continue
                    added.add(pred_name+'_' + str(x+i) + '_' + str(y+j))
                    # print(pred_name+'_' + str(x+i) + '_' + str(y+j))

def create_map(size: int,
               predicate: str,
               obstacles: list):
    valid_pos = []
    adjacencies = {}
    for i in range(1, size):
        for j in range(1, size):
            if f'{i}_{j}' not in obstacles:
                obj = f'{predicate}_{i}_{j}'
                valid_pos.append(f'pos_{i}_{j}')
                # print(f"- {obj}")
    for i in range(1, size):
        for j in range(1, size):
            if f'pos_{i}_{j}' not in valid_pos:
                continue
            if i+1<=size and f"pos_{i+1}_{j}" in valid_pos:
                adjacencies[f'adjacent_pos_{i}_{j}_pos_{i+1}_{j}']=1
            if 1<=i-1 and f"pos_{i-1}_{j}" in valid_pos:
                adjacencies[f'adjacent_pos_{i}_{j}_pos_{i-1}_{j}']=1
            if j+1<=size and f"pos_{i}_{j+1}" in valid_pos:
                adjacencies[f'adjacent_pos_{i}_{j}_pos_{i}_{j+1}']=1
            if 1<=j-1 and f"pos_{i}_{j-1}" in valid_pos:
                adjacencies[f'adjacent_pos_{i}_{j}_pos_{i}_{j-1}']=1
    for k,v in adjacencies.items():
        print(f"- {k}")


if __name__ == "__main__":
    # create_predicates('pos_2_2', 4, 'covered')
    # create_predicates('pos_3_4', 4, 'covered')
    # for item in added:
    #     print(f"- {item}")
    create_map(11,
        'pos',
        ['1_2','1_3','1_4','1_5','1_6','1_7','2_9',
        '3_2','3_3','3_4','3_9',
        '4_9','5_6','5_9',
        '6_3','6_4','6_5','6_6',
        '7_6','7_9','8_9',
        '9_3','9_4','9_5','9_6','9_8','9_9',
        '11_4','11_5','11_6'])
