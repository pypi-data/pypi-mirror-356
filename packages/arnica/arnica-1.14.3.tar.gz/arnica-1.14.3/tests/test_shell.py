""" Module testing Shell, AxiShel et CartShell methods """
import pytest
import os
import numpy as np
import h5py
from arnica.utils.axishell_2 import AxiShell
from arnica.utils.cartshell_3 import CartShell

def test_shell(datadir):
    """ Test of Shell methods by the mean of an AxiShell """

    ctrl_pts_x = (0.0, 0.2)
    ctrl_pts_r = (0.12, 0.12)
    shell = AxiShell(11, 11, 40.0, ctrl_pts_x, ctrl_pts_r)

    #Testing add_curviwidth
    width_profile = ((0.0, -0.04),
                     (0.2, -0.04),
                     (0.4, -0.07),
                     (0.6, -0.04),
                     (0.8, -0.04))
    shell.add_curviwidth('width_profile', width_profile)
    target_val = [-0.04, -0.04, -0.04, -0.055, -0.07, -0.055, -0.04, -0.04,
                  -0.04, -0.04, -0.04]
    np.testing.assert_allclose(shell.width_matrix['width_profile'][0], target_val)

    #Testing bake_millefeuille
    cake = shell.bake_millefeuille('width_profile', 3)
    target_val = [[0.00666667, 0.01333333, 0.00666667],
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
    np.testing.assert_allclose(cake['dz'][0], target_val, rtol=1e-5)

    #Testing average_on_shell_over_dirs
    np.random.seed(1)
    target_field = np.random.random((3, shell.shape[0], shell.shape[1])) #pylint: disable=no-member
    average = shell.average_on_shell_over_dirs(target_field, ['v', 'time'])
    target_val = [3.71048106e-05 ,7.33521695e-05, 8.52748890e-05, 8.09592620e-05,
                  8.20054358e-05, 6.79632056e-05, 7.66314353e-05, 7.87668173e-05,
                  8.60460952e-05, 7.16661617e-05, 4.32831721e-05]
    np.testing.assert_allclose(average, target_val, rtol=1e-5)
    average = shell.average_on_shell_over_dirs(target_field, ['v', 'time'], scale=False)
    target_val = [0.47320114, 0.4699923 , 0.55265719, 0.53329244,
                  0.52278534, 0.44020879, 0.51550363, 0.52670343,
                  0.55136021, 0.46839039, 0.57088887]
    np.testing.assert_allclose(average, target_val, rtol=1e-5)
    
    with pytest.raises(ValueError):
        shell.average_on_shell_over_dirs(target_field, ['v', 'k'])

    point_cloud = np.array([[0.1, 0.12, 0.0]])
    tolerance = 0.04
    mask = shell.set_mask_on_shell(point_cloud, tolerance)
    target_field = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    np.testing.assert_array_equal(mask, target_field)

    case = datadir
    path_actu = os.getcwd()
    os.chdir(case)

    shell.plot("fig.png")
    
    shell.dump_shell("shell")
    size_target = shell.shape[0] * shell.shape[1]
    with h5py.File("shell.h5", 'r') as fin:
        assert fin['mesh/x'][()].size == size_target
        assert fin['mesh/y'][()].size == size_target
        assert fin['mesh/z'][()].size == size_target
        assert fin['variables/r'][()].size == size_target
        assert fin['variables/theta'][()].size == size_target
        assert fin['variables/n_x'][()].size == size_target
        assert fin['variables/n_y'][()].size == size_target
        assert fin['variables/n_z'][()].size == size_target
        assert fin['variables/n_r'][()].size == size_target
        assert fin['variables/du'][()].size == size_target
        assert fin['variables/dv'][()].size == size_target
        assert fin['variables/dwu'][()].size == size_target
        assert fin['variables/dwv'][()].size == size_target
        assert fin['variables/surf'][()].size == size_target

    os.chdir(path_actu)
