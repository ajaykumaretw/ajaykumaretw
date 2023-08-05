i=2
num = 3
flag=True

while i < num:
    if(num % i) == 0:
        flag = False
    i = i+1
    
if flag:
    print('Number is a Prime Number')
else:
    print('Number  is not a Prime Number')