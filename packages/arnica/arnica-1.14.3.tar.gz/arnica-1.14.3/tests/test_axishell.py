import numpy as np
import os
from arnica.utils.axishell import AxiShell

def test_axishell(datadir):

	shell = AxiShell(11,11)
	shell.geom["angle"] = 40.0
	shell.geom["crtl_pts_x"] = (0.0, 0.2)
	shell.geom["crtl_pts_r"] = (0.12, 0.12)

	#Testing dump and load
	case = datadir
	path_actu = os.getcwd()
	os.chdir(case)

	shell.dump()
	loaded_shell = AxiShell(11,11)
	loaded_shell.load()
	np.testing.assert_allclose(loaded_shell.geom["crtl_pts_x"], 
							   shell.geom["crtl_pts_x"])
	os.chdir(path_actu)

	#Testing build_shell
	shell.build_shell()
	test_value = np.array([[ 0., 0.11276311, -0.04104242],
  				  [ 0.02, 0.11276311, -0.04104242],
				  [ 0.04, 0.11276311, -0.04104242],
				  [ 0.06, 0.11276311, -0.04104242],
				  [ 0.08, 0.11276311, -0.04104242],
				  [ 0.1 , 0.11276311, -0.04104242],
				  [ 0.12, 0.11276311, -0.04104242],
				  [ 0.14, 0.11276311, -0.04104242],
				  [ 0.16, 0.11276311, -0.04104242],
				  [ 0.18, 0.11276311, -0.04104242],
				  [ 0.2 , 0.11276311, -0.04104242]])
	np.testing.assert_allclose(shell.matrix['xyz'][0], test_value)

	#Testing add_curviwidth
	width_profile = ((0.0, -0.04),
                     (0.2, -0.04),
                     (0.4, -0.07),
                     (0.6, -0.04),
                     (0.8, -0.04))
	shell.add_curviwidth('width_profile',width_profile)
	test_value = [-0.04, -0.04, -0.04, -0.055, -0.07, -0.055, -0.04, -0.04, 
				  -0.04, -0.04, -0.04 ]
	np.testing.assert_allclose(shell.matrix['width_profile'][0], test_value)

	#Testing bake_millefeuille
	cake = shell.bake_millefeuille('width_profile', 3)
	test_value = [[0.00666667, 0.01333333, 0.00666667],
				  [0.00666667, 0.01333333, 0.00666667],
				  [0.00666667, 0.01333333, 0.00666667],
				  [0.00916667, 0.01833333, 0.00916667],
				  [0.01166667, 0.02333333, 0.01166667],
				  [0.00916667, 0.01833333, 0.00916667],
				  [0.00666667, 0.01333333, 0.00666667],
				  [0.00666667, 0.01333333, 0.00666667],
				  [0.00666667, 0.01333333, 0.00666667],
				  [0.00666667, 0.01333333, 0.00666667],
				  [0.00666667, 0.01333333, 0.00666667]]
	np.testing.assert_allclose(cake['dz'][0], test_value,rtol=1e-5)

	#Testing average_on_shell_over_dirs
	np.random.seed(1)
	test_field = np.random.random((3, shell.shape[0],
								 shell.shape[1]))
	average = shell.average_on_shell_over_dirs(test_field,['theta','time'])
	test_value = [0.47320114, 0.4699923,  0.55265719, 0.53329244, 0.52278534, 
	0.44020879, 0.51550363, 0.52670343, 0.55136021, 0.46839039, 0.57088887]
	np.testing.assert_allclose(average, test_value,rtol=1e-5)
