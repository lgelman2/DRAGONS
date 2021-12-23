# pytest suite
"""
Tests for primitives_bookkeeping.

This is a suite of tests to be run with pytest.

To run:
    1) Set the environment variable GEMPYTHON_TESTDATA to the path that
       contains the directories with the test data.
       Eg. /net/chara/data2/pub/gempython_testdata/
    2) From the ??? (location): pytest -v --capture=no
"""

# TODO @bquint: clean up these tests

import astrodata
import gemini_instruments
import os
import pytest

# from . import ad_compare
from geminidr.niri.primitives_niri_image import NIRIImage
from geminidr.gmos.primitives_gmos_image import GMOSImage
from gempy.utils import logutils

TESTDATAPATH = os.getenv('GEMPYTHON_TESTDATA', '.')
logfilename = 'test_bookkeeping.log'


# --- Fixtures ---
@pytest.fixture(scope="class")
def log():

    if os.path.exists(logfilename):
        os.remove(logfilename)

    log = logutils.get_logger(__name__)
    log.root.handlers = []
    logutils.config(mode='standard', file_name=logfilename)

    yield log

    os.remove(logfilename)


@pytest.fixture(scope="module")
def niri_ads(request, astrofaker):
    return [astrofaker.create('NIRI', ['IMAGE']) for _ in range(request.param)]

# --- Tests ---
@pytest.mark.parametrize('niri_ads', [2], indirect=True)
def test_clear_all_streams(niri_ads):
    p = NIRIImage(niri_ads[:1])
    p.streams['test'] = niri_ads[1:]
    p.clearAllStreams()
    assert not p.streams['test']
    assert len(p.streams['main']) == 1


@pytest.mark.parametrize('niri_ads', [2], indirect=True)
def test_clear_stream(niri_ads):
    p = NIRIImage(niri_ads[:1])
    p.streams['test'] = niri_ads[1:]
    p.clearStream(stream='test')
    assert not p.streams['test']
    assert len(p.streams['main']) == 1
    p.clearStream()
    assert not p.streams['main']


def test_slice_into_streams(astrofaker):
    def gmos_ads():
        ad1 = astrofaker.create("GMOS-N")
        ad1.init_default_extensions()
        ad2 = astrofaker.create("GMOS-N")
        ad2.init_default_extensions()
        return [ad1, ad2]

    # Slice, clearing "main"
    p = GMOSImage(gmos_ads())
    p.sliceIntoStreams(clear=True)
    assert len(p.streams) == 13
    for k, v in p.streams.items():
        assert len(v) == 0 if k == 'main' else 2

    # Slice, not clearing "main"
    p = GMOSImage(gmos_ads())
    p.sliceIntoStreams(clear=False)
    assert len(p.streams) == 13
    for k, v in p.streams.items():
        assert len(v) == 2

    # Slice with different lengths of input
    ad1, ad2 = gmos_ads()
    ad2.phu['EXTRA_KW'] = 33
    del ad1[5]
    p = GMOSImage([ad1, ad2])
    p.sliceIntoStreams(clear=False)
    assert len(p.streams) == 13
    for k, v in p.streams.items():
        assert len(v) == 1 if k == 'index11' else 2
    # The last stream should only have a slice from ad2
    assert 'EXTRA_KW' in p.streams['index11'][0].phu


class TestBookkeeping:
    """
    Suite of tests for the functions in the primitives_standardize module.
    """

    @pytest.mark.xfail(reason="Test needs revision", run=False)
    def test_addToList(self):
        filenames = ['N20070819S{:04d}_flatCorrected.fits'.format(i)
                     for i in range(104, 109)]

        adinputs = [astrodata.open(os.path.join(TESTDATAPATH, 'NIRI', f))
                    for f in filenames]

        # Add one image twice, just for laughs; it should appear only once
        adinputs.append(adinputs[0])

        p = NIRIImage(adinputs)
        p.stacks = {}
        p.addToList(purpose='forTest')

        for f in filenames:
            newfilename = f.replace('flatCorrected', 'forTest')
            assert os.path.exists(newfilename)
            os.remove(newfilename)

        # Check there's one stack of length 5
        assert len(p.stacks) == 1
        assert len(p.stacks[p.stacks.keys()[0]]) == 5

    @pytest.mark.xfail(reason="Test needs revision", run=False)
    def test_getList(self):
        pass

    @pytest.mark.xfail(reason="Test needs revision", run=False)
    def test_showInputs(self):
        pass

    @pytest.mark.xfail(reason="Test needs revision", run=False)
    def test_showList(self):
        pass

    @pytest.mark.xfail(reason="Test needs revision", run=False)
    def test_writeOutputs(self):
        filenames = ['N20070819S{:04d}_flatCorrected.fits'.format(i)
                     for i in range(104, 106)]

        adinputs = [astrodata.open(os.path.join(TESTDATAPATH, 'NIRI', f))
                    for f in filenames]

        p = NIRIImage(adinputs)
        p.writeOutputs(prefix='test', suffix='_blah', strip=True)

        # Check renamed files are on disk and the filenames have been
        # changed for the adinputs
        for f, ad in zip(filenames, p.streams['main']):
            newfilename = 'test' + f.replace('flatCorrected', 'blah')
            assert os.path.exists(newfilename)

            os.remove(newfilename)
            assert newfilename == ad.filename
