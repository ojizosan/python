def cross(A, B):
    "Aの要素とBの要素の外積。"
    return [a+b for a in A for b in B]
 
digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def parse_grid(grid):
    """テキスト形式gridを可能な値の辞書{square: digits}に変換する。ただし
    矛盾が見つかった場合にはFalseを返す。"""
    ## 最初それぞれのマスは何の数字でもありうる。それからgridより値を割り当てる。
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (マスsにdを割り当てられなければ失敗) 
    return values
 
def grid_values(grid):
    "テキスト形式gridを辞書{square: char}に変換する。空のマスは'0'か'.'とする。"
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def assign(values, s, d):
    """ values[s]からd以外のすべての値を取り除き、伝播する。
   valuesを返す。ただし矛盾が見つかった場合はFalseを返す。"""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False
 
def eliminate(values, s, d):
    """ values[s]からdを取り除く。値か場所が1つになったら伝播する。
   valuesを返す。ただし、矛盾が見つかったときにはFalseを返す。"""
    if d not in values[s]:
        return values ## すでに取り除かれている
    values[s] = values[s].replace(d,'')
    ## (1) マスs が1つの値d2まで絞られたなら、ピアからd2を取り除く。
    if len(values[s]) == 0:
	    return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) ユニットuで値dを置きうる場所が1カ所だけになったなら、dをその場所に入れる。
    for u in units[s]:
	    dplaces = [s for s in u if d in values[s]]
	if len(dplaces) == 0:
	    return False ## 矛盾 値を置ける場所がない
	elif len(dplaces) == 1:
	    # ユニットの中でdを置けるところが1カ所しかないので、そこに置く
            if not assign(values, dplaces[0], d):
                return False
    return values

def display(values):
    "valuesを2次元のテキスト形式で表示する。"
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print

def solve(grid): return search(parse_grid(grid))
 
def search(values):
    "深さ優先探索と制約伝播を使い、すべての可能なvaluesを試す。"
    if values is False:
        return False ## 前の時点で失敗している
    if all(len(values[s]) == 1 for s in squares): 
        return values ## 解けた!
    ## 取り得る値の個数が最小である未確定のマスsを選ぶ
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) 
		for d in values[s])
 
def some(seq):
    "seqの要素からtrueであるものをどれか返す。"
    for e in seq:
        if e: return e
    return False

print(solve('003020600900305001001806400008102900700000008006708200002609500800203009005010300'))