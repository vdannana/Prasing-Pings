import datetime as dt
import os
import re

import matplotlib.dates as md
import matplotlib.pyplot as plt

import Configuration as conf

def createDirectory():
    if not os.path.exists(conf.Log_Directory):
        os.mkdir(conf.Log_Directory)
        print("Directory ", conf.Log_Directory,  " Created ")
    else:
        print("Directory ", conf.Log_Directory,  " already exists")

    if not os.path.exists(conf.Log_Directory + '/' + conf.Image_Directory):
        os.mkdir(conf.Log_Directory + '/' + conf.Image_Directory)
        print("Directory ", conf.Log_Directory + '/' + conf.Image_Directory,  " Created ")
    else:
        print("Directory ", conf.Log_Directory + '/' + conf.Image_Directory,  " already exists")

    if not os.path.exists(conf.Log_Directory + '/' + conf.Output_Files):
        os.mkdir(conf.Log_Directory + '/' + conf.Output_Files)
        print("Directory ", conf.Log_Directory + '/' + conf.Output_Files,  " Created ")
    else:
        print("Directory ", conf.Log_Directory + '/' + conf.Output_Files,  " already exists")

    if not os.path.exists(conf.Log_Directory + '/' + conf.Histogram_Plot):
        os.mkdir(conf.Log_Directory + '/' + conf.Histogram_Plot)
        print("Directory ", conf.Log_Directory + '/' + conf.Histogram_Plot,  " Created ")
    else:
        print("Directory ", conf.Log_Directory + '/' + conf.Histogram_Plot,  " already exists")


def Ping_Parser(File_Name,Output_File_Name):
    f = open(Output_File_Name, "w")
    if not os.path.exists(File_Name):
        print("File ", File_Name,  " not found.")
        return -1
    start_time = 0
    end_time = 0
    str_ping = []
    count = 0
    with open(File_Name, "r") as fi:
        for line in fi:
            x = re.search(".*Timeout.*", line.strip())
            if(x):
                str_ping.append(line)
            else:
                if(len(str_ping) >= conf.Max_Count):
                    start_time = str_ping[0].split(' ')[0] + ' ' + str_ping[0].split(' ')[1]
                    end_time = str_ping[-1].split(' ')[0] + ' ' + str_ping[-1].split(' ')[1]
                    count = len(str_ping)
                    f.write(str(count) + " packet are droped between " + str(start_time) + ' ' + str(end_time) + '\n')
                else:
                    count = 0
                    start_time = 0
                    end_time = 0
                str_ping = []
    print('Finished Parsing ' + File_Name + ' output file saved at ' + Output_File_Name)
    f.close()


def Latency_vs_Time(File_Name,Output_File_Name):
    time = []
    latency = []
    sample = False
    with open(File_Name, "r") as file:
        for line in file:
            x = re.search(".*From.*time=.*", line.strip())
            if(x):
                time.append(line.split()[0] + ' ' + line.split()[1][0:-1])
                latency.append(float(line.split()[-1][5:-2]))
    y_value = [dt.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f') for ts in time]
    datenums = md.date2num(y_value)
    plt.figure(figsize = (20,10), dpi = 80)
    ax = plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S.%f')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xlabel('Time')
    plt.ylabel('Latency')
    plt.title('Latency_vs_Time')
    plt.plot(datenums, latency)
    plt.savefig(Output_File_Name)
    plt.show()
    print('Finished ploting ' + File_Name + ' output file saved at ' + Output_File_Name)


def Histogram_Plot(File_Name, Output_File_Name, Output_Graph_Name) :
    f = open(Output_File_Name, "w")
    if not os.path.exists(File_Name):
        print("File ", File_Name,  " not found.")
        return -1
    Dictionary = {}
    with open(File_Name, "r") as fi:
        for line in fi:
            number = int(line.split()[0])
            if number in Dictionary.keys():
                Dictionary[number] +=1;
            else:
                Dictionary[number] = 1
    Plot_Graph(Dictionary, Output_Graph_Name)
    for each in sorted(Dictionary):
        f.write(str(each) + ' number of packets dropped ' + str(Dictionary[each]) + ' times\n')
    print('Finished Parsing ' + File_Name + ' output file saved at ' + Output_File_Name)
    f.close()


def Plot_Graph(Input_Dictionary,Output_File_Name):
    dict = sorted(Input_Dictionary)
    bucket_list = {}
    for i in dict:
        num = int(i/10)
        key = str(num*10) + '-' + str((num + 1) * 10)
        if key in bucket_list.keys():
            bucket_list[key] += Input_Dictionary[i]
        else:
            bucket_list[key] = Input_Dictionary[i]
    lastkey = int(list(bucket_list.keys())[-1].split('-')[1])
    final_bucket = {}
    for i in range(0, int(lastkey/10)):
        final_bucket[str(i*10) + '-' + str((i+1)*10)] = 0
    for i in bucket_list.keys():
        final_bucket[i] = bucket_list[i]
    sum_all = sum(list(final_bucket.values()))
    percentage_bucket_list = []
    for i in list(final_bucket.values()):
        percentage_bucket_list.append((i * 100)/ sum_all)
    plt.figure(figsize = (20,10), dpi = 80)
    plt.bar(list(final_bucket.keys()), percentage_bucket_list, align='center', alpha=0.5, width=1)
    for index, value in enumerate(percentage_bucket_list):
        plt.text(index, value, "{:.2f}".format(value))
    plt.ylim(0,100)
    plt.ylabel('Percentage')
    plt.xlabel('Number of packets')
    plt.title('Frequency of Packet drop')
    plt.savefig(Output_File_Name)
    plt.show()