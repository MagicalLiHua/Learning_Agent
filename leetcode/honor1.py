import math
import sys

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    input_data = sys.stdin.readline().strip()

    data = list(map(int,input_data.split(",")))

    prime_nums = set()

    for item in data:
        if is_prime(int(item)):
            if item not in prime_nums:
                prime_nums.add(item)

    if not prime_nums:
        print("empty")
    else:
        sorted_prime_nums = sorted(list(prime_nums))
        print(",".join(map(str, sorted_prime_nums)))


if __name__ == "__main__":
    main()
