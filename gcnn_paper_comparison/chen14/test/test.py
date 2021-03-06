import sys
sys.path.append('../../../moleprop/util')
import workflow as wf
import pandas as pd
import statistics as stat

M = 3  # number of tests we need to do

args = [
{"nb_epoch":200,
        "n_tasks":1,
        "batch_size": 8,
        "graph_conv_layers":[64,64],
        "dense_layer_size":128,
        "learning_rate":0.005,
        "mode":'regression'},
{"nb_epoch":200,
        "n_tasks":1,
        "batch_size": 8,
        "graph_conv_layers":[64,64],
        "dense_layer_size":256,
        "learning_rate":0.005,
        "mode":'regression'},
{'nb_epoch': 200, 
'learning_rate': 0.0005, 
'dropout': 0.0, 
'graph_conv_layers': [64, 64], 
'batch_size': 8, 
'mode': 'regression', 
'n_tasks': 1, 
'dense_layer_size': 512}
]
{'nb_epoch': 100, 'learning_rate': 0.0005, 'dropout': 0.0, 'graph_conv_layers': [64, 64], 'batch_size': 32, 'mode': 'regression', 'n_tasks': 1, 'dense_layer_size': 128}

scores_all = {'RMSE':[], 'MAE':[], 'R2':[], 'AAD':[]}
for i in range(M):
    print("==========Hyperparameter==========")
    print(args[i])
    scores,pred,test_set = wf.Run.custom_validation(train_dataset = '../optimization/train_'+str(i)+'.csv',
                                                     test_dataset = '../optimization/test_'+str(i)+'.csv',
                                                     model = 'GC', 
                                                     model_args = args[i],
                                                     metrics = ['MAE','RMSE','R2','AAD'])
    for key in scores_all:
        scores_all[key].append(scores[key])
    std = test_set['flashpoint'].std()
    txt = {
           "RMSE":scores['RMSE'],
           "R2":scores['R2'],
           "MAE":scores['MAE'],
           "AAD":scores['AAD'],
           "RMSE/std":scores['RMSE']/std}
    print("About to make parity plot for test ", i)
    p_name = "parity_"+str(i)
    d_name = "parity_plot_"+str(i)
    wf.Plotter.parity_plot(pred,test_set, plot_name = p_name,dir_name = d_name, text = txt)

    print("About to make residual plot for test ", i)
    r_name = "residual_"+str(i)
    d_name = "residual_plot_"+str(i)
    wf.Plotter.residual_histogram(pred,test_set, plot_name = r_name,dir_name = d_name, text = txt)

scores_mean = {'RMSE':stat.mean(scores_all['RMSE']), 
               'MAE':stat.mean(scores_all['MAE']), 
               'R2':stat.mean(scores_all['R2']), 
               'AAD':stat.mean(scores_all['AAD'])}
scores_std = {'RMSE':stat.stdev(scores_all['RMSE']),
               'MAE':stat.stdev(scores_all['MAE']),
               'R2':stat.stdev(scores_all['R2']),
               'AAD':stat.stdev(scores_all['AAD'])}
file = open('Final_test_result.txt', 'w')
for key in scores_mean:
    s = "mean of " + key + " = " + str(scores_mean[key]) + "\n"
    s += "std of " + key + " = " + str(scores_std[key]) + "\n\n"
    file.write(s)
file.close()
