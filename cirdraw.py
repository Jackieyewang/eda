import ver
import nm
def draw():
    num_node = 0
    com = 1
    comd = 1
    for i in range(0,len(ver.list_content)):
        if i==0:
            str = ver.list_content[i]
            #print(ver.list)
        elif i==len(ver.list_content)-1:
            if ver.list_content[i]==['.end']:
                print('end!finish')
                return num_node
            else:
                print('error!')
                return 0
        else:
            tmp = ver.list_content[i][0][0]
            if(ver.list_content[i][0]=="\'\'\'"):
                com = -com
                continue
            if(ver.list_content[i][0]=="\"\"\"" ):
                comd = -comd
                continue
            if(com == -1 or comd == -1):
                continue
            if(tmp == '.'):
                if(len(ver.list_content[i])>1):
                    if ver.list_content[i][0][1] == 't':
                        if len(ver.list_content[i])==4:
                            elem = ver.tran(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3])
                        elif len(ver.list_content[i])==3:
                            elem = ver.tran(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],0)
                        else:
                            elem = ver.Control(ver.list_content[i][0],0)
                        ver.info_control_commands.update({'.tran':elem})

                    elif ver.list_content[i][0][1] == 'p':
                        tmppl = ''
                        for tm in range(2,len(ver.list_content[i])):
                            tmppl += ver.list_content[i][tm]+' '
                        elem = ver.plot(ver.list_content[i][0],ver.list_content[i][1],tmppl)
                        ver.info_control_commands.update({'.plot':elem})

                    elif ver.list_content[i][0][1] == 'd':
                        tmpdc = ver.list_content[i]
                        print(ver.list_content[i])
                        elem = ver.dc("dc",tmpdc[1],tmpdc[2],tmpdc[3],tmpdc[4])
                        ver.info_control_commands.update({'.dc':elem})
                    else:
                        for j in range(2,len(ver.list_content[i])):
                            ver.list_content[i][1] += ver.list_content[i][j]+' '
                        elem = ver.Control(ver.list_content[i][0],ver.list_content[i][1])
                        ver.info_control_commands.update({elem.command:elem.oth})


                else:
                    elem = ver.Control(ver.list_content[i][0],0)
                    ver.info_control_commands.update({elem.command:elem.oth})
            elif(tmp=='#' or tmp=='*'):
                continue
############################################################################
#start to store the information of the circuit
############################################################################
            else:
                #create a dict to store the node
                if(ver.list_content[i][1] not in ver.info_node):
                    ver.info_node.update({ver.list_content[i][1]:num_node})
                    num_node += 1
                if(ver.list_content[i][2] not in ver.info_node):
                    ver.info_node.update({ver.list_content[i][2]:num_node})
                    num_node += 1
                #store the infomation of all elements
                if(tmp=='v'):
                    k = 0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    if(nm.is_number(ver.list_content[i][3][0])==True):
                        if(len(ver.list_content[i])>4):
                            for j in range(5,len(ver.list_content[i])):
                                ver.list_content[i][4] += ver.list_content[i][j]
                            elem = ver.Source(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],ver.list_content[i][4])
                        else:
                            elem = ver.Source(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],'')
                        ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
                    else:
                        for j in range(4,len(ver.list_content[i])):
                            ver.list_content[i][3] += ver.list_content[i][j]
                        elem = ver.Source(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],0,ver.list_content[i][3])
                        ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem

                elif(tmp=='i'):
                    k = 0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    if(nm.is_number(ver.list_content[i][3][0])==True):
                        if(len(ver.list_content[i])>4):
                            for j in range(5,len(ver.list_content[i])):
                                ver.list_content[i][4] += ver.list_content[i][j]
                            elem = ver.Source(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],ver.list_content[i][4])
                        else:
                            elem = ver.Source(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],'')
                        ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
                    else:
                        for j in range(4,len(ver.list_content[i])):
                            ver.list_content[i][3] += ver.list_content[i][j]
                        elem = ver.Source(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],0,ver.list_content[i][3])
                        ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem


                elif(tmp=='r'):
                    k = 0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    elem = ver.Element(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3])
                    ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
                if(tmp=='c'):
                    k = 0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    str = ''
                    if(len(ver.list_content[i])==5):
                        tmpstr = ver.list_content[i][4]
                        g = len(tmpstr)
                        print(g)
                        for w in range(len(tmpstr)):
                            if(tmpstr[w]=='='):
                                g = w
                            if(w>g and tmpstr[w]!=' '):
                                str += tmpstr[w]
                    if str=='':
                        str = '0'
                    elem = ver.cElement(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],str)
                    ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
                if(tmp=='l'):
                    k = 0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    elem = ver.Element(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3])
                    ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
                if(tmp=='g' or tmp =='e'):
                    k = 0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    elem = ver.Source_controled(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],ver.list_content[i][4],ver.list_content[i][5])
                    ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem

                if(tmp=='f' or tmp=='h'):
                    k = 0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    elem = ver.Source_controled(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],ver.list_content[i][4])
                    ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
                if tmp == 'd':
                    k=0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    elem = ver.diode(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3])
                    ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
                if tmp == 'm':
                    k=0
                    while ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]!=0:
                        k = k+1
                    l = ver.list_content[i][6][2:]
                    w = ver.list_content[i][6][2:]
                    elem = ver.mos(ver.list_content[i][0],ver.list_content[i][1],ver.list_content[i][2],ver.list_content[i][3],ver.list_content[i][4],ver.list_content[i][5],l,w)
                    #print('cccccccccccccccdddcccccccccccccc',elem.d,elem.g,elem.s)
                    ver.matrix[ver.info_node[ver.list_content[i][1]]][ver.info_node[ver.list_content[i][2]]][k]=elem
