
s = input(str)
result = []
s = list(s)

for i in s:
    if i.isdigit():
        result.append("number")
    else:
        result.append(i)

print("".join(result))