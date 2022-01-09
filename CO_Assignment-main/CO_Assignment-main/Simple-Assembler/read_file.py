import os

lines = os.read(0, 10**6).strip().splitlines()
list_of_instructions = []
for x in lines:
    line = x.decode('utf-8')
    temp_list = line
    if(temp_list != []):
        list_of_instructions.append(temp_list)
    #print(list_of_instructions[-1])
