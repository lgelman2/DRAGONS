#
#                                                                 gemini_python
#
#                                                      primitives_niri_spect.py
# -----------------------------------------------------------------------------

import os

from importlib import import_module

from geminidr.core import Spect
from gemini_instruments import gmu
from gempy.gemini import gemini_tools as gt
from gempy.library import transform, wavecal
from gemini_instruments.niri import lookup
from recipe_system.utils.decorators import parameter_override, capture_provenance

from .primitives_niri import NIRI
from . import parameters_niri_spect


@parameter_override
@capture_provenance
class NIRISpect(Spect, NIRI):
    """
    This is the class containing all of the preprocessing primitives for the
    NIRISpect level of the hierarchy tree. It inherits all the primitives from
    the level above.
    """
    tagset = {"GEMINI", "NIRI", "SPECT"}

    def _initialize(self, adinputs, **kwargs):
        super()._initialize(adinputs, **kwargs)
        self._param_update(parameters_niri_spect)

    def standardizeWCS(self, adinputs=None, **params):
        """
        This primitive updates the WCS attribute of each NDAstroData extension
        in the input AstroData objects. For spectroscopic data, it means
        replacing an imaging WCS with an approximate spectroscopic WCS.

        Parameters
        ----------
        suffix: str/None
            suffix to be added to output files

        """
        log = self.log
        timestamp_key = self.timestamp_keys[self.myself()]
        log.debug(gt.log_message("primitive", self.myself(), "starting"))
        super().standardizeWCS(adinputs, **params)

        for ad in adinputs:
            log.stdinfo(f"Adding spectroscopic WCS to {ad.filename}")
            # For NIRI wavelength at central pixel doesn't match the descriptor value
            cenwave = self._get_actual_cenwave(ad, asNanometers=True)
            # NIRI's dispersion and spatial axis have the same length.
            # Different square-shaped ROIs can be used, all centered on the array.
            dispersion_axis = 2 - ad[0].dispersion_axis()
            npix = ad[0].shape[1 - dispersion_axis]
            center = 0.5 * (npix - 1)
            transform.add_longslit_wcs(ad, central_wavelength=cenwave,
                                       pointing=ad[0].wcs(center, center))

            # Timestamp. Suffix was updated in the super() call
            gt.mark_history(ad, primname=self.myself(), keyword=timestamp_key)
        return adinputs


    def determineWavelengthSolution(self, adinputs=None, **params):
        """
        This NIRI-specific primitive sets the default order in case it's None.
        It then calls the generic version of the primitive.

        Parameters
        ----------
        adinputs : list of :class:`~astrodata.AstroData`
             Mosaicked Arc data as 2D spectral images or 1D spectra.

        suffix : str/None
            Suffix to be added to output files

        order : int
            Order of Chebyshev fitting function.

        center : None or int
            Central row/column for 1D extraction (None => use middle).

        nsum : int, optional
            Number of rows/columns to average.

        min_snr : float
            Minimum S/N ratio in line peak to be used in fitting.

        weighting : {'natural', 'relative', 'none'}
            How to weight the detected peaks.

        fwidth : float/None
            Expected width of arc lines in pixels. It tells how far the
            KDTreeFitter should look for when matching detected peaks with
            reference arcs lines. If None, `fwidth` is determined using
            `tracing.estimate_peak_width`.

        min_sep : float
            Minimum separation (in pixels) for peaks to be considered distinct

        central_wavelength : float/None
            central wavelength in nm (if None, use the WCS or descriptor)

        dispersion : float/None
            dispersion in nm/pixel (if None, use the WCS or descriptor)

        linelist : str/None
            Name of file containing arc lines. If None, then a default look-up
            table will be used.

        alternative_centers : bool
            Identify alternative central wavelengths and try to fit them?

        nbright : int (or may not exist in certain class methods)
            Number of brightest lines to cull before fitting

        absorption : bool
            If feature type is absorption (default: "False")

        interactive : bool
            Use the interactive tool?

        debug : bool
            Enable plots for debugging.

        Returns
        -------
        list of :class:`~astrodata.AstroData`
            Updated objects with a `.WAVECAL` attribute and improved wcs for
            each slice
"""
        for ad in adinputs:
            if params["absorption"] or ad.central_wavelength(asMicrometers=True) >= 2.8:
                params["lsigma"] = 2
                params["hsigma"] = 2
                if params["min_snr"] is None:
                    params["min_snr"] = 1
        adinputs = super().determineWavelengthSolution(adinputs, **params)
        return adinputs

    
    def _get_arc_linelist(self, waves=None, ext=None, config=None):
        lookup_dir = os.path.dirname(import_module('.__init__',
                                                   self.inst_lookups).__file__)

        if 'ARC' in ext.tags:
            if 'Xe' in ext.object():
                linelist ='Ar_Xe.dat'
            elif "Ar" in ext.object():
                linelist = 'argon.dat'
            else:
                raise ValueError(f"No default line list found for {ext.object()}-type arc. Please provide a line list.")
        else:
            if config.absorption is True or \
                    ext.central_wavelength(asMicrometers=True) >= 2.8:
                linelist = super()._get_atran_linelist(ext=ext, config=config)
                return wavecal.LineList(linelist)
            # In case of wavecal from sky OH emission use these line lists:
            else:
                linelist = 'nearIRsky.dat'

        self.log.stdinfo(f"Using linelist {linelist}")
        filename = os.path.join(lookup_dir, linelist)

        return wavecal.LineList(filename)


    def _get_resolution(self, ad=None):
        # For NIRI actual resolving power values are much lower than
        # the theoretical ones, so read them from LUT
        camera = ad.camera()
        disperser = ad.disperser(stripID=True)[0:6]
        fpmask = ad.focal_plane_mask(stripID=True)
        print(f"resolution = {lookup.spec_wavelengths[camera, fpmask, disperser][2]}")
        return lookup.spec_wavelengths[camera, fpmask, disperser][2]


    def _get_actual_cenwave(self, ext=None, asMicrometers=False, asNanometers=False, asAngstroms=False):
        # For NIRI wavelength at central pixel doesn't match the descriptor value

        unit_arg_list = [asMicrometers, asNanometers, asAngstroms]
        output_units = "meters" # By default
        if unit_arg_list.count(True) == 1:
            # Just one of the unit arguments was set to True. Return the
            # central wavelength in these units
            if asMicrometers:
                output_units = "micrometers"
            if asNanometers:
                output_units = "nanometers"
            if asAngstroms:
                output_units = "angstroms"
        camera = ext.camera()
        disperser = ext.disperser(stripID=True)[0:6]
        fpmask = ext.focal_plane_mask(stripID=True)
        cenwave = lookup.spec_wavelengths[camera, fpmask, disperser][1]
        actual_cenwave = gmu.convert_units('nanometers', cenwave, output_units)

        return actual_cenwave
