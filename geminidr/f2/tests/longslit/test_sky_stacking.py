#!/usr/bin/env python3
"""
Tests for sky stacking and subtraction for F2.
"""

import pytest

import astrodata
from astrodata.testing import download_from_archive
import gemini_instruments
from geminidr.f2.primitives_f2_longslit import F2Longslit


# ---- Tests ------------------------------------------------------------------

def test_associate_sky(change_working_dir, path_to_inputs):

    files = ['S20200301S0071.fits', 'S20200301S0072.fits',
             'S20200301S0073.fits', 'S20200301S0074.fits']

    with change_working_dir(path_to_inputs):
        data = [astrodata.open(f) for f in files]

    p = F2Longslit(data)
    p.separateSky()
    p.associateSky()

    A1, B1, B2, A2 = p.showList()
    A_frames = {'S20200301S0071_skyAssociated.fits',
                'S20200301S0074_skyAssociated.fits'}
    B_frames = {'S20200301S0072_skyAssociated.fits',
               'S20200301S0073_skyAssociated.fits'}

    for ad in (A1, A2):
        assert set(ad.SKYTABLE['SKYNAME']) == B_frames
    for ad in (B1, B2):
        assert set(ad.SKYTABLE['SKYNAME']) == A_frames
