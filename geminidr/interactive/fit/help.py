
def _plot_tool(name, icon):
    return '<img width=16 height=16 src="dragons/static/help/' + icon + '.png"/><span><b>' + name + '</b></span><br/>'


tools_with_select = (
    ("Move", 'move', 'drag the plot around to reposition it'),
    ("Free-Select", 'lasso_select', 'draw an arbitrary area to select points for masking/unmasking<br/><i>also works with shift</i>'),
    ('Box Zoom', 'box_zoom', 'drag a rectangle to zoom into that area of the plot'),
    ('Box Select', 'box_select', 'drag a rectangle to select points for masking/unmasking<br/><i>also works with shift</i>'),
    ('Scroll Wheel Zoom', 'wheel_zoom', 'enable the scroll wheel to zoom the plot in or out'),
    ('Point Select', 'tap_select', 'click on individual points to select or unselect for masking/unmasking.<br/><i>also works with shift</i>'),
    ('Reset', 'reset', 'Reset the view, clearing any zoom or moves')
)

tools_without_select = (
    ("Move", 'move', 'drag the plot around to reposition it'),
    ('Box Zoom', 'box_zoom', 'drag a rectangle to zoom into that area of the plot'),
    ('Scroll Wheel Zoom', 'wheel_zoom', 'enable the scroll wheel to zoom the plot in or out'),
    ('Reset', 'reset', 'Reset the view, clearing any zoom or moves')
)


FIT1D_PARAMETERS_HELP_WITHOUT_GROW = """
<dt>Function</dt>
<dd>
    Function to fit (Chebyshev polynomial or cubic spline). May not be
    configurable.
</dd>
<dt>Order</dt>
<dd>
    Order of fit (either polynomial degree or number of spline pieces)
</dd>
<dt>Max Iterations</dt>
<dd>
    Maximum number of rejection iterations if sigma clipping is enabled
</dd>
<dt>Sigma Clip, Upper, Lower</dt>
<dd>
    Enables sigma rejection with individually settable upper and lower
    sigma bounds
</dd>
"""


FIT1D_PARAMETERS_HELP_WITH_GROW = FIT1D_PARAMETERS_HELP_WITHOUT_GROW + """
<dt>Grow</dt>
<dd>
    Radius within which reject pixels adjacent to sigma-clipped pixels
</dd>
"""


PLOT_TOOLS_WITH_SELECT_HELP_SUBTEXT = """
<h3>Plot Tools</h3>

<p>
<div class="plot_tools_help"><div>""" + \
    '\n'.join(_plot_tool(t[0], t[1]) for t in tools_with_select) + \
"""
</div></div>
Data points in the upper plot may be selected in order to mask or
unmask them from consideration.  To select, choose the <i>Box Select</i>, 
<i>Point Select</i>, or <i>Free-Select</i> tool to the right of the figure.  
Selections may be additive if you hold down the shift key.  Once you have a 
selection, you may <b>mask</b> or <b>unmask</b> the selection by hitting 
the <b>M</b> or <b>U</b> key respectively.
</p>
<dl>""" + \
    '\n'.join('<dt>' + t[0] + '</dt><dd>' + t[2] + '</dd>' for t in tools_with_select) + \
 """
</dl>
<br clear="all"/>"""


PLOT_TOOLS_HELP_SUBTEXT = """
<h3>Plot Tools</h3>

<p>
<div class="plot_tools_help"><div>""" + \
    '\n'.join(_plot_tool(t[0], t[1]) for t in tools_without_select) + \
"""
</div></div>
</p>
<dl>""" + \
    '\n'.join('<dt>' + t[0] + '</dt><dd>' + t[2] + '</dd>' for t in tools_without_select) + \
 """
</dl>
<br clear="all"/>"""


REGION_EDITING_HELP_SUBTEXT = """
<h3>Region Editing</h3>

<p>
In addition to the region edit text box, you can edit regions interactively
on the upper figure.  To start a new region, hover the mouse where you want
one edge of the region and hit <b>R</b>.  Then move to the other end of the
desired region and hit <b>R</b> again.  To edit an existing region, hit <b>E</b>
while the mouse is near the edge you wish to adjust.  To delete a region, hit
<b>D</b> while close to the region you want removed.  The <i>Regions</i>
text entry will also update with these changes and you may fine tune the 
results there as well.
</p>
"""


CALCULATE_SENSITIVITY_HELP_TEXT = """
<h2>Help</h2>
<p>
    This primitive calculates the overall sensitivity of the system
    (instrument, telescope, detector, etc) for each wavelength using
    spectrophotometric data. It is obtained using the ratio
    between the observed data and the reference look-up data, providing
    a relationship between electrons per second on the detector and
    flux from the astronomical target. A smooth function is fitted to
    logarithmic values of this data and will be interpolated to provide
    a value for each wavelength when the fluxCalibrate primitive is run.
</p>
<h3>Fitting parameters</h3>
<dl>""" + FIT1D_PARAMETERS_HELP_WITHOUT_GROW + """
<dt>Regions</dt>
<dd>
    Comma-separated list of colon-separated wavelength (not pixel) pairs
    indicating the region(s) over which the input data should be
    used. The first and last values can be blank, indicating to
    continue to the end of the data.
</dd>
</dl>
""" + PLOT_TOOLS_WITH_SELECT_HELP_SUBTEXT + REGION_EDITING_HELP_SUBTEXT


DETERMINE_WAVELENGTH_SOLUTION_HELP_TEXT = """
<h2>Help</h2>
<p>
    This primitive provides wavelength calibration from a reference
    spectrum (usually of an arc lamp) by identifying peaks in a spectrum
    extracted along the dispersion direction and matching them to features
    with known wavelengths, then fitting a Chebyshev function.
</p>
<p>
    Three plots are shown in the middle of the page. The top plot shows the
    extracted 1D spectrum, with identified lines labeled with their
    wavelengths. The middle plot shows the non-linear component to the fit,
    while the bottom plot shows the residuals about this fit. Some lines in
    the specturm may have been identified but then rejected in subsequent
    iterations (if sigma-clipping is turned on), and these will be shown in
    a different color.
</p>
<p>
    Incorrect line identifications can be deleted in the top plot by pressing
    the <b>D</b> key close to it. A peak in the spectrum can be assigned a
    reference wavelength (identified) with the <b>I</b> key. This will
    activate the dropdown menu and text box in below the top plot, and
    indicate the pixel location of the peak and its wavelength according to
    the current fit. Up to five lines from the reference linelist will be
    available in the dropdown menu, with the closest one selected and
    also present in the text box. You may select this, or one of the other
    lines from the menu, or enter a wavelength directly in the text box,
    and click "OK". You can also decide not to add this line to the fit
    (perhaps if the wrong peak was highlighted) with the "Cancel" button.
    Note that the wavelength entered must be a value that maintains a
    monotonic increase or decrease of wavelength with pixel location so,
    for example, if you identify a line between two lines with wavelength
    identifications, its wavelength must lie between those two
    wavelengths.
</p>
<p>
    The "Identify lines" button will try to assign wavelengths to peaks
    in the spectrum that are not identified. Due to the way the lines are
    identified when constructing the initial fit, this may add new
    line identifications if run immediately after the interactive window
    opens.
</p>
<p>
    In addition, individual points can be masked (excluded from the fit) and
    unmasked in the middle plot by using the <b>M</b> and <b>U</b> keys,
    respectively. A masked point is still plotted in the lower two figures,
    and is still considered when assessing the monotonicity criterion for
    adding new lines. In general then, points should be masked if their
    identification is correct but they hamper the fit (perhaps the reference
    wavelength is incorrect due to the peak in the spectrum being a blend of
    more than one line), whereas a line should be deleted if the
    identification is wrong.
</p>
<h3>Fitting parameters</h3>
<dl>
""" + FIT1D_PARAMETERS_HELP_WITHOUT_GROW + """
</dl>""" + PLOT_TOOLS_WITH_SELECT_HELP_SUBTEXT.replace("upper", "central")


NORMALIZE_FLAT_HELP_TEXT = """
<h2>Help</h2>
<p>
    This primitive normalizes a GMOS Longslit spectroscopic flatfield
    in a manner similar to that performed by gsflat in Gemini-IRAF.
    A function is fitted along the dispersion direction of each
    row, separately for each CCD.
</p><p>
    For Hamamatsu CCDs, 21 unbinned columns at each CCD edge are
    masked out.
</p>
<h3>Fitting parameters</h3>
<dl>""" + FIT1D_PARAMETERS_HELP_WITH_GROW + """
<dt>Regions</dt>
<dd>
    Comma-separated list of colon-separated pixel coordinate pairs
    indicating the region(s) over which the input data should be
    used. The first and last values can be blank, indicating to
    continue to the end of the data.
</dd>
</dl>
""" + PLOT_TOOLS_HELP_SUBTEXT + REGION_EDITING_HELP_SUBTEXT


DEFAULT_HELP = """

<h2>Help</h2>

<p>DRAGONS Interactive Tools provide an interactive web interface to adjust
the data reduction parameters with a preview of the results.  This system
runs in your browser using a local bokeh server.  Adjust the parameters
to your liking and click the <b>Accept</b> button to continue.</p>
"""

TRACE_APERTURES = """
    <h1>Help for traceApertures</h1>

    <p> Traces the spectrum in 2D spectral images for each aperture center 
        stored in the APERTURE on each extension. The tracing starts at the 
        brightest region, instead of one of the edges of the detector. This 
        allows overcoming issues with sources with (almost) no flux in the 
        blue/red extremes. </p> 

    <p> The leftmost panel, named Tracing Parameters, in the Web User Interface 
        contains parameters used to perform the tracing, i.e., to follow how the 
        position in the spatial direction of our target changes along the 
        spectral direction. The Tracing Parameters are applied to all 
        appertures. </p>

    <p> You can find the traced data in the top plot where X represents the 
        pixels in the spectral direction and Y the pixels in the spatial 
        direction. Each traced data is represented by a black circle. </p>

    <p> You can perform a new tracing by changing the Tracing Parameters and 
        by clicking on the Trace Apertures button. Tracing can take a few 
        seconds deppending on your input parameters. If tracing fails, your will 
        receive an error message and the Web UI will return to the previous 
        working state. </p>

    <p> The red line in the top plot shows the function that better represents 
        how our target's spatial position varies continuously along the 
        dispersion direction, following the traced data using a Chebyshev 
        function. <p>  

    <p> You can change the parameters in the rightmost column within each tab, 
        which contains the Fitting Parameters for each APERTURE. If you change 
        a parameter, this primitive will fit again using the most recent parameters 
        and update the line in the plot area. </p>

    <p> For both Tracing Parameters and Fitting Parameters, you will find a 
        reset button. Each reset button only resets the parameters in the same 
        column it belongs. </p>        

    <p> Once you are satisfied with the tracing and the fit, press the Accept 
        button at the top right to continue your data reduction using the 
        parameters on screen. </p>

    <h2> Tracing Parameters: </h2>
    <dl>
        <dt> Max Missed </dt>
        <dd> Maximum number of steps to miss before a line is lost. </dd> 

        <dt> Max Shifted </dt>
        <dd> Maximum shift per pixel in line position. </dd>

        <dt> Number of Lines to Sum </dt>
        <dd> Number of lines to sum. </dd> 

        <dt> Tracing Step </dt>
        <dd> Step in rows/columns for tracing. </dd>
    </dl>

    <h2> Fitting Parameters </h2>
    <dl> 
        <dt> Function </dt>
        <dd> This is the Function used to fit the traced data. For this 
        primitive, we use Chebyshev. </dd>

        <dt> Order </dt>
        <dd> Order of Chebyshev function. </dd> 

        <dt> Max Iteractions </dt>
        <dd> Maximum number of rejection iterations. You can skip data rejection
             if you set this parameter to Zero. </dd>

        <dt> Sigma Clip </dt> 
        <dd> Reject outliers using sigma-clip. </dd>

        <dt> Sigma (Lower) </dt>
        <dd> Number of sigma used as lower threshold. </dd>

        <dt> Sigma (Upper) </dt>
        <dd> Number of sigma used as upper threshold/ </dd>

        <dt> Grow </dt> 
        <dd> If a point is rejected, then any points within a distance grow get 
             rejected too. </dd>

    </dl>
    """


SKY_CORRECT_FROM_SLIT_HELP_TEXT = """
<h2>Help</h2>
<p>
    NOT WRITTEN YET!!!!
</p>
<h3>Fitting parameters</h3>
<dl>""" + FIT1D_PARAMETERS_HELP_WITH_GROW + """
<dt>Regions</dt>
<dd>
    Comma-separated list of colon-separated pixel coordinate pairs
    indicating the region(s) over which the input data should be
    used. The first and last values can be blank, indicating to
    continue to the end of the data.
</dd>
</dl>
""" + PLOT_TOOLS_HELP_SUBTEXT + REGION_EDITING_HELP_SUBTEXT
