

n = 11
l = []
for x in range(2, n):
    for i in range(20):
        l.append(pow(x,i,n))
    print(x)
    print(sorted(list(set(l))))
    l=[]