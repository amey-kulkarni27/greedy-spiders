import itertools

import matplotlib.pyplot as plt

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
    # print("Checking status...")
    n = len(A)
    
    for i in range(n):
        if A[i] < i + 1:
            return -1
    
    for i in range(n):
        if A[i] == i + 1:
            return 1
    return 0

def plot_graph(fcgs):
    '''
    Plotting graph for fcg
    '''
    # print("Plotting Graph...")
    np = len(fcgs)
    for i in range(np):
        n = len(fcgs[i])
        x = [j for j in range(n)]
        plt.plot(x, fcgs[i])
    plt.show()

def fcg(M):
    '''
    Flattened capacity graph for array M
    '''
    # print("Creating FCG...")
    m = len(M)
    if m == 0:
        return [0]
    cap = []
    for i in range(m):
        cap.append(M[i] - (i + 1))
    # flattened capacity array
    fca = [cap[i] for i in range(m)]
    for i in range(m - 2, -1, -1):
        fca[i] = min(fca[i], fca[i + 1])
    # print(M)
    # print(cap)
    # print(fca)
    n = M[len(M) - 1]
    fca_ret = [i for i in range(n + 1)]
    fca_ret[n] = fca[-1]
    ctr = m - 1
    while ctr >= 0 and n == M[ctr]:
        ctr -= 1
    for i in range(n-1, -1, -1):
        if ctr >= 0 and i == M[ctr]:
            fca_ret[i] = fca[ctr]
            while ctr >= 0 and i == M[ctr]:
                ctr -= 1
        else:
            fca_ret[i] = min(fca_ret[i], fca_ret[i+1])
    # print(fca_ret)
    for i in range(n):
        if fca_ret[i + 1] > fca_ret[i] + 1:
            fca_ret[i + 1] = fca_ret[i] + 1
    return fca_ret

def stepM(M, n):
    # print("Updating M...")
    for i in range(len(M)):
        M[i] -= n
        if M[i] <= 0:
            return -1
    return 1
    
def stepD(D, D_dash, n):
    # print("Updating D...")
    for i in range(len(D)):
        D[i] -= n
        D_dash[i] += n


def emergency_till(D):
    # print("Emergency Location...")
    ans = 0
    for i in range(len(D)):
        if D[i] == i + 1:
            ans = i
    return ans


def sizes(fcg1, fcg2):
    '''
    Make their sizes equal
    '''
    # print("Matching sizes...")
    l1 = len(fcg1)
    l2 = len(fcg2)
    if l1 < l2:
        for i in range(l1, l2):
            fcg1.append(fcg1[-1] + 1)
    else:
        for i in range(l2, l1):
            fcg2.append(fcg2[-1] + 1)


def compare(fcg1, fcg2):
    '''
    # if fcg1 is greater than or equal to fcg2, return 1
    # else if fcg1 is less than or equal to fcg2, return -1
    # else return 0
    '''
    # print("Comparing...")
    sizes(fcg1, fcg2)
    g = True # fcg1 >= fcg2
    l = True # fcg1 <= fcg2

    for i in range(len(fcg1)):
        if fcg1[i] > fcg2[i]:
            l = False
        if fcg1[i] < fcg2[i]:
            g = False
    if g:
        return 1
    elif l:
        return -1
    return 0


def filter(M, fcgM, M_gridnew, fcgsnew):
    '''
    0: Remove current M from M_gridnew
    1: Fine, add M to M_gridnew
    '''
    # print("Filtering...")
 
    if status(M) == -1:
        return 0

    i = 0
    # print(len(M_gridnew))
    while i < len(M_gridnew):
        c = compare(fcgM, fcgsnew[i])
        # if M == [3, 4, 5, 6, 8, 10, 10, 11] and i == 1:
        #     print(M, M_gridnew[i])
        #     print(fcg(M_gridnew[i]))
        #     print(fcgM, fcgsnew[i])
        # print(fcgM, fcgsnew[i])
        # if M is greater than or equal to M_gridnew[i], return 1
        # else if M is less than or equal to M_gridnew[i], return -1
        # else return 0
        if c == 1:
            M_gridnew.remove(M_gridnew[i])
            fcgsnew.remove(fcgsnew[i])
        elif c == -1:
            return 0
        else:
            i += 1
    # print(M_gridnew)
    return 1    
    

if __name__ == "__main__":
    # M_grid is a list of lists
    # Each list is a separate possibility
    M_grid = [[7, 8, 9, 12]]
    fcgs = [fcg(M_grid[0])]

    # print(fcgs[0])
    # plot_graph(fcgs[0])

    D = [3, 3, 4, 4]
    D_dash = [9, 10, 10, 12]
    # exit(0)

    while(len(M_grid)):
        # print(M_grid)
        M_gridnew = []
        fcgsnew = []
        if len(M_grid[0]) == 0:
            f = 1
            break
        s = status(D)
        if(s == 0):
            for M in M_grid:
                if len(M) != 0:
                    M.pop(0)
                stepM(M, 1)
                fcgM = fcg(M)
                isfilter = filter(M, fcgM, M_gridnew, fcgsnew)
                # print(inds, isfilter)
                if isfilter:
                    M_gridnew.append(M)
                    fcgsnew.append(fcgM)
            stepD(D, D_dash, 1)
        elif s == 1:
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
            # print("Permutating...")
            # print(t, D)
            perm_array = [i for i in range(t + 1)]
            for M in M_grid:
                if stepM(M, t + 1) == 1:
                    inds_list = list(itertools.permutations(perm_array))
                    for inds in inds_list:
                        M_copy = M[:]
                        for i in range(len(inds)):
                            ind = inds[i]
                            # i -> column number, inds[i] -> row number
                            M_copy.append(D_dash[i] - (t+1) + 2*inds[i])
                        M_copy.sort()
                        # print(M_copy)
                        fcgM = fcg(M_copy)
                        isfilter = filter(M_copy, fcgM, M_gridnew, fcgsnew)
                        # print(inds, isfilter)
                        if isfilter:
                            M_gridnew.append(M_copy)
                            fcgsnew.append(fcgM)
            D = D[t+1:]
            D_dash = D_dash[t+1:]
            stepD(D, D_dash, 1)
        M_grid = M_gridnew[:]
        fcgs = fcgsnew[:]
        print(M_grid)
        plot_graph(fcgs)


    if f == 1:
        print("WIN")
    elif f == -1:
        print("LOSE")