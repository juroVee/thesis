import ipywidgets as w

class Slider:
        pass

freq_slider = w.FloatSlider(
        value=2.,
        min=1.,
        max=10.0,
        step=0.1,
        description='Frequency:',
        readout_format='.1f')

range_slider = w.FloatRangeSlider(
        value=[-1., +1.],
        min=-5., max=+5., step=0.1,
        description='xlim:',
        readout_format='.1f')