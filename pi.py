import numpy as np

# update algorithm
def update(a, b, t, p):
    new_a = (a+b)/2.0
    new_b = np.sqrt(a*b)
    new_t = t-p*(a-new_a)**2
    new_p = 2*p
    return new_a,new_b,new_t,new_p

# initialize
a = 1.0
b = 1/np.sqrt(2)
t = 0.25
p = 1.0
print("0 : {0:.10f}".format((a+b)**2/(4*t)))

# run
for i in range(5):
    a,b,t,p = update(a,b,t,p)    
    print("{0} : {1:.15f}".format(i+1,(a+b)**2/(4*t)))

