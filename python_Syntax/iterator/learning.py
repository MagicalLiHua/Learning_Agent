my_list = [1,2,3,4,5,6]

print(hasattr(my_list,'__iter__'))

class LineInterator:
    def __init__(self,file_path):
        self.file_path = file_path
        self.file_obj = open(file_path,'r')

    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.file_obj.readline()
        if line:
            return line
        else:
            self.file_obj.close()
            raise StopIteration

line_iterator = LineInterator('lines.txt')
for line in line_iterator:
    print(line,end='')
