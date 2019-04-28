list = []  #the oringin list to store the information
list_content = []    #proceed input information
str = ''   # a string to store the information from every lines
info_node = {}   # a list to store every nodes and label
info_branch = {}
NumnodeS = 0    #number of nodes
info_control_commands = {}  # information of every control command
matrix = [[[0 for j in range(10)] for j in range(1000)] for i in range(1000)]    #the matrix that store the circuit
matrix_nodes = [[0 for j in range(1000)] for i in range(1000)]
matrix_source_controled = [[0 for j in range(100)] for i in range(100)]
matrix_V = [0 for j in range(10)]
matrix_RHS = [0 for j in range(20)]
matrix_RHS_fff = []
label_c = []
label_l = []
label_dio = []
label_mos = []
res = 0;
matrix_dc = []
info_plot = []
t_start = 0;
lp_s = 1000
te = 0.01
num_branch = 0
conversion = {'f':10**-15,'p':10**-12,'n':10**-9,'u':10**-6,'m':10**-3,'k':10**3,'meg':10**6,'g':10**9,'t':10**12}#unit conversion
class Element:
    def __init__(self,id,u,v,s):
        self.ID = id
        self.node1 = u
        self.node2 = v
        self.value = s

class cElement:
    def __init__(self,id,u,v,s,ic):
        self.ID = id
        self.node1 = u
        self.node2 = v
        self.value = s
        self.ic = ic

class Source:
    def __init__(self,id,u,v,s,a):
        self.ID = id
        self.node1 = u
        self.node2 = v
        self.value = s
        self.oth = a

class Source_controled:
    def __init__(self,id,u,v,p,q,s):
        self.ID = id
        self.node1 = u
        self.node2 = v
        self.node_control1 = p
        self.node_control2 = q
        self.value = s
class diode:
    def __init__(self,id,u,v,ty):
        self.ID = id
        self.node1 = u
        self.node2 = v
        self.type = ty
        self.value = ty


class Source_controled_fh:
    def __init__(self,id,u,v,c,s):
        self.ID = id
        self.node1 = u
        self.node2 = v
        self.cl = c
        self.value = s

class Control:
    def __init__(self,op,control):
        self.command = op
        self.oth = control

class tran:
    def __init__(self,tran,a,b,c):
        self.tran = tran;
        self.step = a
        self.stop = b
        self.start = c

class plot:
    def __init__(self,plot,a,b):
        self.commannd = plot
        self.tran = a
        self.list = b

class mos:
    def __init__(self,id,nd,ng,ns,nb,mna,l,w):
        self.ID = id
        self.d = nd
        self.g = ng
        self.s = ns
        self.b = nb
        self.mname = mna
        self.l = l
        self.w = w

class dc:
    def __init__(self,dc,con,start,end,step):
        self.command = dc
        self.control = con
        self.start = start
        self.end = end
        self.step = step

def init():
    list = []  #the oringin list to store the information
    list_content = []    #proceed input information
    str = ''   # a string to store the information from every lines
    info_node = {}   # a list to store every nodes and label
    info_branch = {}
    NumnodeS = 0    #number of nodes
    info_control_commands = {}  # information of every control command
    matrix = [[[0 for j in range(10)] for j in range(1000)] for i in range(1000)]    #the matrix that store the circuit
    conversion = {'f':10**-15,'p':10**-12,'n':10**-9,'u':10**-6,'m':10**-3,'k':10**3,'meg':10**6,'g':10**9,'t':10**12}#unit conversion
    matrix_nodes = [[0 for j in range(1000)] for i in range(1000)]
    matrix_source_controled = [[0 for j in range(100)] for i in range(100)]
    matrix_V = [0 for j in range(10)]
    matrix_RHS = [0 for j in range(20)]
    matrix_RHS_fff = []
    lp_s = 100
    T = 10
    num_branch = 0
    label_c = []
    label_l = []
    label_dio = []
    res = 0;
