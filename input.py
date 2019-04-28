import ver
with open('text4.txt','r') as f:
        ver.list = f.readlines()


def get_input():
    for i in range(0,len(ver.list)):
        ver.list[i] = ver.list[i].rstrip('\n')
        ver.str = ver.list[i].lower()
        str_list = ver.str.split()
        ver.list_content.append(str_list)
        print(ver.list_content[i])
