#coding:utf-8
import bisect
import struct
from tkinter import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

list = []; #the oringin list to store the information
list_content = [];   #proceed input information
str = '';  # a string to store the information from every lines
info_node = {};  # a list to store every nodes and label
info_branch = {};
NumnodeS = 0;   #number of nodes
info_control_commands = {}; # information of every control command
matrix = [[[0 for j in range(10)] for j in range(1000)] for i in range(1000)];   #the matrix that store the circuit
conversion = {'f':10**-15,'p':10**-12,'n':10**-9,'u':10**-6,'m':10**-3,'k':10**3,'meg':10**6,'g':10**9,'t':10**12}#unit conversion
matrix_nodes = [[0 for j in range(1000)] for i in range(1000)];
matrix_source_controled = [[0 for j in range(100)] for i in range(100)];
matrix_V = [0 for j in range(10)];
matrix_RHS = [0 for j in range(20)];
lp_s = 10;
T = 10;
label_c = [];
label_l = [];

with open('text4.txt','r') as f:
        list = f.readlines()

class Element:
    def __init__(self,id,u,v,s):
        self.ID = id;
        self.node1 = u;
        self.node2 = v;
        self.value = s;

class Source:
    def __init__(self,id,u,v,s,a):
        self.ID = id;
        self.node1 = u;
        self.node2 = v;
        '''
        if(self.ID[0]=='i'):
            self.value = s + 'A';
        if(self.ID[0]=='v'):
            self.value = s + 'V';
        '''
        self.value = s;
        self.oth = a;

class Source_controled:
    def __init__(self,id,u,v,p,q,s):
        self.ID = id;
        self.node1 = u;
        self.node2 = v;
        self.node_control1 = p;
        self.node_control2 = q;
        self.value = s;

class Source_controled_fh:
    def __init__(self,id,u,v,c,s):
        self.ID = id;
        self.node1 = u;
        self.node2 = v;
        self.cl = c;
        self.value = s;

class Control:
    def __init__(self,op,control):
        self.command = op;
        self.oth = control;
###########################################################################################################
#get the input fron netlist
###########################################################################################################
def get_input():
    for i in range(0,len(list)):
        list[i] = list[i].rstrip('\n');
        str = list[i].lower();
        str_list = str.split();
        list_content.append(str_list);
        print(list_content[i]);

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def find_index_of_str(s1, s2):
    lt=s1.split(s2,1)
    if len(lt)==1:
        return FALSE
    return True
##################################################################################
#STORE INFORMATION                                                               #
###################################################################################
def draw():
    num_node = 0;
    com = 1;
    comd = 1;
    for i in range(0,len(list_content)):
        if i==0:
            str = list_content[i];
            print(list[0]);
        elif i==len(list_content)-1:
            if list_content[i]==['.end']:
                print('end!finish');
                return num_node;
            else:
                print('error!');
                return 0;
        else:
            tmp = list_content[i][0][0];
            if(list_content[i][0]=="\'\'\'"):
                com = -com;
                continue;
            if(list_content[i][0]=="\"\"\"" ):
                comd = -comd;
                continue;
            if(com == -1 or comd == -1):
                continue;
            if(tmp == '.'):
                if(len(list_content[i])>1):
                    for j in range(2,len(list_content[i])):
                        list_content[i][1] += list_content[i][j]+' ';
                    elem = Control(list_content[i][0],list_content[i][1]);
                else:
                    elem = Control(list_content[i][0],0);
                info_control_commands.update({elem.command:elem.oth});
            elif(tmp=='#' or tmp=='*'):
                continue;
############################################################################
#start to store the information of the circuit
############################################################################
            else:
                #create a dict to store the node
                if(list_content[i][1] not in info_node):
                    info_node.update({list_content[i][1]:num_node});
                    num_node += 1;
                if(list_content[i][2] not in info_node):
                    info_node.update({list_content[i][2]:num_node});
                    num_node += 1;
                #store the infomation of all elements
                if(tmp=='v'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    if(is_number(list_content[i][3][0])==True):
                        if(len(list_content[i])>4):
                            for j in range(5,len(list_content[i])):
                                list_content[i][4] += list_content[i][j];
                            elem = Source(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3],list_content[i][4]);
                        else:
                            elem = Source(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3],'');
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                    else:
                        for j in range(4,len(list_content[i])):
                            list_content[i][3] += list_content[i][j];
                        elem = Source(list_content[i][0],list_content[i][1],list_content[i][2],0,list_content[i][3]);
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;

                elif(tmp=='i'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    if(is_number(list_content[i][3][0])==True):
                        if(len(list_content[i])>4):
                            for j in range(5,len(list_content[i])):
                                list_content[i][4] += list_content[i][j];
                            elem = Source(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3],list_content[i][4]);
                        else:
                            elem = Source(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3],'');
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                    else:
                        for j in range(4,len(list_content[i])):
                            list_content[i][3] += list_content[i][j];
                        elem = Source(list_content[i][0],list_content[i][1],list_content[i][2],0,list_content[i][3]);
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;


                elif(tmp=='r'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Element(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                if(tmp=='c'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Element(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                if(tmp=='l'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Element(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                if(tmp=='g' or tmp =='e'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Source_controled(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3],list_content[i][4],list_content[i][5]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;

                if(tmp=='f' or tmp=='h'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Source_controled(list_content[i][0],list_content[i][1],list_content[i][2],list_content[i][3],list_content[i][4]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;

##########################################################################################################################################
# prepare for the cubes
##########################################################################################################################################

def cube_ready(NumnodeS):
    print(info_node);
    print(info_control_commands);
    print("num of nodes",NumnodeS);
    label_option = option();
    print("sssssssssssssssssssssssssssssss",label_option)
    num_branch = 0;
    num_c = 0;
    num_l = 0;
    for i in range(0,NumnodeS):
            for j in range(0,NumnodeS):
                if(matrix[i][j][0] == 0):
                    print(0,end=' ');
                else:
                    print(matrix[i][j][0].value, end=' ');
            print('\n');
    for i in range(0,NumnodeS):
        for j in  range(0,NumnodeS):
            if(matrix[i][j][0]!=0):
                k = 0;
                while(matrix[i][j][k]!=0 and k<10):
                    tmp = matrix[i][j][k];
                    print(tmp.ID[0],'TMP.ID');
                    if(tmp.ID[0]=='r'):
                        matrix_nodes[i][j] -= 1/float(tmp.value);
                    if(tmp.ID[0]=='g'):
                        for p in range(0,NumnodeS):
                            for q in  range(0,NumnodeS):
                                if((p==info_node[tmp.node1] and q==info_node[tmp.node_control1]) or (p==info_node[tmp.node2] and q==info_node[tmp.node_control2])):
                                    matrix_source_controled[p][q] += float(tmp.value);
                                    #print(p,q,matrix_source_controled[p][q]);
                                elif((p==info_node[tmp.node2] and q==info_node[tmp.node_control1]) or (p==info_node[tmp.node1] and q==info_node[tmp.node_control2])):
                                    matrix_source_controled[p][q] -= float(tmp.value);
                                    #print(p,q,matrix_source_controled[p][q]);
                    if(tmp.ID[0]=='i'):
                        matrix_RHS[info_node[tmp.node1]] -= float(tmp.value);
                        matrix_RHS[info_node[tmp.node2]] += float(tmp.value);
                        print("GOT current");
                    if(tmp.ID[0]=='v'):
                        str_branch = tmp.ID;
                        info_branch.update({str_branch:num_branch});
                        num_branch = num_branch+1;
                        ord = NumnodeS + info_branch[str_branch];
                        matrix_nodes[info_node[tmp.node1]][ord] += 1;
                        matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                        matrix_nodes[ord][info_node[tmp.node1]] += 1;
                        matrix_nodes[ord][info_node[tmp.node2]] -= 1;
                        matrix_RHS[ord]  += float(tmp.value);
                        print("GOT voltage" ,ord);
                    if(tmp.ID[0]=='c'):
                        if label_option==0:
                            str_branch = tmp.ID;
                            info_branch.update({str_branch:num_branch});
                            num_branch = num_branch+1;
                            ord = NumnodeS + info_branch[str_branch];
                            matrix_nodes[info_node[tmp.node1]][ord] += 1;
                            matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                            matrix_nodes[ord][info_node[tmp.node1]] += float(tmp.value)*lp_s;
                            matrix_nodes[ord][info_node[tmp.node2]] -= float(tmp.value)*lp_s;
                            matrix_nodes[ord][ord] -= 1;
                            tmpmatrix = [ord,float(tmp.value),info_node[tmp.node1],info_node[tmp.node2]]
                            label_c.append(tmpmatrix);
                            num_c += 1;
                            print("GOT C" ,ord);
                        elif label_option==1:
                            str_branch = tmp.ID;
                            info_branch.update({str_branch:num_branch});
                            num_branch = num_branch+1;
                            ord = NumnodeS + info_branch[str_branch];
                            matrix_nodes[info_node[tmp.node1]][ord] += 1;
                            matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                            matrix_nodes[ord][ord] += 1;
                            tmpmatrix = [ord,float(tmp.value),info_node[tmp.node1],info_node[tmp.node2]]
                            label_c.append(tmpmatrix);
                            num_c += 1;
                            print("GOT C" ,ord);
                        elif label_option==2:
                            str_branch = tmp.ID;
                            info_branch.update({str_branch:num_branch});
                            num_branch = num_branch+1;
                            ord = NumnodeS + info_branch[str_branch];
                            matrix_nodes[info_node[tmp.node1]][ord] += 1;
                            matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                            matrix_nodes[ord][info_node[tmp.node1]] += 2*float(tmp.value)*lp_s;
                            matrix_nodes[ord][info_node[tmp.node2]] -= 2*float(tmp.value)*lp_s;
                            matrix_nodes[ord][ord] -= 1;
                            tmpmatrix = [ord,float(tmp.value),info_node[tmp.node1],info_node[tmp.node2]]
                            label_c.append(tmpmatrix);
                            num_c += 1;
                            print("GOT C" ,ord);

                    if(tmp.ID[0]=='l'):
                        if label_option==0:
                            str_branch = tmp.ID;
                            info_branch.update({str_branch:num_branch});
                            num_branch = num_branch+1;
                            ord = NumnodeS + info_branch[str_branch];
                            matrix_nodes[info_node[tmp.node1]][ord] += 1;
                            matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                            matrix_nodes[ord][info_node[tmp.node1]] += 1;
                            matrix_nodes[ord][info_node[tmp.node2]] -= 1;
                            matrix_nodes[ord][ord] -= lp_s * float(tmp.value);
                            tmpmatrix = [ord,float(tmp.value),info_node[tmp.node1],info_node[tmp.node2]]
                            label_l.append(tmpmatrix);
                            num_l += 1;
                            print("GOT L" ,ord);
                        elif label_option==1:
                            str_branch = tmp.ID;
                            info_branch.update({str_branch:num_branch});
                            num_branch = num_branch+1;
                            ord = NumnodeS + info_branch[str_branch];
                            matrix_nodes[info_node[tmp.node1]][ord] += 1;
                            matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                            matrix_nodes[ord][ord] += 1;
                            tmpmatrix = [ord,float(tmp.value),info_node[tmp.node1],info_node[tmp.node2]]
                            label_l.append(tmpmatrix);
                            num_l += 1;
                            print("GOT L" ,ord);
                        elif label_option==2:
                            str_branch = tmp.ID;
                            info_branch.update({str_branch:num_branch});
                            num_branch = num_branch+1;
                            ord = NumnodeS + info_branch[str_branch];
                            matrix_nodes[info_node[tmp.node1]][ord] += 1;
                            matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                            matrix_nodes[ord][info_node[tmp.node1]] += 2*float(tmp.value)*lp_s;
                            matrix_nodes[ord][info_node[tmp.node2]] -= 2*float(tmp.value)*lp_s;
                            matrix_nodes[ord][ord] -= 1;
                            tmpmatrix = [ord,float(tmp.value),info_node[tmp.node1],info_node[tmp.node2]]
                            label_l.append(tmpmatrix);
                            num_l += 1;
                            print("GOT L" ,ord);
                    if(tmp.ID[0]=='e'):
                        str_branch = tmp.ID;
                        info_branch.update({str_branch:num_branch});
                        num_branch = num_branch+1;
                        ord = NumnodeS + info_branch[str_branch];
                        matrix_nodes[info_node[tmp.node1]][ord] += 1;
                        matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                        matrix_nodes[ord][info_node[tmp.node1]] += 1;
                        matrix_nodes[ord][info_node[tmp.node2]] -= 1;
                        matrix_nodes[ord][info_node[tmp.node_control1]] -= float(tmp.value);
                        matrix_nodes[ord][info_node[tmp.node_control2]] += float(tmp.value);
                        print("GOT  Evoltage" ,ord);
                    if(tmp.ID[0]=='f'):
                        str_branch = tmp.ID;
                        info_branch.update({str_branch:num_branch});
                        num_branch = num_branch+1;
                        ord = NumnodeS + info_branch[str_branch];
                        matrix_nodes[info_node[tmp.node1]][ord] += 1;
                        matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                        matrix_nodes[ord][info_node[tmp.node1]] += 1;
                        matrix_nodes[ord][info_node[tmp.node2]] -= 1;
                        matrix_nodes[ord][info_node[tmp.node_control1]] -= float(tmp.value);
                        matrix_nodes[ord][info_node[tmp.node_control2]] += float(tmp.value);
                        matrix_RHS[ord]  += 0;
                        print("GOT  FCURRENT" ,ord);
                    if(tmp.ID[0]=='h'):
                        str_branch = tmp.ID;
                        info_branch.update({str_branch:num_branch});
                        info_branch.update({str_branch+'CC':num_branch+1});
                        num_branch = num_branch+2;
                        ord = NumnodeS + info_branch[str_branch];
                        matrix_nodes[info_node[tmp.node1]][ord] += 1;
                        matrix_nodes[info_node[tmp.node2]][ord] -= 1;
                        matrix_nodes[ord][info_node[tmp.node1]] += 1;
                        matrix_nodes[ord][info_node[tmp.node2]] -= 1;
                        matrix_nodes[ord][info_node[tmp.node_control1]] += 1;
                        matrix_nodes[ord][info_node[tmp.node_control2]] -= 1;
                        matrix_nodes[info_node[tmp.node_control1]][ord] += 1;
                        matrix_nodes[info_node[tmp.node_control2]][ord] -= 1;
                        matrix_nodes[ord][ord+1] -= float(tmp.value);
                        matrix_RHS[ord]  += 0;
                        print("GOT  Hvoltage" ,ord);
                    k = k+1;
            if(matrix[j][i][0]!=0):
                k = 0;
                while(matrix[j][i][k]!=0 and k<10):
                    tmp = matrix[j][i][k];
                    if(tmp.ID[0]=='r'):
                        matrix_nodes[i][j] -= 1/float(tmp.value);
                    k = k+1;
            if(i!=j):
                matrix_nodes[i][i] -= matrix_nodes[i][j];

    print("start");
    print("the cube of the circuit:")
    for i in range(0,NumnodeS):
        for j in  range(0,NumnodeS):
            matrix_nodes[i][j] += matrix_source_controled[i][j];
            print(matrix_nodes[i][j], end=' ');
        print('\n');
    print('######################################\n######################################');
    print('the cube of RHS:');
    for i in  range(0,NumnodeS):
        print(matrix_RHS[i], end=' ');
    print('\n');

##################################################################################################
# START TO CACULATE
##################################################################################################
def caclulater(NumnodeS):
    print("num of branch",info_branch);
    gnd = int(info_node['0']);
    extra_branch = len(info_branch);
    print("START TO CACULATE",gnd ,"len(branch)",extra_branch);
    matrix_RHS_to_ca = matrix_RHS[:gnd]+matrix_RHS[gnd+1:NumnodeS+extra_branch];
    matrix_nodes_to_ca = matrix_nodes[:gnd]+matrix_nodes[gnd+1:NumnodeS+extra_branch];
    for i in range(0,NumnodeS+extra_branch-1):
        matrix_nodes_to_ca[i]=matrix_nodes_to_ca[i][:gnd]+matrix_nodes_to_ca[i][gnd+1:NumnodeS+extra_branch];
    print("the cube of the circuit to caculate:")
    for i in range(0,NumnodeS+extra_branch-1):
        for j in  range(0,NumnodeS+extra_branch-1):
            print(matrix_nodes_to_ca[i][j], end=' ');
        print('\n');
    print('the oringin cube of RHS for caculate:');
    for i in range(0,NumnodeS+extra_branch-1):
        print(matrix_RHS_to_ca[i], end=' ');
    print('\n');
    option()
    if len(label_c) or len(label_l):
        t = 0;
        matrix_res = [];
        matrix_t = [];
        matrix_t.append(0)
        matrix_res.append(0)
        res = [0 for j in range(NumnodeS+extra_branch)]
        for i in range(0,lp_s):
            t += T/lp_s;
            if len(label_c):
                for p in range(0,len(label_c)):
                    matrix_RHS_to_ca[label_c[p][0]-1] += label_c[p][1]*lp_s*(res[label_c[p][2]]-res[label_c[p][3]])
            if len(label_l):
                for q in range(0,len(label_l)):
                    matrix_RHS_to_ca[label_l[q][0]-1] -= label_l[q][1]*lp_s*(res[label_l[q][2]]-res[label_l[q][3]])
                    print("....................................",matrix_RHS_to_ca,res[label_c[p][0]-1])
            a = np.array(matrix_nodes_to_ca);
            b = np.array(matrix_RHS_to_ca);
            #print(b)
            res = np.linalg.solve(a,b);
            print(res)
            matrix_res.append(res[NumnodeS+1]);
            matrix_t.append(t);
            for p in range(0,len(label_c)):
                matrix_RHS_to_ca[label_c[p][0]-1] = 0
            for q in range(0,len(label_l)):
                matrix_RHS_to_ca[label_l[q][0]-1] = 0
        plt.plot(matrix_t,matrix_res) # pyplot.plot()
        plt.show();

        #print("matrix_res",matrix_res);


    else:
        print('the cube of RHS for caculate:');
        for i in range(0,NumnodeS+extra_branch-1):
            print(matrix_RHS_to_ca[i], end=' ');
        print('\n');
        print("the cube of the circuit to caculate:")
        for i in range(0,NumnodeS+extra_branch-1):
            for j in  range(0,NumnodeS+extra_branch-1):
                print(matrix_nodes_to_ca[i][j], end=' ');
            print('\n');

        a = np.array(matrix_nodes_to_ca);
        b = np.array(matrix_RHS_to_ca);
        res = np.linalg.solve(a,b);
        print(res);



##################################################################################################
# option
##################################################################################################
def option():
    label = 0
    if len(info_control_commands):
        for key in info_control_commands:
            if key=='.option':
                if find_index_of_str(info_control_commands[key],'be'):
                    label = 0
                if find_index_of_str(info_control_commands[key],'de'):
                    label = 1
                if find_index_of_str(info_control_commands[key],'tr'):
                    label = 2
    return label
##################################################################################################
# main
##################################################################################################

def main():
        get_input();
        NumnodeS = draw();
        cube_ready(NumnodeS);
        caclulater(NumnodeS);


#################################################################################################
#GUI
#################################################################################################
class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    def set_init_window(self):
        self.init_window_name.title("王业伟的hspice")
        self.init_window_name.geometry('1068x681+10+10')
        self.init_data_label = Label(self.init_window_name, text="netlist")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=35)
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="输出", bg="lightblue", width=10,command=self.do)
        self.str_trans_to_md5_button.grid(row=1, column=11)

    def do(self):
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        with open('text3.txt','w') as f:
            f.write(self.init_data_Text.get(1.0,END));
        f.close();
        self.result_data_Text.delete(1.0,END)
        self.result_data_Text.insert(1.0,info_node)

def gui_start():
    init_window = Tk()
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()


#gui_start()

main()





