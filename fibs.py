gFib = {}

def fibSLOW(n):
    if(n <= 1): return n
    if(n == 2): return 1
    return fibSLOW(n-1) + fibSLOW(n-2)

def fib(n):
    global gFib
    if n in gFib: return gFib[n]
    if(n <= 1):
        gFib[n] = n
        return n
    gFib[n] = fib(n-1) + fib(n-2)
    return gFib[n]

print(fib(1000))