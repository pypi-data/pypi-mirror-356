import os
import mne
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import json

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def butter_highpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='highpass', analog=False)
    y = filtfilt(b, a, data)
    return y

def get_epoch_abs_mean(full_single_trace, sfreq, epoch_len=None):
    epoch_length = int(epoch_len * sfreq)
    n_epochs = len(full_single_trace) // epoch_length
    output = np.zeros(n_epochs)
    for index in range(n_epochs):
        data_this_epoch = np.array(
            full_single_trace[index*epoch_length: (index+1)*epoch_length]
        )
        output[index] = np.abs(data_this_epoch).mean()
    return output

def get_epoch_abs_median(full_single_trace, sfreq, epoch_len=None):
    epoch_length = int(epoch_len * sfreq)
    n_epochs = len(full_single_trace) // epoch_length
    output = np.zeros(n_epochs)
    for index in range(n_epochs):
        data_this_epoch = np.array(
            full_single_trace[index*epoch_length: (index+1)*epoch_length]
        )
        output[index] = np.median(np.abs(data_this_epoch))
    return output

def get_epoch_abs_max(full_single_trace, sfreq, epoch_len=None):
    epoch_length = int(epoch_len * sfreq)
    n_epochs = len(full_single_trace) // epoch_length
    output = np.zeros(n_epochs)
    for index in range(n_epochs):
        data_this_epoch = np.array(
            full_single_trace[index*epoch_length: (index+1)*epoch_length]
        )
        output[index] = np.abs(data_this_epoch).max()
    return output

def get_epoch_abs_std(full_single_trace, sfreq, epoch_len=None):
    epoch_length = int(epoch_len * sfreq)
    n_epochs = len(full_single_trace) // epoch_length
    output = np.zeros(n_epochs)
    for index in range(n_epochs):
        data_this_epoch = np.array(
            full_single_trace[index*epoch_length: (index+1)*epoch_length]
        )
        output[index] = np.abs(data_this_epoch).std()
    return output

def get_epoch_rms(full_single_trace, sfreq, epoch_len=None):
    epoch_length = int(epoch_len * sfreq)
    n_epochs = len(full_single_trace) // epoch_length
    output = np.zeros(n_epochs)
    for index in range(n_epochs):
        data_this_epoch = np.array(
            full_single_trace[index*epoch_length: (index+1)*epoch_length]
        )
        output[index] = np.sqrt(np.mean(data_this_epoch**2))
    return output

def get_epoch_psd(full_single_trace, sfreq, epoch_len=None):
    epoch_length = int(epoch_len * sfreq)
    n_epochs = len(full_single_trace) // epoch_length
    output = np.zeros((6, n_epochs))
    
    for index in range(n_epochs):
        data_this_epoch = np.array(
            full_single_trace[index*epoch_length: (index+1)*epoch_length]
        )
        psd = np.abs(np.fft.fft(data_this_epoch))**2
        time_step = 1 / sfreq

        freqs = np.fft.fftfreq(data_this_epoch.size, time_step)
        idx = np.argsort(freqs)
        freqs = freqs[idx]
        psd = psd[idx]
        
        delta = np.sum(psd[np.logical_and(freqs >= 1, freqs < 4)])      
        theta = np.sum(psd[np.logical_and(freqs >= 4, freqs < 8)])      
        alpha = np.sum(psd[np.logical_and(freqs >= 8, freqs < 12)])     
        sigma = np.sum(psd[np.logical_and(freqs >= 12, freqs < 15)])    
        beta  = np.sum(psd[np.logical_and(freqs >= 15, freqs < 30)])    
        gamma = np.sum(psd[freqs >= 30])                                

        output[0, index] = delta
        output[1, index] = theta
        output[2, index] = alpha
        output[3, index] = sigma
        output[4, index] = beta
        output[5, index] = gamma
    return output

def extract_experiment_global_stats(edf_filepath, epoch_len=4, emg_channel_no=1, eeg_channel_no=2, save_stats=True):
   
    
    
    raw = mne.io.read_raw_edf(edf_filepath, preload=True)
    sfreq = int(raw.info["sfreq"])

    
    raw.filter(1., 40., fir_design='firwin')
    
    raw_highpass = raw.copy()
    raw_highpass.pick_channels([raw.ch_names[emg_channel_no]])
    raw_highpass.filter(l_freq=20., h_freq=None, fir_design='firwin')
    
    raw_data = raw.get_data()
    raw_data[emg_channel_no] = raw_highpass.get_data()[0]
    
    del raw_highpass
    
    print("进度10%")
    df = pd.DataFrame()
    
    df['eeg_abs_mean'] = get_epoch_abs_mean(raw_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['emg_abs_mean'] = get_epoch_abs_mean(raw_data[emg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['eeg_abs_median'] = get_epoch_abs_median(raw_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['emg_abs_median'] = get_epoch_abs_median(raw_data[emg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['eeg_abs_max'] = get_epoch_abs_max(raw_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['emg_abs_max'] = get_epoch_abs_max(raw_data[emg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['eeg_abs_std'] = get_epoch_abs_std(raw_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['emg_abs_std'] = get_epoch_abs_std(raw_data[emg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['eeg_rms'] = get_epoch_rms(raw_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['emg_rms'] = get_epoch_rms(raw_data[emg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    
    print("进度30%")
    eeg_psd = get_epoch_psd(raw_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
    df['eeg_delta'] = eeg_psd[0]
    df['eeg_theta'] = eeg_psd[1]
    df['eeg_alpha'] = eeg_psd[2]
    df['eeg_sigma'] = eeg_psd[3]
    df['eeg_beta'] = eeg_psd[4]
    df['eeg_gamma'] = eeg_psd[5]
    
    print("进度60%")
    bands = ['delta', 'theta', 'alpha', 'sigma', 'beta', 'gamma']
    freq_ranges = {
        'delta': (1, 4),
        'theta': (4, 8),
        'alpha': (8, 12),
        'sigma': (12, 15),
        'beta': (15, 30),
        'gamma': (30, 40)
    }
    
    for band in bands:
        raw_firwin = raw.copy()
        l_freq, h_freq = freq_ranges[band]
        raw_firwin.filter(l_freq, h_freq, fir_design='firwin')
        raw_firwin_data = raw_firwin.get_data()
        
        df[f'eeg_firwin_{band}_abs_mean'] = get_epoch_abs_mean(raw_firwin_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
        df[f'eeg_firwin_{band}_abs_median'] = get_epoch_abs_median(raw_firwin_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
        df[f'eeg_firwin_{band}_abs_max'] = get_epoch_abs_max(raw_firwin_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
        df[f'eeg_firwin_{band}_abs_std'] = get_epoch_abs_std(raw_firwin_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
        df[f'eeg_firwin_{band}_rms'] = get_epoch_rms(raw_firwin_data[eeg_channel_no], sfreq=sfreq, epoch_len=epoch_len)
        
        del raw_firwin
        del raw_firwin_data
    
    print("进度80%")
    stats = {
        'median': {},
        'mean': {},
        'metadata': {
            'edf_file': os.path.basename(edf_filepath),
            'epoch_len': epoch_len,
            'sfreq': sfreq,
            'emg_channel_no': emg_channel_no,
            'eeg_channel_no': eeg_channel_no,
            'n_epochs': len(df),
            'channel_names': raw.ch_names
        }
    }
    
    
    for column in df.columns:
        stats['median'][column] = float(df[column].median())
        stats['mean'][column] = float(df[column].mean())
    
    print("进度100%")
    if save_stats:
        file_basename = os.path.splitext(os.path.basename(edf_filepath))[0]
        stats_filename = f"{file_basename}_experiment_stats_epoch_{epoch_len}s.json"
        stats_filepath = os.path.join(os.path.dirname(edf_filepath), stats_filename)
        
        with open(stats_filepath, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"统计信息已保存到: {stats_filepath}")

        
        # csv_filename = f"{file_basename}_all_features_epoch_{epoch_len}s.csv"
        # csv_filepath = os.path.join(os.path.dirname(edf_filepath), csv_filename)
        # df.to_csv(csv_filepath, index=True)
    
    return stats

def load_experiment_stats(stats_filepath):
    
    with open(stats_filepath, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    edf_file = "../36657_36657.edf"  
    
    if os.path.exists(edf_file):
        stats = extract_experiment_global_stats(
            edf_filepath=edf_file,
            epoch_len=4,
            emg_channel_no=1,
            eeg_channel_no=2
        )
        
        print("\n=== 统计信息摘要 ===")
        print(f"文件: {stats['metadata']['edf_file']}")
        print(f"Epoch数量: {stats['metadata']['n_epochs']}")
        print(f"采样频率: {stats['metadata']['sfreq']} Hz")
        print(f"通道: {stats['metadata']['channel_names']}")
        
        print("\n=== 部分特征统计 ===")
        for feature in ['eeg_abs_mean', 'emg_abs_mean', 'eeg_delta', 'eeg_theta']:
            if feature in stats['median']:
                print(f"{feature}: median={stats['median'][feature]:.6f}, mean={stats['mean'][feature]:.6f}")
    else:
        print(f"EDF文件不存在: {edf_file}")
        print("请修改edf_file变量为正确的文件路径") 