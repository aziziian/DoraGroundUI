print("Ian Azizi and #1221735190")
print('p\t\tq\t\tp->q')
print('------------------------------------')
def conditional(a,b):
    if a== True and b==False:
        c=False
    else:
        c=True
    return c
for p in True, False:
    for q in True, False:
        y=conditional(p,q)
        print(p,"\t\t",q,"\t\t",y)