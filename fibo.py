fibo = [1, 1]
for n in range(100):
    fibo.append(fibo[n] + fibo[n+1])

print(fibo)