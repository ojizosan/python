def cross(A, B):
    return [A[a] + B[b] for a in range(len(A)) for b in range(len(B))]

cols      = [str(1 + i) for i in range(25)]
rows      = [str(a) for a in 'ABCDEFGHIJKLMNOPQRSTUVWXY']
squares   = cross(rows, cols)
rowunits = [[r + c for c in cols] for r in rows]
colunits = [[r + c for r in rows] for c in cols]
squareunits = [cross(rs, cs) for rs in [rows[a:a+5] for a in range(5)]  for cs in [cols[0:5], cols[5:10], cols[10:15], cols[15:20], cols[20:25]]]
unitlists = rowunits + colunits + squareunits
'''print(rowunits)
print('\n'*3)
print(colunits)
print('\n'*3)
print(squareunits)
print('\n'*3)
print(unitlists)'''
units = dict([[s, [u for u in unitlists if s in u]] for s in squares])
peers = dict((s, list(set(sum(units[s],[]))-set([s]))) for s in squares)
#print(unit)
#print(peers)

'''grid = ''
for k in range(len(numbers)/2):
    if numbers[k*2:k*2 + 2] == '00':
        grid = grid + 'Z'
    else:
        grid = grid + rows[int(numbers[k*2:k*2 + 2])]

values = dict([[s, 'ABCDEFGHIJKLMNOPQRSTUVWXY'] for s in squares])

ccl = [str(c) for c in grid]

shokivalues = dict(list(zip(squares, ccl)))

print(shokivalues)'''

def parse_grid(grid):
    """テキスト形式gridを可能な値の辞書{square: digits}に変換する。ただし
    矛盾が見つかった場合にはFalseを返す。"""
    ## 最初それぞれのマスは何の数字でもありうる。それからgridより値を割り当てる。
    values = dict((s, [str(e+1) for e in range(25)]) for s in squares)
    for s, d in grid_values(grid).items():
        if d != '0':
            if not assign(values, s, d):
                return False ## (マスsにdを割り当てられなければ失敗) 
    print(grid_values(grid).items())
    return values
 
def grid_values(grid):
    "テキスト形式gridを辞書{square: char}に変換する。空のマスは'0'か'.'とする。"
    chars = [str(int(grid[c*2:c*2+2])) for c in range(625)]
    assert len(chars) == 625
    return dict(zip(squares, chars))


def assign(values, s, d):
    """ values[s]からd以外のすべての値を取り除き、伝播する。
   valuesを返す。ただし矛盾が見つかった場合はFalseを返す。"""
    other_values = list(set(cols) - set([d]))
    for d2 in other_values:
        eliminate(values, s, d2)
    #if all(eliminate(values, s, d2) for d2 in other_values)
    #print(other_values)
    return values
 
def eliminate(values, s, d):
    """ values[s]からdを取り除く。値か場所が1つになったら伝播する。
   valuesを返す。ただし、矛盾が見つかったときにはFalseを返す。"""
    '''if d not in values[s]:
        return values ## すでに取り除かれている'''
    values[s] = list(set(values[s]) - set([d]))
    #print(values[s])
    ## (1) マスs が1つの値d2まで絞られたなら、ピアからd2を取り除く。
    length = 0
    for x in values[s]:
        length += 1
    if length == 1:
        d2 = values[s]
        for s2 in peers[s]:
            eliminate(values, s2, d2)
        #if not all(eliminate(values, s2, d2) for s2 in peers[s]):
         #   return False
    ## (2) ユニットuで値dを置きうる場所が1カ所だけになったなら、dをその場所に入れる。
    for u in units[s]:
	    dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 1:
	    # ユニットの中でdを置けるところが1カ所しかないので、そこに置く
        if not assign(values, dplaces[0], d):
            return False
    return values

print(parse_grid('00000000000000001924200000160518000021101200000000002400000000112504000023150600001720080000130115000001000804060500000224220000212519000015031400000000100600000000182014000025150300002307220000020000220005000015010900000207180000122416000000002100002300122400000000130818000007040300000000250017000018020010000009041400000821010000000019002200050300001900202200000000211602000000001500050001040013000013080021000002071700000000000001002225002300092015002500160300000000000000000000180900230011060021040024110005000000000000000000000021001720001900220625001600202200000000000000000000240300150010010000080007200024000000000000000000000025001805001200000922001200070100000000000000000000201600020008231300140002080017000000000000000000000018002125002425000319002300112100000000000000000000240500080015242100060019030001000000000000071210000016001425000005002208000600150000000011192100000000232400200000040700120010000000000615210000130116000019000211000009001000000000161225000024190200000000220400180000200000000013100400000819160000152405000003000700000400002425190000211809000002161100000000230600000000171918000022201000002315140000010224120016000016020900001215230000011314000007180600000000040000000000032116000009252400002204230000000000000000'))
