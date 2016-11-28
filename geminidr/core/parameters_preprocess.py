# This parameter file contains the parameters related to the primitives located
# in the primitives_preprocess.py file, in alphabetical order.

from geminidr import ParametersBASE

class ParametersPreprocess(ParametersBASE):
    addObjectMaskToDQ = {
        "suffix"            : "_objectMaskAdded",
    }
    ADUToElectrons = {
        "suffix"            : "_ADUToElectrons",
    }
    applyDQPlane = {
        "suffix"            : "_dqPlaneApplied",
        "replace_flags"     : 255,
        "replace_value"     : "median",
    }
    associateSky = {
        "suffix"            : "_skyAssociated",
        "time"              : 600.,
        "distance"          : 3.,
        "max_skies"         : None,
        "use_all"           : False,
    }
    correctBackgroundToReferenceImage = {
        "suffix"            : "_backgroundCorrected",
        "remove_zero_level" : False,
    }
    # No default type defined; the flat parameter could be a string
    # or an AstroData object
    divideByFlat = {
        "suffix"            : "_flatCorrected",
        "flat"              : None,
    }
    makeSky = {
        "max_skies"         : None,
    }
    nonlinearityCorrect = {
        "suffix"            : "_nonlinearityCorrected",
    }
    normalizeFlat = {
        "suffix"            : "_normalized",
    }
    separateSky = {
        "suffix"            : "_skySeparated",
        "ref_obj"           : "",
        "ref_sky"           : "",
        "frac_FOV"          : 0.9,
    }
    subtractDark = {
        "suffix"            : "_darkCorrected",
        "dark"              : None,
    }
    subtractSky = {
        "suffix"            : "_skyCorrected",
    }
    subtractSkyBackground = {
        "suffix"            : "_skyBackgroundSubtracted",
    }
    thresholdFlatfield = {
        "suffix"            : "_thresholdFlatfielded",
        "upper"             : 10.0,
        "lower"             : 0.01,
    }