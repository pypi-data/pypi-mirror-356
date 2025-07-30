import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from concurrent.futures import ProcessPoolExecutor

# input_path = "/Users/eric_p/Desktop/Summer 2025/Internship/Data/Trading_Time_Analysis /000001.SZ.csv"
# input_data = pd.read_csv(input_path)
# Parse the integer time into pd.timeStamp
def parse_time(time_code):
    code = time_code.astype(int).astype(str).str.zfill(9)
    hour = code.str[0:2]
    minute = code.str[2:4]
    second = code.str[4:6]
    millisecond = code.str[6:9]
    datetime_str = (
        '2025-06-17 ' + hour + ':' + minute + ':' + second + '.' + millisecond
    )
    return pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M:%S.%f')

def input_file_process(input_path, output_folder):
    if (os.path.getsize(input_path) == 0):
        print("Empty file is detected!")
        return
    else: 
        print(input_path)
        input_data = pd.read_csv(input_path)

        # Rename the first three columns to make it easier to read
        input_data.rename(columns = {
            "time1": "item",
            "time2": "Time1",
            "price": "Time2"
        }, inplace = True)
        
        # Sort the data
        input_data['Time1'] = pd.to_numeric(input_data['Time1'], errors = 'coerce')
        input_data['Time2'] = pd.to_numeric(input_data['Time2'], errors = 'coerce')
        input_data.sort_values(by = ['Time1'], inplace = True)
        
        # Extract all "t" rows and transform t Time to timeStamp
        t_rows = input_data[input_data['item'] == 't'].copy()
        # Extract all "o" rows and transform o Time to timeStamp
        o_rows = input_data[input_data['item'] == 'o'].copy()
        
        # Check if the stock stops trading on that day
        if (t_rows.empty & o_rows.empty):
            print("该股市今日停牌，不计入统计！") # If so, return directly
            return
        
        t_rows['time1_dt'] = parse_time(t_rows['Time1'])
        t_rows['time2_dt'] = parse_time(t_rows['Time2'])
        t_rows.dropna(subset = ['time1_dt', 'time2_dt'], inplace = True)
        
        o_rows['time1_dt'] = parse_time(o_rows['Time1'])
        o_rows['time2_dt'] = parse_time(o_rows['Time2'])
        o_rows.dropna(subset = ['time1_dt', 'time2_dt'], inplace = True)

        # # Transfer time to numerics
        # t_rows['Time1'] = pd.to_numeric(t_rows['Time1'], errors = 'coerce')
        # t_rows['Time2'] = pd.to_numeric(t_rows['Time2'], errors = 'coerce')

        # Calculate the difference between consecutive rows for t rows
        t_rows['time1_diff'] = t_rows['Time1'].diff()
        t_rows['time2_diff'] = t_rows['Time2'].diff()
        t_rows['time_diff'] = t_rows['Time2'] - t_rows['Time1'] 
        
        # Calculate the difference between consecutive rows for o rows
        o_rows['time1_diff'] = o_rows['Time1'].diff()
        o_rows['time2_diff'] = o_rows['Time2'].diff()
        o_rows['time_diff'] = o_rows['Time2'] - o_rows['Time1'] 
        
        # Calculate the record time difference for t rows
        t_rows['record_diff'] = (t_rows['time2_dt'] - t_rows['time1_dt'])
        t_rows_time_earliest = t_rows['Time1'].min()
        if (t_rows_time_earliest > 93500000):
            print("t行统计开始时间大于9:35, 暂时不做讨论。")
            return
        
        if (t_rows_time_earliest < 93000000):
            t_rows_time_earliest = 93000000
        t_rows_no_pre = t_rows[(t_rows['Time1'] >= 93000000) & 
                               (t_rows['Time1'] <= (t_rows_time_earliest + 600000))].copy()
        
        # Calculate the record time difference for o rows
        o_rows['record_diff'] = (o_rows['time2_dt'] - o_rows['time1_dt'])
        o_rows_time_earliest = o_rows['Time1'].min()
        if (o_rows_time_earliest > 93500000):
            print("o行统计开始时间大于9:35, 暂时不做讨论。")
            return
        
        if (o_rows_time_earliest < 93000000):
            o_rows_time_earliest = 93000000
        o_rows_no_pre = o_rows[(o_rows['Time1'] >= 93000000) & 
                               (o_rows['Time1'] <= (o_rows_time_earliest + 600000))].copy()
        
        def t_time_diff(window1, window2):
            # Set the start_time and end_time for the plot
            start_time = t_rows_no_pre['time1_dt'].min()
            one_min_stop = t_rows_no_pre['Time1'].min() + 100000
            five_min_stop = t_rows_no_pre['Time1'].min() + 600000
            one_min_stop = f"{int(one_min_stop):09d}"
            five_min_stop = f"{int(five_min_stop):09d}"
            one_min_stop_time = ('2025-06-17 ' + one_min_stop[0:2] + ":" + one_min_stop[2:4] +
                                 ":" + one_min_stop[4:6] + "." + one_min_stop[6:9])
            five_min_stop_time = ('2025-06-17 ' + five_min_stop[0:2] + ":" + five_min_stop[2:4] +
                                 ":" + five_min_stop[4:6] + "." + five_min_stop[6:9])
            one_min_stop = pd.to_datetime(one_min_stop_time, format='%Y-%m-%d %H:%M:%S.%f')
            five_min_stop = pd.to_datetime(five_min_stop_time, format='%Y-%m-%d %H:%M:%S.%f')

            if (start_time != pd.NaT):
                # Cut the whole trading time into intervals of several seconds
                time_bins_1 = pd.interval_range(start = start_time, end = one_min_stop, 
                                            freq = pd.Timedelta(milliseconds = window1), 
                                            closed = 'left')
                
                time_bins_2 = pd.interval_range(start = one_min_stop, end = five_min_stop, 
                                            freq = pd.Timedelta(milliseconds = window2), 
                                            closed = 'left')
                
                # Assign bins for both intervals
                t_rows_no_pre['bin1'] = pd.cut(t_rows_no_pre['time1_dt'], bins=time_bins_1)
                t_rows_no_pre['bin2'] = pd.cut(t_rows_no_pre['time1_dt'], bins=time_bins_2)

                # Calculate the average time difference for first kind of window
                part1 = t_rows_no_pre.groupby('bin1').agg(
                    avg_diff_ms=('record_diff', lambda x: x.mean().total_seconds() * 1000)
                ).reset_index()
                part1['window_start'] = part1['bin1'].apply(lambda x: x.left)

                # Calculate the average time difference for second kind of window
                part2 = t_rows_no_pre.groupby('bin2').agg(
                    avg_diff_ms=('record_diff', lambda x: x.mean().total_seconds() * 1000)
                ).reset_index()
                part2['window_start'] = part2['bin2'].apply(lambda x: x.left)

                # Concatenate the two results
                t_time_diff_df = pd.concat([part1[['window_start', 'avg_diff_ms']],
                                    part2[['window_start', 'avg_diff_ms']]], ignore_index=True)
                t_time_diff_df['item'] = 't'
                
            return t_time_diff_df
        
        def o_time_diff(window1, window2):
            # Set the start_time and end_time for the plot
            start_time = o_rows_no_pre['time1_dt'].min()
            one_min_stop = t_rows_no_pre['Time1'].min() + 100000
            five_min_stop = t_rows_no_pre['Time1'].min() + 600000
            one_min_stop = f"{int(one_min_stop):09d}"
            five_min_stop = f"{int(five_min_stop):09d}"
            one_min_stop_time = ('2025-06-17 ' + one_min_stop[0:2] + ":" + one_min_stop[2:4] +
                                 ":" + one_min_stop[4:6] + "." + one_min_stop[6:9])
            five_min_stop_time = ('2025-06-17 ' + five_min_stop[0:2] + ":" + five_min_stop[2:4] +
                                 ":" + five_min_stop[4:6] + "." + five_min_stop[6:9])
            one_min_stop = pd.to_datetime(one_min_stop_time, format='%Y-%m-%d %H:%M:%S.%f')
            five_min_stop = pd.to_datetime(five_min_stop_time, format='%Y-%m-%d %H:%M:%S.%f')

            if (start_time != pd.NaT):
                # Cut the whole trading time into intervals of several seconds
                time_bins_1 = pd.interval_range(start = start_time, end = one_min_stop, 
                                            freq = pd.Timedelta(milliseconds = window1), 
                                            closed = 'left')
                
                time_bins_2 = pd.interval_range(start = one_min_stop, end = five_min_stop, 
                                            freq = pd.Timedelta(milliseconds = window2), 
                                            closed = 'left')
                
                # Assign bins for both intervals
                o_rows_no_pre['bin1'] = pd.cut(o_rows_no_pre['time1_dt'], bins=time_bins_1)
                o_rows_no_pre['bin2'] = pd.cut(o_rows_no_pre['time1_dt'], bins=time_bins_2)
                
                # Calculate the average time difference for first kind of window
                part1 = o_rows_no_pre.groupby('bin1').agg(
                    avg_diff_ms=('record_diff', lambda x: x.mean().total_seconds() * 1000)
                ).reset_index()
                part1['window_start'] = part1['bin1'].apply(lambda x: x.left)
                
                # Calculate the average time difference for second kind of window
                part2 = o_rows_no_pre.groupby('bin2').agg(
                    avg_diff_ms=('record_diff', lambda x: x.mean().total_seconds() * 1000)
                ).reset_index()
                part2['window_start'] = part2['bin2'].apply(lambda x: x.left)

                # Concatenate the two results
                o_time_diff_df = pd.concat([part1[['window_start', 'avg_diff_ms']],
                                    part2[['window_start', 'avg_diff_ms']]], ignore_index=True)
                o_time_diff_df['item'] = 'o'
            return o_time_diff_df
        
        t_time_diff_df = t_time_diff(window1 = 10000, window2 = 30000)
        o_time_diff_df = o_time_diff(window1 = 10000, window2 = 30000)
        time_diff_df = pd.concat([t_time_diff_df, o_time_diff_df])

        # # output_path = "/Users/eric_p/Desktop/Summer 2025/Internship/Data/Trading_Time_Analysis /000001.SZ-o.csv"
        # # t_rows.to_csv(output_path, index = False)
        # def time1_diff_plot(t_rows):
        #     # Difference visualization
        #     plt.plot(t_rows['time1_diff'], label = 'time1_diff', color = 'green')
        #     plt.title("time1_diff over time")
        #     plt.xlabel("Index")
        #     plt.ylabel("Difference")
        #     plt.grid(True)
        #     plt.legend()
        #     plt.show()

        # def time2_diff_plot(t_rows):
        #     plt.plot(t_rows['time2_diff'], label = 'time2_diff', color = 'orange')
        #     plt.title("time2_diff over time")
        #     plt.xlabel("Index")
        #     plt.ylabel("Difference")
        #     plt.grid(True)
        #     plt.legend()
        #     plt.show()

        # def start_time_diff_plot(window, title):
        #     # Machine starting time difference
        #     # Set the start_time and end_time for the plot
        #     start_time = t_rows_no_pre['time1_dt'].min()
        #     end_time = t_rows_no_pre['time1_dt'].max()

        #     # Cut the whole trading time into intervals of several seconds
        #     time_bins = pd.interval_range(start = start_time, end = end_time, 
        #                                 freq = pd.Timedelta(milliseconds = window), 
        #                                 closed = 'left')
        #     t_rows_no_pre['bin'] = pd.cut(t_rows_no_pre['time1_dt'], bins = time_bins)

        #     # Calculate the average time difference in each window
        #     time_diff_df = t_rows_no_pre.groupby('bin').agg(
        #         avg_diff_ms=('record_diff', lambda x: x.mean().total_seconds() * 1000)
        #     ).reset_index()

        #     # Get the x-axis for the figure
        #     time_diff_df['window_start'] = time_diff_df['bin'].apply(lambda x: x.left)

        #     plt.plot(time_diff_df['window_start'], time_diff_df['avg_diff_ms'], marker='o', 
        #             color='blue')
        #     plt.title(title)
        #     plt.xlabel("Time")
        #     plt.ylabel("Average Starting Time Difference")
        #     plt.grid(True)
        #     plt.legend()
        #     for (x, y) in zip(time_diff_df['window_start'], time_diff_df['avg_diff_ms']): # Pair the x and y values for each data point
        #         label = f"{y:.0f}ms"
        #         plt.text(x, y + 150, label, fontsize = 6, ha = 'center', va = 'bottom') 
        #     plt.show()
            
        #     return time_diff_df

        # time_diff_df = start_time_diff_plot(window = 10000, 
                            #title = "Average Time Difference For 10-second Intervals: 000001.SZ-t")

        # # 如果交易太密集，延迟容易高，因此我们筛选掉交易太密集的交易，选择比较稀疏的段落
        # t_rows_no_pre_2 = t_rows[(t_rows['Time1'] >= 93000000)].copy()
        # t_rows_sparse = t_rows_no_pre_2[t_rows_no_pre_2['time1_diff'] >= 100]

        # # 计算稀疏时间段的时间差均值
        # start_time_diff = t_rows_sparse['record_diff'].mean()

        # # Visualize start_time_diff
        # def timedelta_to_int(tdelta):
        #     total_ms = int(tdelta.total_seconds() * 1000)
        #     hours = total_ms // 3600000
        #     minutes = (total_ms % 3600000) // 60000
        #     seconds = (total_ms % 60000) // 1000
        #     milliseconds = total_ms % 1000
        #     return int(f"{hours:02d}{minutes:02d}{seconds:02d}{milliseconds:03d}")
        # t_rows_no_pre['record_diff_converted'] = t_rows_no_pre['record_diff'].apply(timedelta_to_int)

        # plt.plot(t_rows_no_pre['record_diff_converted'], label = 'start_time_diff', color = 'blue')
        # plt.title("starting time difference on two sides")
        # plt.xlabel("Index")
        # plt.ylabel("Difference")
        # plt.grid(True)
        # plt.legend()
        # plt.show()

        # print(f'本地机器比交易所机器开始记录时间要慢: {start_time_diff} 毫秒')

        # Organize all data and output them into a single csv file
        output_df = pd.DataFrame({
            'type': time_diff_df['item'],
            'time_interval_start': time_diff_df['window_start'],
            'mean_time_diff': time_diff_df['avg_diff_ms']
        })
        print(output_df)
        stock_code = os.path.basename(input_path)
        output_path = f"{output_folder}/{stock_code}"
        output_df.to_csv(output_path, index = False)

def process_all(input_folder, output_folder):
    # Load all input files
    input_paths = glob.glob(os.path.join(input_folder, "*.csv"))
        
    for input_path in input_paths:
        input_file_process(input_path, output_folder)
    # input_path = "/Users/eric_p/Desktop/Summer 2025/Internship/Data/Ticks/002048.SZ.csv"
    # input_file_process(input_path)