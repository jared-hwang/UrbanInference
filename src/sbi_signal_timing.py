# visualization packages
import matplotlib.pyplot as plt
import matplotlib.animation
import seaborn as sns
import glob
from PIL import Image
import subprocess

from math import cos, pi, sin, sqrt
import numpy as np

import torch
import torch.nn as nn 
import torch.nn.functional as F

import time

API = 'http://localhost:1234'
ABSTREET_PATH = 'path/to/abstreet' # change this
AB_CMD = 'cargo run --release --bin headless -- --port=1234'.split()
abserver = {'proc': None}

def restart_abserver():
    print('Restarting AB server')
    if abserver['proc'] is not None:
        abserver['proc'].kill()
    abserver['proc'] = subprocess.Popen(ab_cmd, cwd=ABSTREET_PATH, stdout=subprocess.DEVNULL)
    time.sleep(3)

def plotting(posterior_samples):
    # mode posterior params
    mean = torch.mean(posterior_samples,axis=0).numpy()

    # mode posterior params
    mode = []
    for i in range(posterior_samples.shape[1]):
        n, bins = np.histogram(posterior_samples[:,i], bins=100)
        mode.append(bins[np.argmax(n)])

    # plot posterior samples
    _ = utils.pairplot(posterior_samples, fig_size=(5,5))
    plt.savefig('pairplot.png', format='png', dpi=300)

    # more detailed joint plot with mean, mode, and original parameter values
    a = sns.jointplot(
        x=posterior_samples[:,0].numpy().flatten(),
        y=posterior_samples[:,1].numpy().flatten(),
        marginal_ticks=False,
        kind="kde",
        marginal_kws=dict(fill=True))
    a.ax_joint.plot(mode[0], mode[1], 'go')
    a.ax_joint.text(mode[0]+2, mode[1]+0.5, 'mode')
    a.ax_joint.plot(mean[0], mean[1], 'yo')
    a.ax_joint.text(mean[0]+2, mean[1]+0.5, 'mean')
    plt.gcf().set_size_inches(10, 5.5)
    plt.savefig('density.png', format='png', dpi=300)

def sim_variable(params):
    '''
    Basic intersection sim, parametrized for signals at traffic light
    373@montlake. Params is a 12-dim vector with real values in accordance with
    variable traffic signal timing for each of four stages. Recovers fixed signal
    timing.
    '''
    rp = params.reshape([4,3])
    absim.reset()
    res = absim.set_traffic_signal_stages(373, {
        i : { 'Variable': (p*10000).tolist() } for i,p in enumerate(rp)
    })

    if res < 0:
        restart_abserver()
        return 10e8

    absim.run(24)
    return ab.data()['avg_trip_duration']

def sim_fixed(params):
    rp = params.reshape([4,1])
    absim.reset()
    res = absim.set_traffic_signal_stages(373, {
        i : { 'Fixed': int((p*10000).tolist()[0]) } for i,p in enumerate(rp)
    })

    if res < 0:
        restart_abserver()
        return torch.tensor([10e8])

    absim.run(24)
    return torch.tensor([absim.data()['avg_trip_duration']])

def sim_simple(params):
    absim.reset()
    res = absim.set_traffic_signal_stages(373, {
        i : { 'Fixed': int(params.tolist()[0]*10000) } for i in range(4)
    })

    if res < 0:
        restart_abserver()
        return torch.tensor([10e8])

    absim.run(24)
    return torch.tensor([absim.data()['avg_trip_duration']])


def sim_simple_var(params):
    absim.reset()
    stages = {
        i : { 'Variable': list(map(int, (params*10000).tolist())) } for i in range(4)
    }
    print('Submitting stages: {}'.format(stages))
    
    res = absim.set_traffic_signal_stages(373, stages)
    
    if res < 0:
        restart_abserver()
        return torch.tensor([10e5])

    absim.run(24)
    return torch.tensor([absim.data()['avg_trip_duration']])/10000