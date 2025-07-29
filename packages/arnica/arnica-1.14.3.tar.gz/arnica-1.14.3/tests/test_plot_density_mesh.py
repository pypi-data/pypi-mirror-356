"""Test plot density mesh"""
import numpy as np
from arnica.utils import plot_density_mesh as pdm
import pytest

@pytest.mark.skip(reason="Need to investigate? How to test functions in function")
def test_get_bins():

	x_coord = [0, .5,  1,  0, .5,  1,  0,  1]
	y_coord = [0,  0,  0,  1,  1,  1, .5, .5]
	z_coord = [0,  0,  0,  0,  0,  0,  0,  0]

	#Testing _get_bins

	a,b = pdm.get_bins(x_coord, y_coord)
	assert((a,b) == (500,500))

def test_scatter_plot_mesh():
	x_coord = [0, .5,  1,  0, .5,  1,  0,  1]
	y_coord = [0,  0,  0,  1,  1,  1, .5, .5]
	z_coord = [0,  0,  0,  0,  0,  0,  0,  0]
	pdm.scatter_plot_mesh(x_coord, y_coord, z_coord, axisym=False, show=False)
	pdm.scatter_plot_mesh(x_coord, y_coord, z_coord, axisym=True, show=False)

