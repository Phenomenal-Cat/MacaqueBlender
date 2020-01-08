
# GenerateMicroSaccades.py

import numpy as np
import scipy
import matplotlib.pyplot as plt

FrameRate       = 60            # Frames per second
Duration        = 2             # Clip duration (seconds)
PlotData        = 1

# Microsaccade parameters
MS = dict([
...     ('AmpMean', 16/60),         # Mean microsaccade amplitude (degrees)
...     ('AmpSig',10/60),           # SD of microsaccade amplitude (degrees)
...     ('DirMean', 0),             # Angular direction of bias for microsaccades (degrees from vertically up)
...     ('DirSig', 0),              # SD of microsaccade direction bias (degrees)
...     ('FreqMean', 0.5),          # Mean microsaccade frequency (Hz)
...     ('FreqSig', 0.5)])          # SD of microsaccade frequency (Hz)

MS['NoMS'] = FrameRate*MS['FreqMean']

# Generate random microsaccade intervals, amplitudes and directions
MS.Values.Int   = np.random.lognormal(mean=MS['FreqMean'], sigma=MS['FreqSig'], size=(1,MS['NoMS']))
MS.Values.Amps  = np.random.lognormal(mean=MS['AmpMean'], sigma=MS['AmpSig'], size=(1,MS['NoMS']))
MS.Values.Dirs  = np.random.uniform(low=0, high=360, size=(1,MS.NoMS))

# Plot some data?
if PlotData == 1:
    fig     = plt.figure()
    ax_lst  = plt.subplot(2, 2, 1)

    plt.hist()
    plt.plot(, )



#
