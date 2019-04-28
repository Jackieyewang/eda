import ver
import oop
import matplotlib.pyplot as plt
def caclulater(NumnodeS):
    print("num of branch",ver.info_branch)
    gnd = int(ver.info_node['0'])
    extra_branch = len(ver.info_branch)
    print("START TO CACULATE",gnd ,"len(branch)",extra_branch)
    N_ex = NumnodeS+extra_branch
    ver.matrix_RHS_fff.append([0 for j in range(N_ex)])
    matrix_RHS_to_ca = ver.matrix_RHS[:gnd]+ver.matrix_RHS[gnd+1:N_ex]
    if len(ver.label_c):
        for p in range(0,len(ver.label_c)):
            matrix_RHS_to_ca[ver.label_c[p][0]-1] = int(ver.label_c[p][5])


    matrix_nodes_to_ca = ver.matrix_nodes[:gnd]+ver.matrix_nodes[gnd+1:N_ex]
    for i in range(0,N_ex-1):
        matrix_nodes_to_ca[i]=matrix_nodes_to_ca[i][:gnd]+matrix_nodes_to_ca[i][gnd+1:N_ex]
    for i in range(0,N_ex-1):
        for j in  range(0,N_ex-1):
            print(matrix_nodes_to_ca[i][j], end=' ')
        print('\n')
    print('the oringin cube of RHS for caculate:')
    for i in range(0,N_ex-1):
        print(matrix_RHS_to_ca[i], end=' ')
    if len(ver.label_c) or len(ver.label_l) or len(ver.label_dio) or len(ver.label_mos):
        if len(ver.info_plot):
            for u in range(len(ver.info_plot)):
                tmp = []
                tmpstr1 = ''
                tmpstr2 = ''
                b = 2
                for v in range(len(ver.info_plot[u])):
                    if ver.info_plot[u][0]=='v' and ver.info_plot[u][1]=='(':
                        while ver.info_plot[u][b] != ',' and ver.info_plot[u][b] != ')':
                            tmpstr1 += ver.info_plot[u][b]
                            b = b+1
                        if ver.info_plot[u][b] == ',':
                            b +=1
                            while ver.info_plot[u][b] != ')':
                                tmpstr2 += ver.info_plot[u][b]
                                b += 1

                v1 = ver.info_node[tmpstr1]
                if len(tmpstr2):
                    v2 = ver.info_node[tmpstr2]
                    if v1 > gnd:
                        v1 -= 1

                    if v2>gnd:
                        v2 -= 1

                    if v1 == gnd:
                        oop.oopCL(v2,-1,N_ex,gnd,matrix_RHS_to_ca,matrix_nodes_to_ca)
                    elif v2==gnd:
                        oop.oopCL(v1,-1,N_ex,gnd,matrix_RHS_to_ca,matrix_nodes_to_ca)
                    else:
                        oop.oopCL(v1,v2,N_ex,gnd,matrix_RHS_to_ca,matrix_nodes_to_ca)
                else:
                    if v1 != gnd:
                        oop.oopCL(v1,-1,N_ex,gnd,matrix_RHS_to_ca,matrix_nodes_to_ca)
                    else:
                        oop.oopCL(2,-1,N_ex,gnd,matrix_RHS_to_ca,matrix_nodes_to_ca)
        else:
            oop.oopCL(2,-1,N_ex,gnd,matrix_RHS_to_ca,matrix_nodes_to_ca)
        plt.show()
        #print("matrix_res",matrix_res)

    else:
        oop.calsim(N_ex,matrix_RHS_to_ca,matrix_nodes_to_ca)
