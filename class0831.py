# simple search
def search(x, N):
    A = range(N)
    for k in range(N):
        if A[k] == x:
            return True
    return False