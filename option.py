import ver
import nm
def option(info_control_commands):
    label = 0
    if len(info_control_commands):
        for key in info_control_commands:
            if key=='.option':
                if find_index_of_str(info_control_commands[key],'be'):
                    label = 0
                if find_index_of_str(info_control_commands[key],'fe'):
                    label = 1
                if find_index_of_str(info_control_commands[key],'tr'):
                    label = 2
    return label


def find_index_of_str(s1, s2):
    lt=s1.split(s2,1)
    if len(lt)==1:
        return False
    return True


def tran(info_control_commands):
    if len(info_control_commands):
        for key in info_control_commands:
            if key=='.tran':
                step = float(info_control_commands[key].step)
                stop = float(info_control_commands[key].stop)
                start = float(info_control_commands[key].start)
                ver.lp_s = int((stop-start)/step);
                ver.te = step
                ver.t_start = start
            if key == '.plot':
                print('plot')
                tmp = info_control_commands[key].list
                str_list = tmp.split()
                ver.info_plot=str_list

            if key == '.dc':
                step = float(info_control_commands[key].step)
                end = float(info_control_commands[key].end)
                start = float(info_control_commands[key].start)
                ver.matrix_dc = [info_control_commands[key].control,start,end,step]
                ver.te = float(info_control_commands[key].step)
                ver.lp_s = int((end-start)/step)
