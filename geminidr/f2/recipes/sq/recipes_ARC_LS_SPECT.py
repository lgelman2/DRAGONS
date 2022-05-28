"""
Recipes available to data with tags ['F2', 'SPECT', 'LS'],
excluding data with tags ['FLAT', 'DARK', 'BIAS'].
These are F2 longslit arc-lamp or sky-line calibrations.
Default is "makeProcessedArc".
"""
recipe_tags = {'F2', 'SPECT', 'LS'}
blocked_tags = {'FLAT', 'DARK', 'BIAS'}

def makeProcessedArc(p):
    p.prepare()
    p.addDQ()
    p.addVAR(read_noise=True)
    p.ADUToElectrons()
    p.addVAR(poisson_noise=True)
  #  p.darkCorrect(do_cal=False) # opt for cals from skylines?
  #  p.flatCorrect(do_cal=False) # opt for cals from skylines?
    p.stackFrames()
    p.makeIRAFCompatible()
    p.determineWavelengthSolution()
    p.determineDistortion(debug=True)
    p.storeProcessedArc()
    p.writeOutputs()


_default = makeProcessedArc
