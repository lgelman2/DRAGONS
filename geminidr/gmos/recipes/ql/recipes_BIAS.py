"""
Recipes available to data with tags ['GMOS', 'CAL', 'BIAS'].
Default is "makeProcessedBias".
"""
recipe_tags = {'GMOS', 'CAL', 'BIAS'}

from geminidr.gmos.recipes.sq.recipes_BIAS import makeProcessedBias
from .recipes_common import makeIRAFCompatible

_default = makeProcessedBias
