import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import ver
import option
def oopCL(v1,v2,N_ex,gnd,matrix_RHS_to_ca,matrix_nodes_to_ca):
        t = ver.t_start
        matrix_res = []
        matrix_t = []
        matrix_v = []
        m=[]
        res = [0 for j in range(N_ex)]
        #res[1] = 0.013
        ver.matrix_RHS_fff = list(matrix_RHS_to_ca)
        for i in range(0,ver.lp_s):
            t += ver.te
            if len(ver.label_c):
                for p in range(0,len(ver.label_c)):
                    if ver.label_c[p][2]>gnd:
                        ver.label_c[p][2] -= 1
                    if ver.label_c[p][3]>gnd:
                        ver.label_c[p][3] -= 1
                    r_c = res[ver.label_c[p][2]]
                    l_c = res[ver.label_c[p][3]]
                    if ver.label_c[p][2]==gnd:
                        r_c = 0
                    if ver.label_c[p][3]==gnd:
                        l_c = 0
                    if ver.label_c[p][4]==0:
                        #print(ver.matrix_RHS_fff,ver.label_c)
                        matrix_RHS_to_ca[ver.label_c[p][0]-1] += ver.label_c[p][1]*ver.lp_s*(r_c-l_c)
                    elif ver.label_c[p][4]==1:
                        #print(ver.matrix_RHS_fff,ver.label_c)
                        #print("sssssssssss",ver.matrix_RHS_fff,ver.label_c,ver.label_c[p][0]-1)
                        matrix_RHS_to_ca[ver.label_c[p][0]-1] += ver.label_c[p][1]*ver.lp_s*(r_c-l_c)+ver.matrix_RHS_fff[ver.label_c[p][0]-1]
                    elif ver.label_c[p][4]==2:
                        #print(ver.matrix_RHS_fff,ver.label_c)
                        matrix_RHS_to_ca[ver.label_c[p][0]-1] += ver.label_c[p][1]*ver.lp_s*(r_c-l_c)+0.5*ver.matrix_RHS_fff[ver.label_c[p][0]-1]
            if len(ver.label_l):
                for q in range(0,len(ver.label_l)):
                    if ver.label_l[q][2]>gnd:
                        ver.label_l[q][2] -= 1
                    if ver.label_l[q][3]>gnd:
                        ver.label_l[q][3] -= 1
                    l_l = res[ver.label_l[q][3]]
                    r_l = res[ver.label_l[q][2]]
                    if ver.label_l[q][2]==gnd:
                        r_l = 0

                    if ver.label_l[q][3]==gnd:
                        l_l = 0
                    if ver.label_l[p][4]==0:
                        #print(ver.matrix_RHS_fff,ver.label_l)
                        matrix_RHS_to_ca[ver.label_l[q][0]-1] -= ver.label_l[q][1]*ver.lp_s*ver.matrix_RHS_fff[ver.label_l[q][0]-1]
                    elif ver.label_c[p][4]==1:
                        matrix_RHS_to_ca[ver.label_l[q][0]-1] -= ver.label_l[q][1]*ver.lp_s*ver.matrix_RHS_fff[ver.label_l[q][0]-1]+(r_l-l_l)
                    elif ver.label_c[p][4]==2:
                        matrix_RHS_to_ca[ver.label_l[q][0]-1] -= ver.label_l[q][1]*ver.lp_s*ver.matrix_RHS_fff[ver.label_l[q][0]-1]+(r_l-l_l)*0.5
            #print(matrix_RHS_to_ca)
            if len(ver.label_dio):
                for k in range(0,len(ver.label_dio)):
                    a = ver.label_dio[k][0]
                    if ver.label_dio[k][1]>gnd:
                        ver.label_dio[k][1] -=1
                    if ver.label_dio[k][2]>gnd:
                        ver.label_dio[k][2] -= 1

                    if ver.label_dio[k][1]==gnd:
                        r_dio = 0
                        l_dio = res[ver.label_dio[k][2]]
                        v = r_dio - l_dio
                        J = a*math.exp(a*v)*v-math.exp(a*v)+1
                        matrix_nodes_to_ca[ver.label_dio[k][2]][ver.label_dio[k][2]] += a*math.exp(a*v)
                        matrix_RHS_to_ca[ver.label_dio[k][2]] -= J
                    elif ver.label_dio[k][2]==gnd:
                        r_dio = res[ver.label_dio[k][1]]
                        l_dio = 0
                        v = r_dio - l_dio
                        J = a*math.exp(a*v)*v-math.exp(a*v)+1
                        matrix_nodes_to_ca[ver.label_dio[k][1]][ver.label_dio[k][1]] += a*math.exp(a*v)
                        matrix_RHS_to_ca[ver.label_dio[k][1]] += J
                    else:
                        v = r_dio - l_dio
                        J = a*math.exp(a*v)*v-math.exp(a*v)+1
                        matrix_nodes_to_ca[ver.label_dio[k][1]][ver.label_dio[k][1]] += a*math.exp(a*v)
                        matrix_nodes_to_ca[ver.label_dio[k][2]][ver.label_dio[k][2]] += a*math.exp(a*v)
                        matrix_nodes_to_ca[ver.label_dio[k][1]][ver.label_dio[k][2]] -= a*math.exp(a*v)
                        matrix_nodes_to_ca[ver.label_dio[k][2]][ver.label_dio[k][1]] -= a*math.exp(a*v)
                        matrix_RHS_to_ca[ver.label_dio[k][1]] += J
                        matrix_RHS_to_ca[ver.label_dio[k][2]] -= J
                    matrix_v.append(v)
            if len(ver.matrix_dc):
                matrix_RHS_to_ca[ver.NumnodeS-2+ver.info_branch[ver.matrix_dc[0]]] += ver.matrix_dc[3]
                #print(matrix_RHS_to_ca)
            if len(ver.label_mos):
                for mo in range(len(ver.label_mos)):
                        tmp = ver.label_mos[mo]
                        #print(tmp)
                        if tmp[0] == "nmos" :
                            node_g = tmp[2]
                            node_d = tmp[1]
                            node_s = tmp[4]
                            Width = tmp[6]
                            Lenth = tmp[5]
                            print(tmp)
                            if node_g!=0 and node_s!=0 and node_d!=0:
                                Vgs = ver.matrix_RHS_fff[node_g-1] - ver.matrix_RHS_fff[node_s-1]
                                Vds = ver.matrix_RHS_fff[node_d-1] - ver.matrix_RHS_fff[node_s-1]
                            elif node_g!=0 and node_d!=0:
                                Vgs = ver.matrix_RHS_fff[node_g-1]
                                Vds = ver.matrix_RHS_fff[node_d-1]
                            elif node_g!=0 and node_s!=0:
                                Vgs = ver.matrix_RHS_fff[node_g-1] - ver.matrix_RHS_fff[node_s-1]
                                Vds = -ver.matrix_RHS_fff[node_s-1]
                            elif node_d!=0 and node_s!=0:
                                Vgs = -ver.matrix_RHS_fff[node_s-1]
                                Vds = ver.matrix_RHS_fff[node_d-1] -ver.matrix_RHS_fff[node_s-1]
                            elif node_g!=0:
                                Vgs = ver.matrix_RHS_fff[node_g-1]
                                Vds = 0
                            elif node_d!=0:
                                Vgs = 0
                                Vds = ver.matrix_RHS_fff[node_d-1]
                            else:
                                Vgs = -ver.matrix_RHS_fff[node_s-1]
                                Vds = -ver.matrix_RHS_fff[node_s-1]
                            Vt = 0.43
                            Kn = 115e-6
                            lamda = 0.06
                            gds = 0
                            gm = 0
                            if (Vgs > Vt) and ( 0 < Vds < Vgs - Vt):
                                gm = Width / Lenth * Kn * Vds * (1 + lamda * Vds)
                                gds = Width / Lenth * Kn * (Vgs - Vt - Vds) * (1 + lamda * Vds) + lamda * Width / Lenth * Kn * ((Vgs - Vt) * Vds - 0.5 * Vds ** 2)
                                matrix_RHS_to_ca[node_d] -= Width / Lenth * Kn * ((Vgs - Vt) * Vds - 0.5 * Vds ** 2)*(1 + lamda * Vds) - gm * Vgs - gds * Vds
                                matrix_RHS_to_ca[node_s] += Width / Lenth * Kn * ((Vgs - Vt) * Vds - 0.5 * Vds ** 2)*(1 + lamda * Vds) - gm * Vgs - gds * Vds

                            if (Vgs > Vt) and (Vds >= Vgs - Vt) :
                                gm = Width / Lenth * Kn * (Vgs - Vt) * (1 + lamda * Vds)
                                gds = 0.5 * Width / Lenth * Kn * (Vgs - Vt) ** 2 * lamda
                                matrix_RHS_to_ca[node_d] -= 0.5 * Width / Lenth * Kn * (Vgs - Vt) ** 2 * (1 + lamda * Vds) - gm * Vgs - gds * Vds
                                matrix_RHS_to_ca[node_s] += 0.5 * Width / Lenth * Kn * (Vgs - Vt) ** 2 * (1 + lamda * Vds)- gm * Vgs - gds * Vds

                            if (Vgs > Vt) and (Vds <= 0) :
                                gm = Width / Lenth * Kn * Vds
                                gds = Width / Lenth * Kn * (Vgs - Vt - Vds)
                                matrix_RHS_to_ca[node_d] -= Width / Lenth * Kn * ((Vgs - Vt) * Vds - 0.5 * Vds ** 2) - gm * Vgs - gds * Vds
                                matrix_RHS_to_ca[node_s] += Width / Lenth * Kn * ((Vgs - Vt) * Vds - 0.5 * Vds ** 2) - gm * Vgs - gds * Vds

                            matrix_nodes_to_ca[node_d][node_d] += gds
                            matrix_nodes_to_ca[node_d][node_s] -= gds + gm
                            matrix_nodes_to_ca[node_d][node_g] += gm
                            matrix_nodes_to_ca[node_s][node_d] -= gds
                            matrix_nodes_to_ca[node_s][node_s] += gds + gm
                            matrix_nodes_to_ca[node_s][node_g] -= gm

                        if tmp[0] == "pmos" :
                            node_g = tmp[2]
                            node_d = tmp[1]
                            node_s = tmp[4]
                            Width = tmp[6]
                            Lenth = tmp[5]

                            if node_g!=0 :
                                Vg = ver.matrix_RHS_fff[node_g-1]
                            else :
                                Vg = 0
                            if node_d!=0 :
                                Vd = ver.matrix_RHS_fff[node_d-1]
                            else :
                                Vd = 0
                            if node_s!=0 :
                                Vs = ver.matrix_RHS_fff[node_s-1]
                            else :
                                Vs = 0
                            Vgs = Vg - Vs
                            Vds = Vd - Vs
                            Vsg = - Vgs
                            Vsd = - Vds
                            Vt = -0.4
                            Kp = -30e-6
                            lamda = -0.1
                            gds = 0
                            gm = 0
                            if (Vsg > -Vt) and (0 < Vsd < Vsg + Vt):
                                gm = -Width / Lenth * Kp * Vsd * (1 - lamda * Vsd)
                                gds = -Width / Lenth * Kp * (Vsg + Vt - Vsd) * (1 - lamda * Vsd) + lamda * Width / Lenth * Kp * ((Vsg + Vt) * Vsd - 0.5 * Vsd ** 2)
                                matrix_RHS_to_ca[node_d] -= Width / Lenth * Kp * ((Vsg + Vt) * Vsd - 0.5 * Vsd ** 2) * (1 - lamda * Vsd) - gm * Vgs - gds * Vds
                                matrix_RHS_to_ca[node_s] += Width / Lenth * Kp * ((Vsg + Vt) * Vsd - 0.5 * Vsd ** 2) * (1 - lamda * Vsd) - gm * Vgs - gds * Vds

                            if (Vsg > -Vt) and (Vsd >= Vsg + Vt) :
                                gm = -Width / Lenth * Kp * (Vsg + Vt) * (1 - lamda * Vsd)
                                gds = lamda * 0.5 * Width / Lenth * Kp * (Vsg + Vt) ** 2
                                matrix_RHS_to_ca[node_d] -= 0.5 * Width / Lenth * Kp * (Vsg + Vt) ** 2 * (1 - lamda * Vsd) - gm * Vgs - gds * Vds
                                matrix_RHS_to_ca[node_s] += 0.5 * Width / Lenth * Kp * (Vsg + Vt) ** 2 * (1 - lamda * Vsd) - gm * Vgs - gds * Vds

                            if (Vsg > -Vt) and (Vsd <= 0):
                                gm = -Width / Lenth * Kp * Vsd
                                gds = -Width / Lenth * Kp * (Vsg + Vt - Vsd)
                                matrix_RHS_to_ca[node_d] -= Width / Lenth * Kp * ((Vsg + Vt) * Vsd - 0.5 * Vsd ** 2) - gm * Vgs - gds * Vds
                                matrix_RHS_to_ca[node_s] += Width / Lenth * Kp * ((Vsg + Vt) * Vsd - 0.5 * Vsd ** 2) - gm * Vgs - gds * Vds

                            matrix_nodes_to_ca[node_d][node_d] += gds
                            matrix_nodes_to_ca[node_d][node_s] -= gds + gm
                            matrix_nodes_to_ca[node_d][node_g] += gm
                            matrix_nodes_to_ca[node_s][node_d] -= gds
                            matrix_nodes_to_ca[node_s][node_s] += gds + gm
                            matrix_nodes_to_ca[node_s][node_g] -= gm

            #print(matrix_nodes_to_ca)
            a = np.array(matrix_nodes_to_ca)
            b = np.array(matrix_RHS_to_ca)
            res = np.linalg.solve(a,b)
            ver.matrix_RHS_fff= list(res)
            #print(matrix_RHS_to_ca)

            if v1 == -1:
                matrix_res.append(0)
            elif v2 == -1:
                matrix_res.append(res[0])
            else:
                matrix_res.append(res[v2]-res[v1])


            #print(m)
            matrix_t.append(t)
            #print(ver.matrix_RHS_fff)
            for p in range(0,len(ver.label_c)):
                matrix_RHS_to_ca[ver.label_c[p][0]-1] = 0
            for q in range(0,len(ver.label_l)):
                matrix_RHS_to_ca[ver.label_l[q][0]-1] = 0


        plt.plot(matrix_t,matrix_res)
        #plt.plot(matrix_t,matrix_res)



def calsim(N_ex,matrix_RHS_to_ca,matrix_nodes_to_ca):
        print('the cube of RHS for caculate:')
        for i in range(0,N_ex-1):
            print(matrix_RHS_to_ca[i], end=' ')
        print('\n')
        print("the cube of the circuit to caculate:")
        for i in range(0,N_ex-1):
            for j in  range(0,N_ex-1):
                print(matrix_nodes_to_ca[i][j], end=' ')
            print('\n')

        a = np.array(matrix_nodes_to_ca)
        b = np.array(matrix_RHS_to_ca)
        res = np.linalg.solve(a,b)
        ver.res = res
        print(res)
