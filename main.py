import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

def scheduling(time, location, length, mandatory):
    if time:                                 # Business hours
        return (location and mandatory)      # In office and mandatory participation
    else:                                    # Outside business hours
        return ((not location) and length)   # Teleconference for a short duration


## Creating binary CSP
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(scheduling, ['time', 'location', 'length', 'mandatory'])


bqm = dwavebinarycsp.stitch(csp)
sampler = EmbeddingComposite(DWaveSampler(endpoint='https://cloud.dwavesys.com/sapi', token='DEV-a36d6f7d2d63b7c7601cd7f2d85b4e44a4f9b939', solver=[]))
response = sampler.sample(bqm, num_reads=5000)
min_energy = next(response.data(['energy']))[0]

total = 0
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    total = total + occurrences
    if energy == min_energy:
        time = 'business hours' if sample['time'] else 'evenings'
        location = 'office' if sample['location'] else 'home'
        length = 'short' if sample['length'] else 'long'
        mandatory = 'mandatory' if sample['mandatory'] else 'optional'
        print("{}: During {} at {}, you can schedule a {} meeting that is {}".format(occurrences, time, location, length, mandatory))
        print("Total occurrences: ", total)


