# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 10:30:17 2021

@author: rueland
"""
        
import os
import numpy as np
import pandas as pd

def get_spike_spread(kilosort_output_folder, spread_amplitude_threshold=0.1):

    # compute spike template diffusion
    templates = np.load(os.path.join(kilosort_output_folder, "templates.npy")) # units, data, electrodes
        
    channel_spread = []
    for t, template in enumerate(templates):
        max_amp_per_channel = np.nanmax(template, axis=0)
        if all(np.isnan(x) for x in max_amp_per_channel): # check for nan templates
            channel_spread.append(np.nan)
        else:
            highest_amp = np.max(max_amp_per_channel)
            highest_amp_channel = np.argmax(max_amp_per_channel)
            desired_amp = highest_amp * spread_amplitude_threshold
            rel_pot_channels = np.abs(np.where(max_amp_per_channel < desired_amp)[0] - highest_amp_channel)
            first_channel_desired = np.min(rel_pot_channels)
            channel_spread.append(first_channel_desired)
            
    return channel_spread
        

def get_n_spikes(kilosort_output_folder, total_units):
    
    spike_clusters = np.load(os.path.join(kilosort_output_folder, 'spike_clusters.npy'))
    
    unit_n_spikes = np.zeros(total_units)
    for cluster_id in np.unique(spike_clusters):
        unit_n_spikes[cluster_id] = np.sum(spike_clusters == cluster_id)
        
    return unit_n_spikes


def create_extended_metrics_file(kilosort_output_folder, spread_amplitude_threshold=0.1, save=False):
    
    # load existing data for units
    cluster_labels = pd.read_csv(os.path.join(kilosort_output_folder, "cluster_KSLabel.tsv"), sep='\t')
    cluster_cont = pd.read_csv(os.path.join(kilosort_output_folder, "cluster_ContamPct.tsv"), sep='\t')
    cluster_amp = pd.read_csv(os.path.join(kilosort_output_folder, "cluster_Amplitude.tsv"), sep='\t')
    metrics = pd.read_csv(os.path.join(kilosort_output_folder, "metrics.csv"), index_col = 0)
    
    # compute number of spikes for each unit
    n_spikes_per_cluster = get_n_spikes(kilosort_output_folder, total_units=len(metrics))
        
    # compute spike template spread
    spread_per_cluster = get_spike_spread(kilosort_output_folder, spread_amplitude_threshold)
        
    # merge into df
    unit_table = pd.merge(metrics, cluster_labels)
    unit_table = pd.merge(unit_table, cluster_cont)
    unit_table = pd.merge(unit_table, cluster_amp)
    unit_table['channel_spread'] = spread_per_cluster
    unit_table['n_spikes'] = n_spikes_per_cluster
 
    if save is True:
        unit_table.to_csv(os.path.join(kilosort_output_folder, 'metrics_extended.csv'))
        
    return unit_table
        