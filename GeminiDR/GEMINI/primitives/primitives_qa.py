# Prototype demo
from astrodata.utils import logutils

from gempy.gemini import gemini_tools as gt

from GEMINI.lookups import BGConstraints
from GEMINI.lookups import CCConstraints
from GEMINI.lookups import IQConstraints

from primitives_CORE import PrimitivesCORE

# ------------------------------------------------------------------------------
class QA(PrimitivesCORE):
    """
    This is the class containing all of the primitives for the GEMINI level of
    the type hierarchy tree. It inherits all the primitives from the level
    above, 'GENERALPrimitives'.
    """
    tag = "GEMINI"

    def measureBG(self, adinputs=None, stream='main', **params):
        """
        This primitive measures the sky background level for an image by
        averaging (clipped mean) the sky background level for each object 
        in the OBJCAT generated by detect_sources, ie the BACKGROUND value 
        from sextractor.

        The count levels are then converted to a flux using the nominal
        (*not* measured) Zeropoint values - the point being you want to measure
        the actual background level, not the flux incident on the top of the 
        cloud layer necessary to produce that flux level.

        """
        log = logutils.get_logger(__name__)
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        logutils.update_indent(3)
        pmsg = "{}:{}".format("PRIMITIVE:", self.myself())
        p_pars = self.parameters.measureBG
        sfx = p_pars["suffix"]
        log.status("-" * len(pmsg))
        log.status(pmsg)
        log.status("-" * len(pmsg))

        log.stdinfo("BGConstraints: \n{}".format(BGConstraints.bgConstraints))

        timestamp_key = self.timestamp_keys[self.myself()]
        if adinputs:
            self.adinputs = adinputs

        log.stdinfo("Parameters available on {}".format(self.myself()))
        log.stdinfo(str(p_pars))
        log.stdinfo("working on ...")
        for ad in self.adinputs:
            log.stdinfo(ad.filename)

        # Add the appropriate time stamps to the PHU
        gt.mark_history(adinput=ad, primname=self.myself(), keyword=timestamp_key)
        for ad in self.adinputs:
            ad.filename = gt.filename_updater(adinput=ad, suffix=sfx, strip=True)
            log.stdinfo(ad.filename)

        logutils.update_indent(0)
        return

    def measureCC(self, adinputs=None, stream='main', **params):
        """
        This primitive will determine the zeropoint by looking at
        sources in the OBJCAT for which a reference catalog magnitude
        has been determined.

        It will also compare the measured zeropoint against the nominal
        zeropoint for the instrument and the nominal atmospheric extinction
        as a function of airmass, to compute the estimated cloud attenuation.

        This function is for use with sextractor-style source-detection.
        It relies on having already added a reference catalog and done the
        cross match to populate the refmag column of the objcat

        The reference magnitudes (refmag) are straight from the reference
        catalog. The measured magnitudes (mags) are straight from the object
        detection catalog.

        We correct for astromepheric extinction at the point where we
        calculate the zeropoint, ie we define:
        actual_mag = zeropoint + instrumental_mag + extinction_correction

        where in this case, actual_mag is the refmag, instrumental_mag is
        the mag from the objcat, and we use the nominal extinction value as
        we don't have a measured one at this point. ie  we're actually
        computing zeropoint as:
        zeropoint = refmag - mag - nominal_extinction_correction

        Then we can treat zeropoint as: 
        zeropoint = nominal_photometric_zeropoint - cloud_extinction
        to estimate the cloud extinction.

        """
        log = logutils.get_logger(__name__)
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        logutils.update_indent(3)
        pmsg = "{}:{}".format("PRIMITIVE:", self.myself())
        p_pars = self.parameters.measureCC
        sfx = p_pars["suffix"]
        log.status("-" * len(pmsg))
        log.status(pmsg)
        log.status("-" * len(pmsg))

        log.stdinfo("CCConstraints: \n{}".format(CCConstraints.ccConstraints))

        timestamp_key = self.timestamp_keys[self.myself()]
        if adinputs:
            self.adinputs = adinputs

        log.stdinfo("Parameters available on {}".format(self.myself()))
        log.stdinfo(str(p_pars))
        log.stdinfo("working on ...")
        for ad in self.adinputs:
            log.stdinfo(ad.filename)

        # Add the appropriate time stamps to the PHU
        gt.mark_history(adinput=ad, primname=self.myself(), keyword=timestamp_key)
        for ad in self.adinputs:
            ad.filename = gt.filename_updater(adinput=ad, suffix=sfx, strip=True)
            log.stdinfo(ad.filename)

        logutils.update_indent(0)
        return

    def measureIQ(self, adinputs=None, stream='main', **params):
        """
        This primitive is for use with sextractor-style source-detection.
        FWHM (from _profile_sources()) and CLASS_STAR (from SExtractor)
        are already in OBJCAT; this function does the clipping and reporting
        only. Measured FWHM is converted to zenith using airmass^(-0.6).

        """
        log = logutils.get_logger(__name__)
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        logutils.update_indent(3)
        pmsg = "{}:{}".format("PRIMITIVE:", self.myself())
        p_pars = self.parameters.measureIQ
        sfx = p_pars["suffix"]
        log.status("-" * len(pmsg))
        log.status(pmsg)
        log.status("-" * len(pmsg))

        log.stdinfo("IQConstraints: \n{}".format(IQConstraints))

        timestamp_key = self.timestamp_keys[self.myself()]
        if adinputs:
            self.adinputs = adinputs

        log.stdinfo("Parameters available on {}".format(self.myself()))
        log.stdinfo(str(p_pars))
        log.stdinfo("working on ...")
        for ad in self.adinputs:
            log.stdinfo(ad.filename)

        # Add the appropriate time stamps to the PHU
        gt.mark_history(adinput=ad, primname=self.myself(), keyword=timestamp_key)
        for ad in self.adinputs:
            ad.filename = gt.filename_updater(adinput=ad, suffix=sfx, strip=True)
            log.stdinfo(ad.filename)

        logutils.update_indent(0)
        return
