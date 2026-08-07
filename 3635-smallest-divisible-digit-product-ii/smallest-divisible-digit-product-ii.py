from collections import deque

class Solution(object):
    def smallestNumber(self, num, t):
        # 1) factor t into primes 2,3,5,7
        exps = [0,0,0,0]   # [#2s, #3s, #5s, #7s]
        for i,p in enumerate((2,3,5,7)):
            while t % p == 0:
                t //= p
                exps[i] += 1
        if t != 1:
            return "-1"    # has some other prime
        
        e2,e3,e5,e7 = exps
        
        # 2) hard‑code each digit’s (Δ2,Δ3,Δ5,Δ7)
        digit_fact = {
            1: (0,0,0,0),
            2: (1,0,0,0),
            3: (0,1,0,0),
            4: (2,0,0,0),
            5: (0,0,1,0),
            6: (1,1,0,0),
            7: (0,0,0,1),
            8: (3,0,0,0),
            9: (0,2,0,0),
        }
        
        # 3) build a dist[] via BFS over all exponent‑states up to (e2,e3,e5,e7)
        D2, D3, D5, D7 = e2+1, e3+1, e5+1, e7+1
        total = D2*D3*D5*D7
        dist = [-1]*total
        
        def idx(a,b,c,d):
            # flatten 4D → 1D
            return ((a*D3 + b)*D5 + c)*D7 + d
        
        def decode(ix):
            d = ix % D7; ix //= D7
            c = ix % D5; ix //= D5
            b = ix % D3; ix //= D3
            a = ix
            return a,b,c,d
        
        dq = deque([0])
        dist[0] = 0
        while dq:
            cur = dq.popleft()
            a,b,c,d = decode(cur)
            step = dist[cur] + 1
            for dig in range(1,10):
                da,db,dc,dd = digit_fact[dig]
                na = a+da if a+da < D2 else e2
                nb = b+db if b+db < D3 else e3
                nc = c+dc if c+dc < D5 else e5
                nd = d+dd if d+dd < D7 else e7
                ni = idx(na,nb,nc,nd)
                if dist[ni] < 0:
                    dist[ni] = step
                    dq.append(ni)
        
        # helper: build the lex‐min suffix that exactly solves deficits (a,b,c,d)
        def build_suffix(a,b,c,d):
            out = []
            rem = dist[idx(a,b,c,d)]
            for _ in range(rem):
                curd = dist[idx(a,b,c,d)]
                for dig in range(1,10):
                    da,db,dc,dd = digit_fact[dig]
                    na = max(0, a-da)
                    nb = max(0, b-db)
                    nc = max(0, c-dc)
                    nd = max(0, d-dd)
                    if dist[idx(na,nb,nc,nd)] == curd-1:
                        out.append(str(dig))
                        a,b,c,d = na,nb,nc,nd
                        break
            return "".join(out)
        
        # 4) attempt a SAME‐LENGTH DFS/backtracking search in lex order
        N = len(num)
        chosen = [0]*N
        # states[i] holds the pre‐digit state at position i
        states = [None]*(N+1)
        # initialize at depth 0
        states[0] = {
            'a': e2, 'b': e3, 'c': e5, 'd': e7,
            'prefix_equal': True,
            'next_dig': int(num[0])
        }
        i = 0
        
        while True:
            # backtracked off the front → no same‐length solution
            if i < 0:
                break
            
            # reached depth N → check if deficits are fully solved
            if i == N:
                st = states[N]
                if st['a']==0 and st['b']==0 and st['c']==0 and st['d']==0:
                    return "".join(str(d) for d in chosen)
                # else backtrack
                i -= 1
                continue
            
            st = states[i]
            a,b,c,d = st['a'], st['b'], st['c'], st['d']
            prefix_equal = st['prefix_equal']
            ndig = st['next_dig']
            
            limit = int(num[i]) if prefix_equal else 1
            placed = False
            
            for dig in range(ndig, 10):
                if dig == 0:
                    continue
                if prefix_equal and dig < limit:
                    continue
                da,db,dc,dd = digit_fact[dig]
                na = max(0, a-da)
                nb = max(0, b-db)
                nc = max(0, c-dc)
                nd = max(0, d-dd)
                need = dist[idx(na,nb,nc,nd)]
                rem  = N - i - 1
                if need <= rem:
                    # commit this digit
                    chosen[i] = dig
                    st['next_dig'] = dig + 1
                    new_eq = prefix_equal and (dig == limit)
                    next_ndig = (int(num[i+1]) if new_eq and i+1 < N else 1)
                    states[i+1] = {
                        'a': na, 'b': nb, 'c': nc, 'd': nd,
                        'prefix_equal': new_eq,
                        'next_dig': next_ndig
                    }
                    i += 1
                    placed = True
                    break
            
            if not placed:
                # backtrack
                i -= 1
        
        # 5) no same‐length: build the shortest possible longer L
        need_full = dist[idx(e2,e3,e5,e7)]
        L = max(N+1, need_full)
        # pad with ‘1’s then exact suffix
        return "1"*(L-need_full) + build_suffix(e2,e3,e5,e7)