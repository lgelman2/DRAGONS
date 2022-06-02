#
#                                                                  gemini_python
#
#                                                           primitives_gemini.py
# ------------------------------------------------------------------------------
import datetime
from copy import deepcopy

from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.modeling import models

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

        log.status("Updating keywords that are common to all Gemini data")
        for ad in adinputs:
            if ad.phu.get(timestamp_key):
                log.warning(f"No changes will be made to {ad.filename}, "
                            "since it has already been processed by "
                            "standardizeObservatoryHeaders")
                continue

            # Update various header keywords
            ad.hdr.set('BUNIT', 'adu', self.keyword_comments['BUNIT'])
            for ext in ad:
                if 'RADECSYS' in ext.hdr:
                    ext.hdr['RADESYS'] = (ext.hdr['RADECSYS'], ext.hdr.comments['RADECSYS'])
                    del ext.hdr['RADECSYS']

            # Timestamp and update filename
            gt.mark_history(ad, primname=self.myself(), keyword=timestamp_key)
            ad.update_filename(suffix=params["suffix"], strip=True)
            log.debug(f"Successfully updated keywords for {ad.filename}")
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

    def standardizeWCS(self, adinputs=None, **params):
        """
        This primitive attempts to identify inputs with a bad WCS based on the
        relationship between the WCS and other header keywords. If any such
        inputs are found, the reduction may either exit, or it may attempt to
        fix the WCS using header keywords describing the telescope offsets.
        In addition, it is also possible to construct entirely new WCS objects
        for each input based on the offsets.

        The primitive defines "groups" which are sequences of ADs with the
        same observation_id() and without a significant amount of dead time
        between successive exposures. Within each group, a base "Pointing" is
        constructed from the first AD with a self-consistent WCS, and the most
        recent self-consistent WCS is also stored. When an AD with a bad WCS is
        encountered, an attempt is made to fix it using the base Pointing first
        and then the most recent. This is done because only GNIRS can handle
        rotations between images and, if a sequence includes rotations, this
        rotation could become large over the course of a group, but might be
        small enough to ignore between successive images.

        Note that this method must be called BEFORE any instrument-specific
        WCS modifications, such as adding a spectroscopic axis. Child
        standardizeWCS() methods should super() this one before doing their
        own work.

        Parameters
        ----------
        suffix: str
            suffix to be added to output files
        bad_wcs: str (exit | fix | bootstrap)
            how to handle a bad WCS, or whether to create a complete new set
        """
        log = self.log
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        timestamp_key = self.timestamp_keys[self.myself()]
        suffix = params["suffix"]
        bad_wcs = params["bad_wcs"]
        limit = params["debug_consistency_limit"]
        max_deadtime = params["debug_max_deadtime"]
        if bad_wcs == 'ignore':
            log.stdinfo("No WCS checking will take place")
            return adinputs

        bad_wcs_list = []
        base_pointing = None
        last_pointing = None
        last_obsid = None
        last_endtime = None
        for ad in adinputs:
            if ad.tags.intersection({'ARC', 'BIAS', 'DARK', 'FLAT'}):
                log.debug(f"Skipping {ad.filename} due to its tags")
                continue

            this_datetime = ad.ut_datetime()
            this_obsid = ad.observation_id()
            if last_endtime is not None and (this_obsid != last_obsid or
                    (this_datetime - last_endtime).seconds > max_deadtime):
                if base_pointing is None:
                    raise ValueError(f"Now processing {ad.filename} but could "
                                     "not find a valid pointing in the "
                                     "previous group")
                log.debug(f"Starting new group with {ad.filename}")
                base_pointing = None
                last_pointing = None

            p = Pointing(ad)
            needs_fixing = not p.self_consistent(limit=limit)

            if needs_fixing or bad_wcs == 'bootstrap':
                if bad_wcs == 'exit' or base_pointing is None:
                    # Do not want to, or cannot yet, fix
                    bad_wcs_list.append(ad)
                else:
                    # Want to, and can, fix, so fix!
                    if last_pointing is None:
                        log.stdinfo(base_pointing.fix_wcs(ad))
                    else:  # can try both the base and the last Pointings
                        try:
                            log.stdinfo(base_pointing.fix_wcs(ad))
                        except NotImplementedError:
                            log.debug(f"Could not fix {ad.filename} using "
                                      f"{base_pointing.filename}")
                            log.stdinfo(last_pointing.fix_wcs(ad))

            if not needs_fixing:
                last_pointing = p
                if base_pointing is None:
                    # Found a reliable base WCS
                    base_pointing = p
                    # Fix all backed up ADs if we want to
                    if bad_wcs != 'exit':
                        while bad_wcs_list:
                            log.stdinfo(base_pointing.fix_wcs(bad_wcs_list.pop(0)))

            last_endtime = (this_datetime +
                            datetime.timedelta(seconds=ad.exposure_time()))
            last_obsid = this_obsid

        if bad_wcs == 'exit' and bad_wcs_list:
            log.stdinfo("The following files were identified as having bad "
                        "WCS information:")
            for ad in bad_wcs_list:
                log.stdinfo(f"    {ad.filename}")
            raise ValueError("Some files have bad WCS information and user "
                             "has requested an exit")

        for ad in adinputs:
            # Timestamp and update filename
            gt.mark_history(ad, primname=self.myself(), keyword=timestamp_key)
            ad.update_filename(suffix=suffix, strip=True)

        return adinputs


class Pointing:
    # (x, y), 0-indexed
    center_of_rotation_dict = {'GNIRS': (629., 519.)}

    def __init__(self, ad):
        self.phu = ad.phu.copy()
        self.wcs = [ext.wcs for ext in ad]
        self.target_coords = SkyCoord(ad.target_ra(), ad.target_dec(),
                                      unit=u.deg)
        self.coords = SkyCoord(ad.ra(), ad.dec(), unit=u.deg)
        self.xoffset = ad.detector_x_offset()
        self.yoffset = ad.detector_y_offset()
        self.filename = ad.filename

    def __repr__(self):
        return f"Pointing object from {self.filename}"

    def self_consistent(self, limit=10):
        """
        Determine whether the WCS information in this Pointing is
        self-consistent and therefore (presumably) reliable

        Parameters
        ----------
        limit: float
            maximum discrepancy (in arcseconds) between the expected and
            actual pointings for the pointing to be considered OK

        Returns
        -------
        bool: is the pointing self-consistent?
        """
        expected_coords = self.target_coords.spherical_offsets_by(
            self.phu['RAOFFSET']*u.arcsec, self.phu['DECOFFSE']*u.arcsec)
        return self.coords.separation(expected_coords).arcsec <= limit

    def fix_wcs(self, ad):
        """
        Fix another AD based on this pointing. The aim here is to preserve
        the pixel location around which the Pix2Sky projection occurs.

        Parameters
        ----------
        ad: AstroData object
            the AD whose WCS needs fixing

        Returns
        -------
        str: message indicating how the WCS has been fixed
        """
        xoffset, yoffset = ad.detector_x_offset(), ad.detector_y_offset()
        delta_pa = self.phu['PA'] - ad.phu['PA']
        rotate = abs(delta_pa) > 0.1
        if rotate:
            try:
                x0, y0 = self.center_of_rotation_dict[ad.instrument()]
            except KeyError:
                raise NotImplementedError("No center of rotation defined for "
                                          f"{ad.instrument()}. Please contact "
                                          "the HelpDesk for advice.")
            t = ((models.Shift(-xoffset - x0) & models.Shift(-yoffset - y0)) |
                 models.Rotation2D(delta_pa) |
                 (models.Shift(self.xoffset + x0) & models.Shift(self.yoffset + y0)))
        else:
            t = models.Shift(self.xoffset - xoffset) & models.Shift(self.yoffset - yoffset)

        # Copy the WCS of each extension of the "Pointing" AD, but update
        # the (RA, DEC) of the projection center, and the rotation matrix
        for ext, wcs in zip(ad, self.wcs):
            for m in wcs.forward_transform:
                if isinstance(m, models.AffineTransformation2D):
                    aftran = m
                elif isinstance(m, models.RotateNative2Celestial):
                    nat2cel = m
                    break
            else:
                raise ValueError("Cannot find center point of projection")
            x, y = wcs.invert(nat2cel.lon.value, nat2cel.lat.value)
            xnew, ynew = t(x, y)
            new_lon, new_lat = wcs(xnew, ynew)
            ext.wcs = deepcopy(wcs)
            for m in wcs.forward_transform:
                if isinstance(m, models.AffineTransformation2D) and rotate:
                    m.matrix = models.Rotation2D(delta_pa)(*aftran.matrix.value)
                elif isinstance(m, models.RotateNative2Celestial):
                    m.lon = new_lon
                    m.lat = new_lat

        return f"Fixing the WCS for {ad.filename} using {self.filename}"
