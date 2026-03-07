def prime_generator(limit):
    for i in range(2,limit+1):
        if judge(i):
            yield i

def judge(number):
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True


prime_gen = prime_generator(10)

for i in prime_gen:
    print(i)