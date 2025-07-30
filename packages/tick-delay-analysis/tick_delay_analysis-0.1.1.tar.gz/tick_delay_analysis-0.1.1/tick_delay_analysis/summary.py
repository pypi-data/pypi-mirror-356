import pandas as pd
import numpy as np
import glob
import os

def mean_time_diff_calc(file_path, SZ_time_diff_bracket, CYB_time_diff_bracket, SH_time_diff_bracket):
    input_file = pd.read_csv(file_path)
    input_file['row_name'] = range(1, len(input_file) + 1)
    stock_code = os.path.basename(file_path)
        
    time_tick_reference = input_file[input_file['row_name'] <= 32].copy()
    input_file['mean_time_diff'] = pd.to_numeric(input_file['mean_time_diff'], errors = 'coerce')
    input_file['row_name'] = pd.to_numeric(input_file['row_name'], errors = 'coerce')
    
    if (stock_code[0] == '0'):
        SZ_time_diff_bracket.append(input_file[input_file['row_name'] <= 32])
    elif (stock_code[0] == '3'):
        CYB_time_diff_bracket.append(input_file[input_file['row_name'] <= 32])
    else:
        SH_time_diff_bracket.append(input_file[input_file['row_name'] <= 32])
    return (SZ_time_diff_bracket, CYB_time_diff_bracket, SH_time_diff_bracket, time_tick_reference)

def summarize_all(input_folder):
    input_files = glob.glob(os.path.join(input_folder, "*.csv"))
    
    SZ_time_diff_bracket = []
    CYB_time_diff_bracket = [] 
    SH_time_diff_bracket = []
    # Append row names to each file
    for file_path in input_files:
        
        (SZ_time_diff_bracket, 
         CYB_time_diff_bracket, 
         SH_time_diff_bracket, 
         time_tick_reference) = mean_time_diff_calc(file_path, SZ_time_diff_bracket, 
                                                    CYB_time_diff_bracket, SH_time_diff_bracket)
        
    SZ_bracket = pd.concat(SZ_time_diff_bracket, ignore_index = True)
    CYB_bracket = pd.concat(CYB_time_diff_bracket, ignore_index = True)
    SH_bracket = pd.concat(SH_time_diff_bracket, ignore_index = True)
    # print(all_bracket)
    
    SZ_categorized_mean = SZ_bracket.groupby('row_name')['mean_time_diff'].mean().reset_index()
    CYB_categorized_mean = CYB_bracket.groupby('row_name')['mean_time_diff'].mean().reset_index()
    SH_categorized_mean = SH_bracket.groupby('row_name')['mean_time_diff'].mean().reset_index()
    
    SZ_categorized_mean.rename(columns = {'mean_time_diff': 'SZ_mean_time_diff'}, inplace = True)
    CYB_categorized_mean.rename(columns = {'mean_time_diff': 'CYB_mean_time_diff'}, inplace = True)
    SH_categorized_mean.rename(columns = {'mean_time_diff': 'SH_mean_time_diff'}, inplace = True)
    # print(SZ_categorized_mean)
    # print(CYB_categorized_mean)
    # print(SH_categorized_mean)
    
    SZ_full_df = pd.merge(time_tick_reference, SZ_categorized_mean, on = 'row_name', how = 'inner')
    SZ_CYB_full_df = pd.merge(SZ_full_df, CYB_categorized_mean, on = 'row_name', how = 'inner')
    all_full_df = pd.merge(SZ_CYB_full_df, SH_categorized_mean, on = 'row_name', how = 'inner')
    output_df = all_full_df[['type', 'time_interval_start', 'SZ_mean_time_diff', 'CYB_mean_time_diff', 'SH_mean_time_diff']]
    
    output_path = f"{input_folder}/Statistics_Summary.csv"
    output_df.to_csv(output_path, index = False)
    # print(time_tick_reference)
    # print(categorized_mean)

    # time_diff_0 = []
    # time_diff_3 = []
    # time_diff_6 = []
    
    # for file_path in input_files:
    #     input_file = pd.read_csv(file_path)
    #     input_file["row_number"] = range(1, len(input_file) + 1)
    #     stock_code = os.path.basename(file_path)
    #     if stock_code[0] == "0":
    #         cons_time_diff_0 = mean_time_diff_calc(input_file)
    #         time_diff_0.append(cons_time_diff_0)
    #     elif stock_code[0] == "3":
    #         cons_time_diff_3 = mean_time_diff_calc(input_file)
    #         time_diff_3.append(cons_time_diff_3)
    #     else:
    #         cons_time_diff_6 = mean_time_diff_calc(input_file)
    #         time_diff_6.append(cons_time_diff_6)
    
    # pd_time_diff_0 = pd.DataFrame(time_diff_0, columns = ["time_diff_0"])
    # pd_time_diff_3 = pd.DataFrame(time_diff_3, columns = ["time_diff_3"])
    # pd_time_diff_6 = pd.DataFrame(time_diff_6, columns = ["time_diff_6"])
    
    # mean_time_diff_0 = pd_time_diff_0.dropna(subset = ["time_diff_0"]).mean()
    # mean_time_diff_3 = pd_time_diff_3.dropna(subset = ["time_diff_3"]).mean()
    # mean_time_diff_6 = pd_time_diff_6.dropna(subset = ["time_diff_6"]).mean()
    
    # output_df = pd.DataFrame({
    #     "深交所股票6月17日平均交易延迟:": mean_time_diff_0,
    #     "创业板股票6月17日平均交易延迟:": mean_time_diff_3,
    #     "上交所股票6月17日平均交易延迟:": mean_time_diff_6
    # })
    # output_df.to_csv("/Users/eric_p/Desktop/Summer 2025/Internship/Data/Ticks_Results_20250617/Statistics_Summary.csv", index = False)
    