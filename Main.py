# requirements matpoltlib
import Common_Function as cf
import Configuration as conf

# create required directory.
cf.createDirectory()

# Parses ping files and fetches consecutive ping drops records.
for i in conf.File_Names:
   cf.Ping_Parser(conf.Input_File_Directory + '/' + i, conf.Log_Directory + '/' + conf.Output_Files + '/' + i)

# parses ping files and plot latency v/s time graph.
for i in conf.File_Names:
    cf.Latency_vs_Time(conf.Input_File_Directory + '/' + i, conf.Log_Directory + '/' + conf.Image_Directory + '/' + i.split('.')[0] + '.png')

#parses output of Ping_Parser function and plot histogram.
for i in conf.File_Names:
    cf.Histogram_Plot(conf.Log_Directory + '/' + conf.Output_Files + '/' + i, conf.Log_Directory + '/' + conf.Histogram_Plot + '/' + i, conf.Log_Directory + '/' + conf.Histogram_Plot + '/' + i.split('.')[0] + '.png')
