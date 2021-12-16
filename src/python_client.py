import torch
import numpy as np

import sbi.utils as utils
from sbi.inference.base import infer
from sbi.inference import SNPE, prepare_for_sbi, simulate_for_sbi

from sbi_signal_timing import *

# init wrapper
absim = ABStreet(API)

# get baseline
print('-- Running baseline --')
absim.run(24)
pre_duration = absim.data()['avg_trip_duration']/10000

# establish prior over timing variables
print('-- Verifying SBI setup --')
prior = utils.BoxUniform(low=torch.tensor([12,0,0]), high=torch.tensor([80,20,80]))

# set up SNPE
simulator, prior = prepare_for_sbi(sim_simple, prior)
inference = SNPE(prior)

# run simulation trials
theta, x = simulate_for_sbi(simulator, proposal=prior, num_simulations=250) # change this if needed
density_estimator = inference.append_simulations(theta, x).train()
posterior = inference.build_posterior(density_estimator)

# plotting (takes a while)
diffs = [0,4,8]
for diff in diffs:
    posterior_samples = posterior.sample((30000,), x=torch.tensor([pre_duration-diff]))
    plotting(posterior_samples)

means = []
for i in range(-10,10):
    posterior_samples = posterior.sample((50000,), x=torch.tensor([pre_duration+i*10000]))
    means.append(torch.mean(posterior_samples,axis=0).numpy())
    
print('Difference of best run: {}'.format(pre_duration-x[np.argmin(x)]))