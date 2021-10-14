# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 11:50:39 2021

@author: rueland
"""


import os
import numpy as np


def get_n_spikes(kilosort_output_folder):
    
    spike_times = np.load(os.path.join(kilosort_output_folder, 'spike_times.npy'))
    spike_clusters = np.load(os.path.join(kilosort_output_folder, 'spike_clusters.npy'))
                                                        
    unit_spikes, unit_ids = compute_unit_spikes(spike_times, spike_clusters)    

    unit_n_spikes = [len(x) for x in unit_spikes] 

    return unit_n_spikes, unit_ids           
    


def compute_unit_spikes(spike_times, spike_clusters):
    unit_spikes = []
    unit_ids = []
    for cluster_id in np.unique(spike_clusters):
        unit_spikes.append(spike_times[np.where(spike_clusters == cluster_id)])
        unit_ids.append(cluster_id)   
        
    return unit_spikes, unit_ids