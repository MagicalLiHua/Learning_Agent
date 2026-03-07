def file_generator(file_path):
    with open(file_path,'r') as file_obj:
        for line in file_obj:
            yield line
    file_obj.close()


gen = file_generator('./lines.txt')

print(next(gen))
print(next(gen))
print(next(gen))