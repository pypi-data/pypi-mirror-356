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

def get_epoch_abs_mean (chunk_data):
    
    return np.abs(chunk_data).mean()


def get_epoch_abs_median (chunk_data):
    return np.median(np.abs(chunk_data))


def get_epoch_abs_max (chunk_data):
    return np.abs(chunk_data).max()


def get_epoch_abs_std (chunk_data):
    return np.abs(chunk_data).std()


def get_epoch_rms (chunk_data):
    return rmsValue(chunk_data)

def rmsValue(arr): 
    square = 0
    mean = 0.0
    root = 0.0
    n = len(arr)
    for i in range(0,n): 
        square += (arr[i]**2) 
      
    mean = (square / (float)(n)) 
      
    root = mean**0.5 
      
    return root 


def get_epoch_psd (chunk_data, sfreq):
    
    output = np.zeros(6)
    
    psd = np.abs(np.fft.fft(chunk_data))**2
    time_step = 1 / sfreq

    freqs = np.fft.fftfreq(chunk_data.size, time_step)
    idx = np.argsort(freqs)
    freqs = freqs[idx]
    psd = psd[idx]
    
    delta = np.sum(psd[np.logical_and(freqs >= 1, freqs <= 4)])
    theta = np.sum(psd[np.logical_and(freqs >= 4, freqs <= 8)])
    alpha = np.sum(psd[np.logical_and(freqs >= 8, freqs <= 12)])
    sigma = np.sum(psd[np.logical_and(freqs >= 12, freqs <= 15)])
    beta  = np.sum(psd[np.logical_and(freqs >= 15, freqs <= 30)])
    gamma = np.sum(psd[freqs >= 30])

    output[0] = delta
    output[1] = theta
    output[2] = alpha
    output[3] = sigma
    output[4] = beta
    output[5] = gamma
    return output

def load_experiment_stats(stats_filepath):
   
    with open(stats_filepath, 'r') as f:
        return json.load(f)

def extract_features_from_chunk(chunk_data, sfreq, epoch_len=4, emg_channel_no=None, eeg_channel_no=None, 
                               experiment_stats=None):
    
    try:       
        
        emg_data = chunk_data[emg_channel_no] 
        eeg_data = chunk_data[eeg_channel_no]
        
        eeg_filtered = butter_bandpass_filter(eeg_data, 1., 40., sfreq)
        emg_filtered = butter_highpass_filter(emg_data, 20., sfreq)

        feature_dict = {}
        base_features = {
            'eeg_abs_mean': get_epoch_abs_mean(eeg_filtered),
            'eeg_abs_median': get_epoch_abs_median(eeg_filtered),
            'eeg_abs_std': get_epoch_abs_std(eeg_filtered),
            'eeg_abs_max': get_epoch_abs_max(eeg_filtered),
            'eeg_rms': get_epoch_rms(eeg_filtered),
            
            'emg_abs_mean': get_epoch_abs_mean(emg_filtered),
            'emg_abs_median': get_epoch_abs_median(emg_filtered),
            'emg_abs_std': get_epoch_abs_std(emg_filtered),
            'emg_abs_max': get_epoch_abs_max(emg_filtered),
            'emg_rms': get_epoch_rms(emg_filtered),
        }
        feature_dict.update(base_features)
        
        if experiment_stats is not None:
            for base_col in base_features.keys():
                if base_col in experiment_stats.get('median', {}):
                    median_val = experiment_stats['median'][base_col]
                    if median_val != 0:
                        feature_dict[f'{base_col}_n'] = base_features[base_col] / median_val
                    else:
                        feature_dict[f'{base_col}_n'] = 0.0
                else:
                    print(f"Warning: Missing median stat for {base_col}")
                    feature_dict[f'{base_col}_n'] = 1.0  
                
                if base_col in experiment_stats.get('mean', {}):
                    mean_val = experiment_stats['mean'][base_col]
                    if mean_val != 0:
                        feature_dict[f'{base_col}_n2'] = base_features[base_col] / mean_val
                    else:
                        feature_dict[f'{base_col}_n2'] = 0.0
                else:
                    print(f"Warning: Missing mean stat for {base_col}")
                    feature_dict[f'{base_col}_n2'] = 1.0  
        
        eeg_psd = get_epoch_psd(eeg_filtered, sfreq)
        bands = ['delta', 'theta', 'alpha', 'sigma', 'beta', 'gamma']
        
        for i, band in enumerate(bands):
            band_power = eeg_psd[i]
            feature_dict[f'eeg_{band}'] = band_power
            
            if experiment_stats is not None:
                band_key = f'eeg_{band}'
                if band_key in experiment_stats.get('median', {}):
                    median_val = experiment_stats['median'][band_key]
                    if median_val != 0:
                        feature_dict[f'eeg_{band}_n'] = band_power / median_val
                    else:
                        feature_dict[f'eeg_{band}_n'] = 0.0
                else:
                    feature_dict[f'eeg_{band}_n'] = 1.0
                        
                if band_key in experiment_stats.get('mean', {}):
                    mean_val = experiment_stats['mean'][band_key]
                    if mean_val != 0:
                        feature_dict[f'eeg_{band}_n2'] = band_power / mean_val
                    else:
                        feature_dict[f'eeg_{band}_n2'] = 0.0
                else:
                    feature_dict[f'eeg_{band}_n2'] = 1.0
        
        ratios = ['theta', 'alpha', 'sigma', 'beta', 'gamma']
        delta_power = feature_dict['eeg_delta']
        
        for ratio in ratios:
            if delta_power != 0:
                feature_dict[f'eeg_{ratio}_delta_ratio'] = feature_dict[f'eeg_{ratio}'] / delta_power
                
                if experiment_stats is not None:
                    delta_n = feature_dict.get('eeg_delta_n', 1.0)
                    delta_n2 = feature_dict.get('eeg_delta_n2', 1.0)
                    
                    if delta_n != 0:
                        feature_dict[f'eeg_{ratio}_delta_ratio_n'] = feature_dict.get(f'eeg_{ratio}_n', 1.0) / delta_n
                    else:
                        feature_dict[f'eeg_{ratio}_delta_ratio_n'] = 0.0
                        
                    if delta_n2 != 0:
                        feature_dict[f'eeg_{ratio}_delta_ratio_n2'] = feature_dict.get(f'eeg_{ratio}_n2', 1.0) / delta_n2
                    else:
                        feature_dict[f'eeg_{ratio}_delta_ratio_n2'] = 0.0
            else:
                feature_dict[f'eeg_{ratio}_delta_ratio'] = 0.0
                if experiment_stats is not None:
                    feature_dict[f'eeg_{ratio}_delta_ratio_n'] = 0.0
                    feature_dict[f'eeg_{ratio}_delta_ratio_n2'] = 0.0
        
        freq_ranges = {
            'delta': (1, 4),
            'theta': (4, 8),
            'alpha': (8, 12),
            'sigma': (12, 15),
            'beta': (15, 30),
            'gamma': (30, 40)
        }
        
        for band in bands:
            l_freq, h_freq = freq_ranges[band]
            eeg_filtered_firwin = butter_bandpass_filter(eeg_filtered, l_freq, h_freq, sfreq)
            
            base_name = f'eeg_firwin_{band}'
            metrics = {
                'abs_mean': get_epoch_abs_mean,
                'abs_median': get_epoch_abs_median,
                'abs_max': get_epoch_abs_max,
                'abs_std': get_epoch_abs_std,
                'rms': get_epoch_rms
            }
            
            for metric_name, metric_func in metrics.items():
                base_value = metric_func(eeg_filtered_firwin)
                col = f'{base_name}_{metric_name}'
                feature_dict[col] = base_value
                
                if experiment_stats is not None:
                    if col in experiment_stats.get('median', {}):
                        median_val = experiment_stats['median'][col]
                        if median_val != 0:
                            feature_dict[f'{col}_n'] = base_value / median_val
                        else:
                            feature_dict[f'{col}_n'] = 0.0
                    else:
                        feature_dict[f'{col}_n'] = 1.0
                            
                    if col in experiment_stats.get('mean', {}):
                        mean_val = experiment_stats['mean'][col]
                        if mean_val != 0:
                            feature_dict[f'{col}_n2'] = base_value / mean_val
                        else:
                            feature_dict[f'{col}_n2'] = 0.0
                    else:
                        feature_dict[f'{col}_n2'] = 1.0
        
        df = pd.DataFrame([feature_dict])
        
        feature_order_path = os.path.join(os.path.dirname(__file__), "model", "feature_order.csv")
        if os.path.exists(feature_order_path):
            expected_features = pd.read_csv(feature_order_path, header=None, names=['feature'])
            feature_list = expected_features['feature'].str.strip().tolist()
            
            missing_features = set(feature_list) - set(df.columns)
            if missing_features:
                print(f"Warning: Missing features: {missing_features}")
                for feature in missing_features:
                    df[feature] = 0.0
            
            df = df[feature_list]

        df.index = range(len(df))
        
        return df
            
    except Exception as e:
        print(f"Error in extract_features_from_chunk: {str(e)}")
        raise

