def count_up():
    for i in range(3):
        yield i 

for number in count_up():
    print(number)