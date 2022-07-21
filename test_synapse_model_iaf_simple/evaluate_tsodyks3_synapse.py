"""
Example of the tsodyks3_synapse in NEST
---------------------------------------

This example is based on the NEST example evaluate_tsodyks2_synapse.
Here, an additional postsynaptic neuron is simulated and connected
to the presynaptic neuron using the tsodyks3_synapse model.

"""

import nest
import nest.voltage_trace
import numpy as np
import matplotlib.pyplot as plt

nest.ResetKernel()


###############################################################################
# Parameter set for facilitation

fac_params = {"U": 0.2, "u": 0.2, 'x': 1.0, 'y': 0.0, "tau_fac": 1500.,
              "tau_rec": 200., "weight": 100.}
fac_params2 = {"U": 0.2, "u": 0.2, 'x': 1.0, "tau_fac": 1500.,
              "tau_rec": 200., "weight": 100.}
fac_params3 = {"U": 0.2, "u": 0.2, 'x': 1.0, "tau_fac": 1500.,
              "tau_rec": 200., "weight": 100.}

###############################################################################
# Now we assign the parameter set to the synapse models.

tsodyks_params = dict(fac_params, synapse_model="tsodyks_synapse")     # for tsodyks_synapse
tsodyks2_params = dict(fac_params2, synapse_model="tsodyks2_synapse")  # for tsodyks2_synapse
tsodyks3_params = dict(fac_params3, synapse_model="tsodyks3_synapse")  # for tsodyks3_synapse

###############################################################################
# Create three neurons.

neuron = nest.Create("iaf_psc_exp", 4)

###############################################################################
# Neuron one produces spikes. Neurons 2, 3 and 4 receive the spikes via the
# synapse models.

nest.Connect(neuron[0], neuron[1], syn_spec=tsodyks_params)
nest.Connect(neuron[0], neuron[2], syn_spec=tsodyks2_params)
nest.Connect(neuron[0], neuron[3], syn_spec=tsodyks3_params)

###############################################################################
# Now create the voltmeters to record the responses
 
voltmeter = nest.Create("voltmeter", 3, params={'interval': 0.1})


###############################################################################
# Connect the voltmeters to the neurons.

nest.Connect(voltmeter[0], neuron[1])
nest.Connect(voltmeter[1], neuron[2])
nest.Connect(voltmeter[2], neuron[3])

###############################################################################
# Now simulate the standard STP protocol: a burst of spikes, followed by a
# pause and a recovery response.

sim1 = 500.0
sim2 = 1000.0
sim3 = 500.0


#neuron[0].I_e = 376.0
neuron[0].set(I_e=376.0)
print(nest.GetStatus(neuron[0]))
nest.Simulate(sim1)

neuron[0].I_e = 0.0
print(nest.GetStatus(neuron[0]))
nest.Simulate(sim2)

neuron[0].I_e = 376.0
print(nest.GetStatus(neuron[0]))
nest.Simulate(sim3)


###############################################################################
# Finally, generate voltage traces. Both are shown in the same plot and
# should be almost completely overlapping.


voltmeter1 = voltmeter[0].get('events')
voltmeter2 = voltmeter[1].get('events')
voltmeter3 = voltmeter[2].get('events')



T = voltmeter1['times']
V1 = voltmeter1['V_m']
V2 = voltmeter2['V_m']
V3 = voltmeter3['V_m']

data_v = [T, V1, V2, V3]
np.savetxt("voltage_data.dat", data_v)

plt.figure(1)
nest.voltage_trace.from_device(voltmeter[0])
nest.voltage_trace.from_device(voltmeter[1])
nest.voltage_trace.from_device(voltmeter[2])
plt.show()

