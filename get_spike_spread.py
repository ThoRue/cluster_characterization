# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 14:47:24 2021

@author: rueland
"""


def get_spike_spread(kilosort_output_folder, fraction_of_amp=0.1):

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
            desired_amp = highest_amp * fraction_of_amp
            rel_pot_channels = np.abs(np.where(max_amp_per_channel < desired_amp)[0] - highest_amp_channel)
            first_channel_desired = np.min(rel_pot_channels)
            channel_spread.append(first_channel_desired)
        