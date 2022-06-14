import itertools


'''
1) M will be initialised (one possibility at the start)
2) D, D_dash will be the same throughout
3) We will loop using D and D_dash
    a) If there is no emergency, reduce all Ms by one and filter
    b) If there is an emergency, consider all possibilities in M after choosing (t+1) values in the D_dash array
4) Repeat step 3) until done gives a verdict
'''
f = -1


def status(A):
    '''
    0: Fine, no emergency
    1: Emergency, but not over
    -1: Over
    '''
 
    n = len(A)
    
    for i in range(n):
        if A[i] < i + 1:
            return -1
    
    for i in range(n):
        if A[i] == i + 1:
            return 1
    return 0

def compare(fcg1, fcg2):
    pass

def fcg(M):
    '''
    Flattened capacity graph for array M
    '''
    m = len(M)
    cap = []
    for i in range(m):
        cap.append(M[i] - (i + 1))
    # flattened capacity array
    fca = [cap[i] for i in range(m)]
    for i in range(m - 2, -1, -1):
        fca[i] = min(fca[i], fca[i + 1])
    return fca

def done(D, D_dash, M):
    '''
    -1: remove M from M_grid
    1: Win (Bugs win)
    0: Continue with M
    '''
    s1 = status(M)
    s2 = status(D)

    if s1 == -1 or s2 == -1 or (s1 == 1 and s2 == 1):
        return -1
    
    if(len(D) == 0 and len(M) == 0):
        return 1
    
    return 0

def stepM(M, n):
    for i in range(len(M)):
        M[i] -= n
        if M[i] <= 0:
            return -1
    return 1
    
def stepD(D, D_dash, n):
    for i in range(len(D)):
        D[i] -= n
        D_dash[i] += n


def emergency_till(D):
    ans = 0
    for i in range(len(D)):
        if D[i] == i + 1:
            ans = i
    return ans


# M_grid is a list of lists
# Each list is a separate possibility
M_grid = []

D = []
D_dash = []


while(len(M_grid)):
    if len(M_grid[0]):
        f = 1
        break
    s = status(D)
    if(s == 0):
        for M in M_grid:
            if len(M) != 0:
                M.pop(0)
            stepM(M, 1)
        stepD(D, D_dash, 1)
    else:
        t = emergency_till(D)
        # x <- D_dash[0, t]
        # sort these
        # D'[0] - (t + 1), D'[1] - (t + 1) + 2, D'[2] - (t + 1) + 2*2
        '''
        Algo
        1) For every M
            a) stepM(M, t+1)
            b) Create a permuation of t+1
                i) Based on it, select values from (ith element, jth turn) -> D'[i] - (t + 1) + 2*(j-1)
                ii) Enter these values in M
        5) D = D[t+1:], D_dash = D_dash[t+1:]
        6) stepD(D, D_dash, t+1)
        '''
        perm_array = [i for i in range(t + 1)]
        M_gridnew = []
        for M in M_grid:
            if stepM(M, t + 1) == 1:
                inds_list = list(itertools.permutations(perm_array))
                for inds in inds_list:
                    for i in range(len(inds)):
                        ind = inds[i]
                        # i -> column number, inds[i] -> row number
                        M.append(D_dash[i] - (t+1) + 2*inds[i])
                        # if(filter(M)):
                            # M_gridnew.append(M)
        # M_grid = M_gridnew
        D = D[t+1:]
        D_dash = D_dash[t+1:]
        stepD(D, D_dash, 1)

if f == 1:
    print("WIN")
elif f == -1:
    print("LOSE")