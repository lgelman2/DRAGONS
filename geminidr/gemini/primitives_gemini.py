#
#                                                                  gemini_python
#
#                                                           primitives_gemini.py
# ------------------------------------------------------------------------------
from astropy.coordinates import SkyCoord

from gempy.gemini import gemini_tools as gt

from geminidr.core import Bookkeeping, CalibDB, Preprocess
from geminidr.core import Visualize, Standardize, Stack

from .primitives_qa import QA
from . import parameters_gemini

from recipe_system.utils.decorators import parameter_override, capture_provenance


# ------------------------------------------------------------------------------
@parameter_override
@capture_provenance
class Gemini(Standardize, Bookkeeping, Preprocess, Visualize, Stack, QA,
             CalibDB):
    """
    This is the class containing the generic Gemini primitives.

    """
    tagset = {"GEMINI"}

    def _initialize(self, adinputs, **kwargs):
        super()._initialize(adinputs, **kwargs)
        self._param_update(parameters_gemini)

    def addMDF(self, adinputs=None, suffix=None, mdf=None):
        """
        This primitive is used to add an Mask Definition File (MDF) extension to
        the input AstroData object. This MDF extension consists of a FITS binary
        table with information about where the spectroscopy slits are in
        the focal plane mask. In IFU, it is the position of the fibers. In
        Multi-Object Spectroscopy, it is the position of the multiple slits.
        In longslit is it the position of the single slit.

        If only one MDF is provided, that MDF will be add to all input AstroData
        object(s). If more than one MDF is provided, the number of MDF AstroData
        objects must match the number of input AstroData objects.

        If no MDF is provided, the primitive will attempt to determine an
        appropriate MDF.

        Parameters
        ----------
        suffix: str
            suffix to be added to output files
        mdf: str/None
            name of MDF to add (None => use default)
        """
        log = self.log
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        timestamp_key = self.timestamp_keys[self.myself()]

        mdf_list = mdf or self.caldb.get_calibrations(adinputs, caltype="mask").files

        for ad, mdf in zip(*gt.make_lists(adinputs, mdf_list, force_ad=True)):
            if ad.phu.get(timestamp_key):
                log.warning('No changes will be made to {}, since it has '
                            'already been processed by addMDF'.
                            format(ad.filename))
                continue
            if hasattr(ad, 'MDF'):
                log.warning('An MDF extension already exists in {}, so no '
                            'MDF will be added'.format(ad.filename))
                continue

            if mdf is None:
                log.stdinfo('No MDF could be retrieved for {}'.
                            format(ad.filename))
                continue

            try:
                # This will raise some sort of exception unless the MDF file
                # has a single MDF Table extension
                ad.MDF = mdf.MDF
            except:
                if len(mdf.tables) == 1:
                    ad.MDF = getattr(mdf, mdf.tables.pop())
                else:
                    log.warning('Cannot find MDF in {}, so no MDF will be '
                                'added'.format(mdf.filename))
                continue

            log.fullinfo('Attaching the MDF {} to {}'.format(mdf.filename,
                                                             ad.filename))

            gt.mark_history(ad, primname=self.myself(), keyword=timestamp_key)
            ad.update_filename(suffix=suffix, strip=True)
        return adinputs

    def standardizeObservatoryHeaders(self, adinputs=None, **params):
        """
        This primitive is used to make the changes and additions to the
        keywords in the headers of Gemini data.

        Parameters
        ----------
        suffix: str
            suffix to be added to output files
        """
        log = self.log
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        timestamp_key = self.timestamp_keys[self.myself()]

        for ad in adinputs:
            if ad.phu.get(timestamp_key):
                log.warning("No changes will be made to {}, since it has "
                            "already been processed by standardize"
                            "ObservatoryHeaders".format(ad.filename))
                continue

            # Update various header keywords
            log.status("Updating keywords that are common to all Gemini data")
            ad.hdr.set('BUNIT', 'adu', self.keyword_comments['BUNIT'])
            for ext in ad:
                if 'RADECSYS' in ext.hdr:
                    ext.hdr['RADESYS'] = (ext.hdr['RADECSYS'], ext.hdr.comments['RADECSYS'])
                    del ext.hdr['RADECSYS']

            # Timestamp and update filename
            gt.mark_history(ad, primname=self.myself(), keyword=timestamp_key)
            ad.update_filename(suffix=params["suffix"], strip=True)
        return adinputs

    def standardizeStructure(self, adinputs=None, **params):
        """
        This primitive is used to standardize the structure of Gemini data,
        specifically.

        Parameters
        ----------
        suffix: str
            suffix to be added to output files
        attach_mdf: bool
            attach an MDF to the AD objects?
        mdf: str
            full path of the MDF to attach
        """
        log = self.log
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        timestamp_key = self.timestamp_keys[self.myself()]

        # If attach_mdf=False, this just zips up the ADs with a list of Nones,
        # which has no side-effects.
        for ad, mdf in zip(*gt.make_lists(adinputs, params['mdf'])):
            if ad.phu.get(timestamp_key):
                log.warning("No changes will be made to {}, since it has "
                            "already been processed by standardizeStructure".
                            format(ad.filename))
                continue

            # Attach an MDF to each input AstroData object if it seems appropriate
            if params["attach_mdf"] and (ad.tags & {'LS', 'MOS', 'IFU', 'XD'}):
                self.addMDF([ad], mdf=mdf)

            # Timestamp and update filename
            gt.mark_history(ad, primname=self.myself(), keyword=timestamp_key)
            ad.update_filename(suffix=params["suffix"], strip=True)
        return adinputs

    def checkWCS(self, adinputs=None, tolerance=None):
        """
        This primitive checks for consistency within the WCS by comparing the
        header offsets with the WCS coordinates

        Parameters
        ----------
        tolerance: float
            positional tolerance in arcseconds
        """
        log = self.log
        log.debug(gt.log_message("primitive", self.myself(), "starting"))

        if len(set(ad.instrument() for ad in adinputs)) > 1:
            raise ValueError("Not all data are from the same instrument")
        if any('PREPARED' in ad.tags for ad in adinputs):
            raise ValueError(f"'{self.myself()}' requires unprepared data")

        adref = adinputs[0]
        refindex = (len(adref) - 1) // 2
        refpixel = tuple(length // 2 for length in adref[refindex].shape[::-1])

        bad = []
        for i, ad in enumerate(adinputs):
            offsets = ad.detector_x_offset(), ad.detector_y_offset()
            pixel = tuple(r + o for r, o in zip(refpixel, offsets)) + refpixel[2:]
            # Be wary of third F2 axis
            coord = SkyCoord(*ad[refindex].wcs(*pixel)[:2], unit='deg')
            if i == 0:
                log.stdinfo(f"Using {ad.filename} as the reference")
                ref_coord = coord
            else:
                sep = ref_coord.separation(coord).arcsec
                if sep > tolerance:
                    bad.append((ad.filename, sep))

        for (fname, sep) in bad:
            log.stdinfo(f"{fname} has a discrepancy of {sep:.2f} arcsec")

        if len(bad) > len(adinputs) // 2:
            log.stdinfo(f"The first frame ({adref.filename}) is likely to "
                        "be the one in error")
        elif not bad:
            log.stdinfo("All files appear to be OK")

        return adinputs
