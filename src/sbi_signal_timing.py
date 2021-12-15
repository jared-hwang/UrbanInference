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

import sbi.utils as utils
from sbi.inference.base import infer
from sbi.inference import SNPE, prepare_for_sbi, simulate_for_sbi

from .ABStreet import ABStreet

API = 'http://localhost:1234'

ab_cmd = 'cargo run --release --bin headless -- --port=1234'.split()
abserver = subprocess.Popen(ab_cmd)
absim = ABStreet(API)

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
        xlim=[0,length],
        ylim=[0,width],
        marginal_ticks=False,
        kind="kde",
        marginal_kws=dict(fill=True))
    a.ax_joint.plot(mode[0], mode[1], 'go')
    a.ax_joint.text(mode[0]+2, mode[1]+0.5, 'mode')
    a.ax_joint.plot(mean[0], mean[1], 'yo')
    a.ax_joint.text(mean[0]+2, mean[1]+0.5, 'mean')
    a.ax_joint.plot(rpos[0], rpos[1], 'rx')
    a.ax_joint.text(rpos[0]+2, rpos[1]+0.5, 'target')
    plt.gcf().set_size_inches(10, 5.5)
    plt.savefig('density.png', format='png', dpi=300)

def sim_variable(params):
    '''
    Basic intersection sim, parametrized for signals at traffic light
    373@montlake. Params is a 12-dim vector with real values in accordance with
    variable traffic signal timing for each of four stages. Recovers fixed signal
    timing.
    '''
    ab = ABStreet(API)
    ab.set_traffic_signal_stages(373, {})
    pass

def sim_fixed(params):
    rp = params.reshape([4,3])
    absim.reset()
    res = absim.set_traffic_signal_stages(373, {
        i : { 'Variable': (p*10000).tolist() } for i,p in enumerate(rp)
    })

    if res < 0:
        abserver.kill()
        abserver = subprocess.Popen(ab_cmd)
        return 10e8

    absim.run(12)
    return ab.data()['avg_trip_duration']


if __name__ == '__main__':
    # get baseline
    absim.run(12)
    pre_duration = absim.data()['avg_trip_duration']
    
    # establish prior over timing variables
    prior = utils.BoxUniform(low=torch.tensor([10]*4), high=torch.tensor([200]*4))
    simulator, prior = prepare_for_sbi(sim_fixed, prior)
    inference = SNPE(prior)

    theta, x = simulate_for_sbi(simulator, proposal=prior, num_simulations=15000)
    density_estimator = inference.append_simulations(theta, x).train()
    posterior = inference.build_posterior(density_estimator)
    posterior_samples = posterior.sample((50000,), x=real_data)

    plotting(posterior_samples)
