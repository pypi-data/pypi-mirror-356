
import numpy as np
from arnica.utils.showy import showy


def test_showy():
    """Damo of a simplified set of graphs with showy"""
    data = dict()
    data["time"] = np.linspace(0, 0.1, num=256)

    freq = 10.
    for freq in np.linspace(10, 20, num=9):
        data["sine_" + str(freq)] = np.cos(data["time"] * freq * 2 * np.pi)

    # Creating a template
    template = {
        "title": "Example",
        "graphs": [{
            "curves": [{"var": "sine_*"}],
            "x_var": "time",
            "y_label": "Sine [mol/m³/s]",
            "x_label": "Time [s]",
            "title": "Sinus of frquency *"
        }],
        "figure_structure": [3, 3],
        "figure_dpi": 92.6
    }

    showy(template, data, data_c=None, show=False)
