""" module to test de core_fd parts of Arnica """

from copy import deepcopy

import numpy as np
import pytest

import arnica.utils.mesh_tool as msh
from arnica.solvers_2d.core_fd import Metrics2d
from arnica.solvers_2d.boundary import Boundary2d


@pytest.fixture
def setup_test_case_cyl():
    T_west = 500.
    T_east = 1500.

    MESH_CYL = {"kind": 'cyl',
                "r_min": 1.,
                "r_max": 2.,
                "theta_min": 0.,
                "theta_max": 2. * np.pi,
                "n_pts_rad": 15,
                "n_pts_tgt": 15
                }

    # Boundary conditions
    # Default values
    boundary = {"North": {"type": "Periodic", 'Values': {}},
                "West": {"type": "Periodic", 'Values': {}},
                "South": {"type": "Periodic", 'Values': {}},
                "East": {"type": "Periodic", 'Values': {}}}

    boundary["West"]["type"] = "Robin"
    boundary["West"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 500.}

    boundary["East"]["type"] = "Robin"
    boundary["East"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 1500.}

    # Input fields: Temperature, pressure, etc.
    field = {"absorption_coefficient": 1.,
             "temperature": [T_west, T_east]}

    # Create parameter dictionary
    params = {}
    params["boundaries"] = boundary
    params["field"] = field

    # Setup simulation with cylindrical mesh
    params["mesh"] = MESH_CYL

    return params


@pytest.fixture
def setup_test_case_cyl_diff_res_theta():
    T_west = 500.
    T_east = 1500.

    MESH_CYL = {"kind": 'cyl',
                "r_min": 1.,
                "r_max": 2.,
                "theta_min": 0.,
                "theta_max": 2. * np.pi,
                "n_pts_rad": 15
                }

    # Boundary conditions
    # Default values
    BOUNDARY = {"North": {"type": "Periodic", 'Values': {}},
                "West": {"type": "Periodic", 'Values': {}},
                "South": {"type": "Periodic", 'Values': {}},
                "East": {"type": "Periodic", 'Values': {}}}

    BOUNDARY["West"]["type"] = "Robin"
    BOUNDARY["West"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 500.}

    BOUNDARY["East"]["type"] = "Robin"
    BOUNDARY["East"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 1500.}

    # Input fields: Temperature, pressure, etc.
    FIELD = {"absorption_coefficient": 1.,
             "temperature": [T_west, T_east]}

    # Create parameter dictionary
    PARAMS = {}
    PARAMS["boundaries"] = BOUNDARY
    PARAMS["field"] = FIELD

    # Setup simulation with cylindrical mesh
    PARAMS["mesh"] = MESH_CYL

    return PARAMS


@pytest.fixture
def setup_test_case_rect_diff_res_x_y():
    T_west = 500.
    T_east = 1500.

    # Mesh definition
    MESH_RECT = {"kind": 'rect',
                 "x_max": 1.,
                 "y_max": 1.,
                 "x_res": 5.,
                 "y_res": 4.,
                 }

    # Boundary conditions
    # Default values
    BOUNDARY = {"North": {"type": "Periodic", 'Values': {}},
                "West": {"type": "Periodic", 'Values': {}},
                "South": {"type": "Periodic", 'Values': {}},
                "East": {"type": "Periodic", 'Values': {}}}

    BOUNDARY["West"]["type"] = "Robin"
    BOUNDARY["West"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 500.}

    BOUNDARY["East"]["type"] = "Robin"
    BOUNDARY["East"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 1500.}

    # Input fields: Temperature, pressure, etc.
    FIELD = {"absorption_coefficient": 1.,
             "temperature": [T_west, T_east]}

    # Create parameter dictionary
    PARAMS = {}
    PARAMS["boundaries"] = BOUNDARY
    PARAMS["field"] = FIELD

    # Setup simulation with rectangular mesh
    PARAMS["mesh"] = MESH_RECT

    return PARAMS


@pytest.fixture
def setup_test_case_rect():
    T_west = 500.
    T_east = 1500.

    # Mesh definition
    MESH_RECT = {"kind": 'rect',
                 "x_max": 1.,
                 "y_max": 1.,
                 "x_res": 5.,
                 "y_res": 5.,
                 }

    # Boundary conditions
    # Default values
    BOUNDARY = {"North": {"type": "Periodic", 'Values': {}},
                "West": {"type": "Periodic", 'Values': {}},
                "South": {"type": "Periodic", 'Values': {}},
                "East": {"type": "Periodic", 'Values': {}}}

    BOUNDARY["West"]["type"] = "Robin"
    BOUNDARY["West"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 500.}

    BOUNDARY["East"]["type"] = "Robin"
    BOUNDARY["East"]["Values"] = {"Emissivity": 1.,
                                  "Wall_temperature": 1500.}

    # Input fields: Temperature, pressure, etc.
    FIELD = {"absorption_coefficient": 1.,
             "temperature": [T_west, T_east]}

    # Create parameter dictionary
    PARAMS = {}
    PARAMS["boundaries"] = BOUNDARY
    PARAMS["field"] = FIELD

    # Setup simulation with rectangular mesh
    PARAMS["mesh"] = MESH_RECT

    return PARAMS


def test_perio_ns(setup_test_case_cyl):
    """test NS periodicity"""
    dict_test_perio = deepcopy(setup_test_case_cyl)

    dict_test_perio["boundaries"]["North"]["type"] = "Periodic"
    dict_test_perio["boundaries"]["South"]["type"] = "Periodic"
    dict_test_perio["boundaries"]["West"]["type"] = "Robin"
    dict_test_perio["boundaries"]["East"]["type"] = "Robin"

    bnd = Boundary2d(dict_test_perio["boundaries"])

    assert bnd.periodic_ns == True


def test_perio_we(setup_test_case_cyl):
    """test WE periodicity"""
    dict_test_perio = deepcopy(setup_test_case_cyl)

    dict_test_perio["boundaries"]["West"]["type"] = "Periodic"
    dict_test_perio["boundaries"]["East"]["type"] = "Periodic"
    dict_test_perio["boundaries"]["North"]["type"] = "Robin"
    dict_test_perio["boundaries"]["South"]["type"] = "Robin"

    bnd = Boundary2d(dict_test_perio["boundaries"])

    assert bnd.periodic_we == True


def test_no_perio(setup_test_case_cyl):
    """test no periodicity"""
    dict_test_perio = deepcopy(setup_test_case_cyl)

    dict_test_perio["boundaries"]["West"]["type"] = "Neumann"
    dict_test_perio["boundaries"]["East"]["type"] = "Neumann"
    dict_test_perio["boundaries"]["North"]["type"] = "Robin"
    dict_test_perio["boundaries"]["South"]["type"] = "Robin"

    bnd = Boundary2d(dict_test_perio["boundaries"])

    assert bnd.periodic_we == False
    assert bnd.periodic_ns == False


def test_perio_wrong_bc_definition(setup_test_case_cyl):
    """test wrong bc definition"""
    dict_test_perio = deepcopy(setup_test_case_cyl)

    dict_test_perio["boundaries"]["West"]["type"] = "Periodic"
    dict_test_perio["boundaries"]["North"]["type"] = "Periodic"
    dict_test_perio["boundaries"]["East"]["type"] = "Robin"
    dict_test_perio["boundaries"]["South"]["type"] = "Robin"

    with pytest.raises(IOError):
        Boundary2d(dict_test_perio["boundaries"])


def test_perio_error_only_1_perio_defined(setup_test_case_cyl):
    """test wrong bc definition"""
    dict_test_perio = deepcopy(setup_test_case_cyl)

    dict_test_perio["boundaries"]["West"]["type"] = "Periodic"
    dict_test_perio["boundaries"]["North"]["type"] = "Neumann"
    dict_test_perio["boundaries"]["East"]["type"] = "Robin"
    dict_test_perio["boundaries"]["South"]["type"] = "Robin"

    with pytest.raises(IOError):
        Boundary2d(dict_test_perio["boundaries"])


def test_bc_type(setup_test_case_cyl):
    """test wrong bc implemented"""
    implemented_bc = ["Dirichlet", "Neumann", "Robin", "Periodic"]
    dict_test_perio = deepcopy(setup_test_case_cyl)

    dict_test_perio["boundaries"]["West"]["type"] = "Dirichlet"
    dict_test_perio["boundaries"]["North"]["type"] = "Dirichlet"
    dict_test_perio["boundaries"]["East"]["type"] = "Neumann"
    dict_test_perio["boundaries"]["South"]["type"] = "Robin"

    bnd = Boundary2d(dict_test_perio["boundaries"])

    for bc_name in bnd.boundary_params.keys():
        assert bnd.boundary_params[bc_name]["type"] in implemented_bc


@pytest.fixture
def metric_cyl(setup_test_case_cyl):
    """
    Radiation solver (P1 Approximation)

    Parameters :
    ------------
    params : dict of setup parameters

    """
    params = deepcopy(setup_test_case_cyl)
    x_coor, y_coor = msh.get_mesh(params["mesh"])
    print("Shape of x_coor (cyl)")
    print(x_coor.shape)

    bnd = Boundary2d(params["boundaries"])

    print("\n\tmain ---> Compute Metrics")
    metric = Metrics2d(x_coor, y_coor, periodic_ns=bnd.periodic_ns,
                       periodic_we=bnd.periodic_we)

    return metric


@pytest.fixture
def metric_cyl_diff_res_x_y(setup_test_case_cyl_diff_res_theta):
    """
    Radiation solver (P1 Approximation)

    Parameters :
    ------------
    params : dict of setup parameters

    """
    params = deepcopy(setup_test_case_cyl_diff_res_theta)
    x_coor, y_coor = msh.get_mesh(params["mesh"])
    print("Shape of x_coor (cyl)")
    print(x_coor.shape)

    bnd = Boundary2d(params["boundaries"])

    print("\n\tmain ---> Compute Metrics")
    metric = Metrics2d(x_coor, y_coor, periodic_ns=bnd.periodic_ns,
                       periodic_we=bnd.periodic_we)

    return metric


@pytest.fixture
def metric_rect(setup_test_case_rect):
    """
    Radiation solver (P1 Approximation)

    Parameters :
    ------------
    params : dict of setup parameters

    """
    params = deepcopy(setup_test_case_rect)
    x_coor, y_coor = msh.get_mesh(params["mesh"])

    bnd = Boundary2d(params["boundaries"])

    metric = Metrics2d(x_coor,
                       y_coor,
                       periodic_ns=bnd.periodic_ns,
                       periodic_we=bnd.periodic_we)

    return metric


@pytest.fixture
def metric_rect_diff_res_x_y(setup_test_case_rect_diff_res_x_y):
    """
    Radiation solver (P1 Approximation)

    Parameters :
    ------------
    params : dict of setup parameters

    """
    params = deepcopy(setup_test_case_rect_diff_res_x_y)
    x_coor, y_coor = msh.get_mesh(params["mesh"])

    bnd = Boundary2d(params["boundaries"])

    metric = Metrics2d(x_coor,
                       y_coor,
                       periodic_ns=bnd.periodic_ns,
                       periodic_we=bnd.periodic_we)

    return metric


def test_Metrics2d_grad_x_vs_grad_x_csr_rect(metric_rect):
    """test gradx vs gradx_csr for resx=resy with rect mesh"""
    metric_rect.check_compute_matrices()
    grad_x = metric_rect.grad_x_slow.toarray()
    grad_x_csr = metric_rect.grad_x_csr.toarray()
    assert np.allclose(grad_x, grad_x_csr)


def test_Metrics2d_grad_y_vs_grad_y_csr_rect(metric_rect):
    """test grady vs gradx_csr for resx=resy with rect mesh"""
    metric_rect.check_compute_matrices()
    grad_y = metric_rect.grad_y_slow.toarray()
    grad_y_csr = metric_rect.grad_y_csr.toarray()
    assert np.allclose(grad_y, grad_y_csr)


def test_Metrics2d_grad_x_vs_grad_x_csr_rect_diff_res_x_y(
        metric_rect_diff_res_x_y):
    """Check if csr is correctly implemented for gradx in diff res rect"""
    metric_rect_diff_res_x_y.check_compute_matrices()
    grad_x = metric_rect_diff_res_x_y.grad_x_slow.toarray()
    grad_x_csr = metric_rect_diff_res_x_y.grad_x_csr.toarray()
    assert np.allclose(grad_x, grad_x_csr)


def test_Metrics2d_grad_y_vs_grad_y_csr_rect_diff_res_x_y(
        metric_rect_diff_res_x_y):
    """Check if csr is correctly implemented for grady in diff res rect"""
    metric_rect_diff_res_x_y.check_compute_matrices()
    grad_y = metric_rect_diff_res_x_y.grad_y_slow.toarray()
    grad_y_csr = metric_rect_diff_res_x_y.grad_y_csr.toarray()
    assert np.allclose(grad_y, grad_y_csr)


def test_Metrics2d_grad_x_vs_grad_x_csr_cyl_diff_res_x_y(
        metric_cyl_diff_res_x_y):
    """Check if csr is correctly implemented for gradx in diff res cyl"""
    metric_cyl_diff_res_x_y.check_compute_matrices()
    grad_x = metric_cyl_diff_res_x_y.grad_x_slow.toarray()
    grad_x_csr = metric_cyl_diff_res_x_y.grad_x_csr.toarray()
    assert np.allclose(grad_x, grad_x_csr)


def test_Metrics2d_grad_y_vs_grad_y_csr_cyl_diff_res_x_y(
        metric_cyl_diff_res_x_y):
    """Check if csr is correctly implemented for grady in diff res cyl"""
    metric_cyl_diff_res_x_y.check_compute_matrices()
    grad_y = metric_cyl_diff_res_x_y.grad_y_slow.toarray()
    grad_y_csr = metric_cyl_diff_res_x_y.grad_y_csr.toarray()
    assert np.allclose(grad_y, grad_y_csr)
