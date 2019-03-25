#coding:utf-8
import bisect
import struct
from tkinter import *
import numpy as np

list = []; #the oringin list to store the information
list_content = [];   #proceed input information
str = '';  # a string to store the information from every lines
info_node = {};  # a list to store every nodes and label
NumnodeS = 0;   #number of nodes
info_control_commands = {}; # information of every control command
matrix = [[[0 for j in range(10)] for j in range(1000)] for i in range(1000)];   #the matrix that store the circuit
conversion = {'f':10**-15,'p':10**-12,'n':10**-9,'u':10**-6,'m':10**-3,'k':10**3,'meg':10**6,'g':10**9,'t':10**12}#unit conversion
matrix_nodes = [[0 for j in range(1000)] for i in range(1000)];
matrix_source_controled = [[0 for j in range(100)] for i in range(100)];
matrix_V = [0 for j in range(10)];
matrix_I = [0 for j in range(10)];
matrix_MNA = [[0 for j in range(100)] for i in range(100)];

with open('text2.txt','r') as f:
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
                    for j in range(1,len(list_content[i])):
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
                        for j in range(5,len(list_content[i])):
                            list_content[i][4] += list_content[i][j];
                        elem = Source('v',list_content[i][1],list_content[i][2],list_content[i][3],list_content[i][4]);
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                    else:
                        for j in range(4,len(list_content[i])):
                            list_content[i][3] += list_content[i][j];
                        elem = Source('v',list_content[i][1],list_content[i][2],0,list_content[i][3]);
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;

                elif(tmp=='i'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    if(is_number(list_content[i][3][0])==True):
                        if(len(list_content[i])>4):
                            for j in range(5,len(list_content[i])):
                                list_content[i][4] += list_content[i][j];
                            elem = Source('i',list_content[i][1],list_content[i][2],list_content[i][3],list_content[i][4]);
                        else:
                            elem = Source('i',list_content[i][1],list_content[i][2],list_content[i][3],'');
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                    else:
                        for j in range(4,len(list_content[i])):
                            list_content[i][3] += list_content[i][j];
                        elem = Source('i',list_content[i][1],list_content[i][2],0,list_content[i][3]);
                        matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;


                elif(tmp=='r'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Element('r',list_content[i][1],list_content[i][2],list_content[i][3]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                if(tmp=='c'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Element('c',list_content[i][1],list_content[i][2],list_content[i][3]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                if(tmp=='l'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Element('l',list_content[i][1],list_content[i][2],list_content[i][3]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;
                if(tmp=='g'):
                    k = 0;
                    while matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]!=0:
                        k = k+1;
                    elem = Source_controled('g',list_content[i][1],list_content[i][2],list_content[i][3],list_content[i][4],list_content[i][5]);
                    matrix[info_node[list_content[i][1]]][info_node[list_content[i][2]]][k]=elem;


##########################################################################################################################################
# prepare for the cubes
##########################################################################################################################################

def cube_ready(NumnodeS):
    print(NumnodeS);
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
                    print(tmp.ID,'TMP.ID');
                    if(tmp.ID=='r'):
                        matrix_nodes[i][j] -= 1/float(tmp.value);
                    if(tmp.ID=='g'):
                        for p in range(0,NumnodeS):
                            for q in  range(0,NumnodeS):
                                if((p==info_node[tmp.node1] and q==info_node[tmp.node_control1]) or (p==info_node[tmp.node2] and q==info_node[tmp.node_control2])):
                                    matrix_source_controled[p][q] += int(tmp.value);
                                    #print(p,q,matrix_source_controled[p][q]);
                                elif((p==info_node[tmp.node2] and q==info_node[tmp.node_control1]) or (p==info_node[tmp.node1] and q==info_node[tmp.node_control2])):
                                    matrix_source_controled[p][q] -= int(tmp.value);
                                    #print(p,q,matrix_source_controled[p][q]);
                    if(tmp.ID=='g'):
                        for p in range(0,NumnodeS):
                            for q in  range(0,NumnodeS):
                                if((p==info_node[tmp.node1] and q==info_node[tmp.node_control1]) or (p==info_node[tmp.node2] and q==info_node[tmp.node_control2])):
                                    matrix_source_controled[p][q] += int(tmp.value);
                                    #print(p,q,matrix_source_controled[p][q]);
                                elif((p==info_node[tmp.node2] and q==info_node[tmp.node_control1]) or (p==info_node[tmp.node1] and q==info_node[tmp.node_control2])):
                                    matrix_source_controled[p][q] -= int(tmp.value);
                                    #print(p,q,matrix_source_controled[p][q]);
                    if(tmp.ID=='i'):
                        if(tmp.ID=='i'):
                            matrix_I[info_node[tmp.node1]] -= int(tmp.value);
                            matrix_I[info_node[tmp.node2]] += int(tmp.value);
                        print("GOT current");
                    k = k+1;
            if(matrix[j][i][0]!=0):
                k = 0;
                while(matrix[j][i][k]!=0 and k<10):
                    tmp = matrix[j][i][k];
                    if(tmp.ID=='r'):
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
    print('the cube of I:');
    for i in  range(0,NumnodeS):
        print(matrix_I[i], end=' ');
    print('\n');

##################################################################################################
# START TO CACULATE
##################################################################################################
def caclulater(NumnodeS):
    gnd = int(info_node['0']);
    print("START TO CACULATE",gnd);
    matrix_I_to_ca = matrix_I[:gnd]+matrix_I[gnd+1:NumnodeS];
    matrix_nodes_to_ca = matrix_nodes[:gnd]+matrix_nodes[gnd+1:NumnodeS];
    for i in range(0,NumnodeS-1):
        matrix_nodes_to_ca[i]=matrix_nodes_to_ca[i][:gnd]+matrix_nodes_to_ca[i][gnd+1:NumnodeS];
    print('the cube of I for caculate:');
    for i in range(0,NumnodeS-1):
        print(matrix_I_to_ca[i], end=' ');
    print('\n');
    print("the cube of the circuit to caculate:")
    for i in range(0,NumnodeS-1):
        for j in  range(0,NumnodeS-1):
            print(matrix_nodes_to_ca[i][j], end=' ');
        print('\n');

    a = np.array(matrix_nodes_to_ca);
    b = np.array(matrix_I_to_ca);
    res = np.linalg.solve(a,b);
    print(res);




##################################################################################################
# main
##################################################################################################

def main():
        get_input();
        NumnodeS = draw();
        cube_ready(NumnodeS);
        caclulater(NumnodeS);
        print(info_node);
        print(info_control_commands);

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





