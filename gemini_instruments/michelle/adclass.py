from astrodata import astro_data_tag, astro_data_descriptor, returns_list, TagSet
from ..gemini import AstroDataGemini

class AstroDataMichelle(AstroDataGemini):

    __keyword_dict = dict(central_wavelength = 'GRATPOS',
                          coadds = 'NUMEXPOS',
                          disperser = 'GRATNAME',
                          dispersion = 'GRATDISP',
                          exposure_time = 'EXPOSURE',
                          filter_name = 'FILTER',
                          focal_plane_mask = 'SLITNAME',
                          read_mode = 'MODE')

    @staticmethod
    def _matches_data(source):
        return source[0].header.get('INSTRUME', '').upper() == 'MICHELLE'

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet({'MICHELLE'}, ())

    @astro_data_tag
    def _tag_mode(self):
        camera = self.phu.get('CAMERA')
        if camera == 'imaging':
            return TagSet({'IMAGE'}, ())
        elif camera == 'spectroscopy':
            return TagSet({'SPECT', 'LS'}, ())

    @astro_data_descriptor
    def exposure_time(self):
        """
        Returns the exposure time in seconds.

        Returns
        -------
        float
            Exposure time.
        """
        exposure_time = self.phu.get(self._keyword_for('exposure_time'), -1)
        num_ext = self.phu.get('NUMEXT', 1)
        if exposure_time < 0:
            return None
        return exposure_time * num_ext * self.coadds()

    @astro_data_descriptor
    def filter_name(self, stripID=False, pretty=False):
        """
        Returns the name of the filter(s) used. Since MICHELLE was not originally
        a Gemini instrument, its filters don't have componentIDs and so pretty
        and stripID do nothing.

        Parameters
        ----------
        stripID : bool
            Does nothing
        pretty : bool
            Does nothing

        Returns
        -------
        str
            The name of the filter
        """
        filter_name = self.phu.get('FILTER')
        return 'blank' if filter_name == 'NBlock' else filter_name

    @returns_list
    @astro_data_descriptor
    def pixel_scale(self):
        """
        Returns the image scale in arcseconds per pixel, one value per
        extension unless called on a single-extension slice. For Michelle,
        this comes from the PIXELSIZ PHU keyword

        Returns
        -------
        float/list of floats
            the pixel scale
        """
        return self.phu.get('PIXELSIZ')
