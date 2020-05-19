# requirements matpoltlib
import Common_Function as cf
import Configuration as conf

cf.createDirectory()

for i in conf.File_Names:
   cf.Ping_Parser(conf.Input_File_Directory + '/' + i, conf.Log_Directory + '/' + conf.Output_Files + '/' + i)

for i in conf.File_Names:
    cf.Latency_vs_Time(conf.Input_File_Directory + '/' + i, conf.Log_Directory + '/' + conf.Image_Directory + '/' + i.split('.')[0] + '.png')

for i in conf.File_Names:
    cf.Histogram_Plot(conf.Log_Directory + '/' + conf.Output_Files + '/' + i, conf.Log_Directory + '/' + conf.Histogram_Plot + '/' + i, conf.Log_Directory + '/' + conf.Histogram_Plot + '/' + i.split('.')[0] + '.png')
