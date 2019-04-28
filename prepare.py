import ver
import option
import nm

def cube_ready(NumnodeS):
    option.tran(ver.info_control_commands)
    print(ver.info_node)
    print(ver.info_control_commands)
    #print("num of nodes",NumnodeS)
    label_option = option.option(ver.info_control_commands)
    #print("sssssssssssssssssssssssssssssss",label_option)
    num_branch = 0
    num_c = 0
    num_l = 0
    for i in range(0,NumnodeS):
            for j in range(0,NumnodeS):
                if(ver.matrix[i][j][0] == 0):
                    print(0,end=' ')
                else:
                    if ver.matrix[i][j][0].ID[0] =='m':
                        print(ver.matrix[i][j][0].l, end=' ')
                    else:
                        print(ver.matrix[i][j][0].value, end=' ')
            print('\n')
    for i in range(0,NumnodeS):
        for j in  range(0,NumnodeS):
            if(ver.matrix[i][j][0]!=0):
                k = 0
                while(ver.matrix[i][j][k]!=0 and k<10):
                    tmp = ver.matrix[i][j][k]
                    if tmp.ID[0] != 'm':
                        tmp.value = nm.tran(tmp.value)
                    print(tmp.ID[0],'TMP.ID')
                    if(tmp.ID[0]=='r'):
                        ver.matrix_nodes[i][j] -= 1/float(tmp.value)
                        ver.matrix_nodes[j][i] -= 1/float(tmp.value)
                    if(tmp.ID[0]=='g'):
                        for p in range(0,NumnodeS):
                            for q in  range(0,NumnodeS):
                                if((p==ver.info_node[tmp.node1] and q==ver.info_node[tmp.node_control1]) or (p==ver.info_node[tmp.node2] and q==ver.info_node[tmp.node_control2])):
                                    ver.matrix_source_controled[p][q] += float(tmp.value)
                                    #print(p,q,ver.matrix_source_controled[p][q])
                                elif((p==ver.info_node[tmp.node2] and q==ver.info_node[tmp.node_control1]) or (p==ver.info_node[tmp.node1] and q==ver.info_node[tmp.node_control2])):
                                    ver.matrix_source_controled[p][q] -= float(tmp.value)
                                    #print(p,q,ver.matrix_source_controled[p][q])
                    if(tmp.ID[0]=='i'):
                        ver.matrix_RHS[ver.info_node[tmp.node1]] -= float(tmp.value)
                        ver.matrix_RHS[ver.info_node[tmp.node2]] += float(tmp.value)
                        print("GOT current")
                    if(tmp.ID[0]=='v'):
                        str_branch = tmp.ID
                        if len(ver.matrix_dc) and tmp.ID == ver.matrix_dc[0]:
                            tmp.value = ver.matrix_dc[1]

                        ver.info_branch.update({str_branch:num_branch})
                        num_branch = num_branch+1
                        ord = NumnodeS + ver.info_branch[str_branch]
                        ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                        ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= 1
                        ver.matrix_RHS[ord]  += float(tmp.value)
                        print("GOT voltage" ,ord)
                    if(tmp.ID[0]=='c'):
                        if label_option==0:
                            #print("ssssssssssssssssssssssssssssssssssssss",label_option)
                            str_branch = tmp.ID
                            ver.info_branch.update({str_branch:num_branch})
                            num_branch = num_branch+1
                            ord = NumnodeS + ver.info_branch[str_branch]
                            ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                            ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                            ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += float(tmp.value)*ver.lp_s
                            ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= float(tmp.value)*ver.lp_s
                            ver.matrix_nodes[ord][ord] -= 1
                            num_c += 1
                            print("GOT C" ,ord)
                        elif label_option==1:
                            str_branch = tmp.ID
                            ver.info_branch.update({str_branch:num_branch})
                            num_branch = num_branch+1
                            ord = NumnodeS + ver.info_branch[str_branch]
                            ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                            ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                            ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += float(tmp.value)*ver.lp_s
                            ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= float(tmp.value)*ver.lp_s
                            ver.matrix_nodes[ord][ord] -= 1
                            num_c += 1
                            print("GOT C" ,ord)
                        elif label_option==2:
                            str_branch = tmp.ID
                            ver.info_branch.update({str_branch:num_branch})
                            num_branch = num_branch+1
                            ord = NumnodeS + ver.info_branch[str_branch]
                            ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                            ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                            ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += float(tmp.value)*ver.lp_s
                            ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= float(tmp.value)*ver.lp_s
                            ver.matrix_nodes[ord][ord] -= 0.5
                            num_c += 1
                            print("GOT C" ,ord)
                        tmpmatrix = [ord,float(tmp.value),ver.info_node[tmp.node1],ver.info_node[tmp.node2],label_option,tmp.ic]
                        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',tmpmatrix)
                        ver.label_c.append(tmpmatrix)
                    if(tmp.ID[0]=='l'):
                        if label_option==0:
                            str_branch = tmp.ID
                            ver.info_branch.update({str_branch:num_branch})
                            num_branch = num_branch+1
                            ord = NumnodeS + ver.info_branch[str_branch]
                            ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                            ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                            ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += 1
                            ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= 1
                            ver.matrix_nodes[ord][ord] -= ver.lp_s * float(tmp.value)
                            num_l += 1
                            print("GOT L" ,ord)
                        elif label_option==1:
                            str_branch = tmp.ID
                            ver.info_branch.update({str_branch:num_branch})
                            num_branch = num_branch+1
                            ord = NumnodeS + ver.info_branch[str_branch]
                            ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                            ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                            ver.matrix_nodes[ord][ord] -= ver.lp_s * float(tmp.value)
                            num_l += 1
                            print("GOT L" ,ord)
                        elif label_option==2:
                            str_branch = tmp.ID
                            ver.info_branch.update({str_branch:num_branch})
                            num_branch = num_branch+1
                            ord = NumnodeS + ver.info_branch[str_branch]
                            ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                            ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                            ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += 0.5
                            ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= 0.5
                            ver.matrix_nodes[ord][ord] -= ver.lp_s * float(tmp.value)
                            num_l += 1
                            print("GOT L" ,ord)
                        tmpmatrix = [ord,float(tmp.value),ver.info_node[tmp.node1],ver.info_node[tmp.node2],label_option]
                        ver.label_l.append(tmpmatrix)
                    if(tmp.ID[0]=='e'):
                        str_branch = tmp.ID
                        ver.info_branch.update({str_branch:num_branch})
                        num_branch = num_branch+1
                        ord = NumnodeS + ver.info_branch[str_branch]
                        ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                        ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node_control1]] -= float(tmp.value)
                        ver.matrix_nodes[ord][ver.info_node[tmp.node_control2]] += float(tmp.value)
                        print("GOT  Evoltage" ,ord)
                    if(tmp.ID[0]=='f'):
                        str_branch = tmp.ID
                        ver.info_branch.update({str_branch:num_branch})
                        num_branch = num_branch+1
                        ord = NumnodeS + ver.info_branch[str_branch]
                        ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                        ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node_control1]] -= float(tmp.value)
                        ver.matrix_nodes[ord][ver.info_node[tmp.node_control2]] += float(tmp.value)
                        ver.matrix_RHS[ord]  += 0
                        print("GOT  FCURRENT" ,ord)
                    if(tmp.ID[0]=='h'):
                        str_branch = tmp.ID
                        ver.info_branch.update({str_branch:num_branch})
                        ver.info_branch.update({str_branch+'CC':num_branch+1})
                        num_branch = num_branch+2
                        ord = NumnodeS + ver.info_branch[str_branch]
                        ver.matrix_nodes[ver.info_node[tmp.node1]][ord] += 1
                        ver.matrix_nodes[ver.info_node[tmp.node2]][ord] -= 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node1]] += 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node2]] -= 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node_control1]] += 1
                        ver.matrix_nodes[ord][ver.info_node[tmp.node_control2]] -= 1
                        ver.matrix_nodes[ver.info_node[tmp.node_control1]][ord] += 1
                        ver.matrix_nodes[ver.info_node[tmp.node_control2]][ord] -= 1
                        ver.matrix_nodes[ord][ord+1] -= float(tmp.value)
                        ver.matrix_RHS[ord]  += 0
                        print("GOT  Hvoltage" ,ord)
                    if tmp.ID[0] == 'd':
                        tmpmatrix = [float(tmp.type),ver.info_node[tmp.node1],ver.info_node[tmp.node2]]
                        ver.label_dio.append(tmpmatrix)
                    k = k+1
                    if tmp.ID[0] == 'm':
                        print("Got a mos")
                        tmp.l = nm.tran(tmp.l)
                        tmp.w = nm.tran(tmp.w)
                        tmpmatrix = [tmp.mname,ver.info_node[tmp.d],ver.info_node[tmp.g],ver.info_node[tmp.b],ver.info_node[tmp.s],tmp.l,tmp.w]
                        ver.label_mos.append(tmpmatrix)
                        #print(ver.label_mos)

            if(i!=j):
                ver.matrix_nodes[i][i] -= ver.matrix_nodes[i][j]

    print("start")
    print("the cube of the circuit:")
    for i in range(0,NumnodeS):
        for j in  range(0,NumnodeS):
            ver.matrix_nodes[i][j] += ver.matrix_source_controled[i][j]
            print(ver.matrix_nodes[i][j], end=' ')
        print('\n')
    print('######################################\n######################################')
    print('the cube of RHS:')
    for i in  range(0,NumnodeS):
        print(ver.matrix_RHS[i], end=' ')
    print('\n')
