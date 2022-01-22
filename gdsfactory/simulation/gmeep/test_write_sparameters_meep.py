"""test meep sparameters"""

import numpy as np
import pandas as pd

import gdsfactory as gf
import gdsfactory.simulation as sim
import gdsfactory.simulation.gmeep as gm
from gdsfactory.tech import LAYER_STACK


def test_sparameters_straight(dataframe_regression):
    """Checks Sparameters for a straight waveguide"""
    c = gf.components.straight(length=2)
    p = 3
    c = gf.add_padding_container(c, default=0, top=p, bottom=p)
    df = gm.write_sparameters_meep(c, overwrite=True, resolution=20)

    # Check reasonable reflection/transmission
    assert np.allclose(df["s12m"], 1, atol=1e-02)
    assert np.allclose(df["s21m"], 1, atol=1e-02)
    assert np.allclose(df["s11m"], 0, atol=5e-02)
    assert np.allclose(df["s22m"], 0, atol=5e-02)

    if dataframe_regression:
        dataframe_regression.check(df)


def test_sparameters_straight_symmetric(dataframe_regression):
    """Checks Sparameters for a straight waveguide"""
    c = gf.components.straight(length=2)
    p = 3
    c = gf.add_padding_container(c, default=0, top=p, bottom=p)
    # port_symmetries for straight
    port_symmetries = {
        "o1": {
            "s11": ["s22"],
            "s21": ["s12"],
        }
    }
    df = gm.write_sparameters_meep(
        c, overwrite=True, resolution=20, port_symmetries=port_symmetries
    )

    # Check reasonable reflection/transmission
    assert np.allclose(df["s12m"], 1, atol=1e-02)
    assert np.allclose(df["s21m"], 1, atol=1e-02)
    assert np.allclose(df["s11m"], 0, atol=5e-02)
    assert np.allclose(df["s22m"], 0, atol=5e-02)

    if dataframe_regression:
        dataframe_regression.check(df)


def test_sparameters_crossing_symmetric(dataframe_regression):
    """Checks Sparameters for a waveguide crossing. Exploits symmetries."""
    c = gf.components.crossing()
    port_symmetries = {
        "o1": {
            "s11": ["s22", "s33", "s44"],
            "s21": ["s12", "s34", "s43"],
            "s31": ["s13", "s24", "s42"],
            "s41": ["s14", "s23", "s32"],
        }
    }
    df = gm.write_sparameters_meep(
        c, overwrite=True, resolution=20, port_symmetries=port_symmetries
    )

    if dataframe_regression:
        dataframe_regression.check(df)


# def test_sparameterNxN_crossing(dataframe_regression):
#     """Checks that get_sparameterNxN properly sources, monitors,
#     and sweeps over the ports of all orientations
#     Uses low resolution 2D simulations to run faster
#     """
#     # c = gf.components.crossing()
#     c = gf.components.straight(length=2)
#     p = 3
#     c = gf.add_padding_container(c, default=0, top=p, bottom=p)
#     df = gm.write_sparameters_meep(c, overwrite=True, resolution=20)

#     # Check reciprocity
#     for i in range(1, len(c.ports) + 1):
#         for j in range(1, len(c.ports) + 1):
#             if i == j:
#                 continue
#             else:
#                 assert np.allclose(
#                     df["s{}{}m".format(i, j)].to_numpy(),
#                     df["s{}{}m".format(j, i)].to_numpy(),
#                     atol=1e-02,
#                 )
#                 assert np.allclose(
#                     df["s{}{}a".format(i, j)].to_numpy(),
#                     df["s{}{}a".format(j, i)].to_numpy(),
#                     atol=1e-02,
#                 )
#     if dataframe_regression:
#         dataframe_regression.check(df)


# def test_sparameterNxN_symmetries_straight(dataframe_regression):
#     """Checks the duplication of Sparameters when using port_symmetry toggle
#     Uses a straight to be faster than crossing, although crossing works well too
#     """

#     # No symmetry toggle
#     c = gf.components.straight(length=2)
#     p = 3
#     c = gf.add_padding_container(c, default=0, top=p, bottom=p)
#     start = time.time()
#     df = gm.write_sparameters_meep(
#         c,
#         overwrite=True,
#         resolution=50,  # Comparison needs higher resolution
#         animate=False,
#     )
#     stop = time.time()
#     time_full = stop - start

#     # port_symmetries for straight
#     port_symmetries = {
#         "o1": {
#             "s11": ["s22"],
#             "s21": ["s12"],
#         }
#     }
#     start = time.time()
#     df_symm = gm.write_sparameters_meep(
#         c,
#         overwrite=True,
#         animate=False,
#         resolution=50,  # Comparison needs higher resolution
#         port_symmetries=port_symmetries,
#     )
#     stop = time.time()
#     time_symm = stop - start

#     # Compare symmetry to no symmetry
#     for i in range(1, len(c.ports) + 1):
#         for j in range(1, len(c.ports) + 1):
#             assert np.allclose(
#                 df["s{}{}m".format(i, j)].to_numpy(),
#                 df_symm["s{}{}m".format(i, j)].to_numpy(),
#                 atol=5e-02,
#             )
#             assert np.allclose(
#                 df["s{}{}a".format(i, j)].to_numpy(),
#                 df_symm["s{}{}a".format(i, j)].to_numpy(),
#                 atol=5e-02,
#             )
#     # Check that it was shorter
#     assert time_full > time_symm

#     if dataframe_regression:
#         dataframe_regression.check(df_symm)


# def test_sparameterNxN_symmetries_crossing(dataframe_regression):
#     """Checks the duplication of Sparameters when using port_symmetry toggle
#     Uses a straight to be faster than crossing, although crossing works well too
#     """

#     # No symmetry toggle
#     c = gf.components.crossing()
#     # c = gf.components.straight(length=2)
#     # p = 3
#     # c = gf.add_padding_container(c, default=0, top=p, bottom=p)
#     start = time.time()
#     df = gm.write_sparameters_meep(
#         c,
#         overwrite=True,
#         resolution=50,  # Comparison needs higher resolution
#         animate=False,
#     )
#     stop = time.time()
#     time_full = stop - start

#     # port_symmetries for crossing
#     port_symmetries={
#             "o1": {
#                 "s11": ["s22", "s33", "s44"],
#                 "s21": ["s12", "s34", "s43"],
#                 "s31": ["s13", "s24", "s42"],
#                 "s41": ["s14", "s23", "s32"],
#             }
#         }
#     start = time.time()
#     df_symm = gm.write_sparameters_meep(
#         c,
#         overwrite=True,
#         animate=False,
#         resolution=50,  # Comparison needs higher resolution
#         port_symmetries=port_symmetries,
#     )
#     stop = time.time()
#     time_symm = stop - start

#     # Compare symmetry to no symmetry
#     for i in range(1, len(c.ports) + 1):
#         for j in range(1, len(c.ports) + 1):
#             assert np.allclose(
#                 df["s{}{}m".format(i, j)].to_numpy(),
#                 df_symm["s{}{}m".format(i, j)].to_numpy(),
#                 atol=5e-02,
#             )
#             assert np.allclose(
#                 df["s{}{}a".format(i, j)].to_numpy(),
#                 df_symm["s{}{}a".format(i, j)].to_numpy(),
#                 atol=5e-02,
#             )
#     # Check that it was shorter
#     assert time_full > time_symm

#     if dataframe_regression:
#         dataframe_regression.check(df)
#         dataframe_regression.check(df_symm)


def test_sparameters_straight_mpi(dataframe_regression):
    """Checks Sparameters for a straight waveguide using MPI"""
    c = gf.components.straight(length=2)
    p = 3
    c = gf.add_padding_container(c, default=0, top=p, bottom=p)
    filepath = gm.write_sparameters_meep_mpi(c, overwrite=True)
    df = pd.read_csv(filepath)

    # Check reasonable reflection/transmission
    assert np.allclose(df["s12m"], 1, atol=1e-02)
    assert np.allclose(df["s21m"], 1, atol=1e-02)
    assert np.allclose(df["s11m"], 0, atol=5e-02)
    assert np.allclose(df["s22m"], 0, atol=5e-02)

    if dataframe_regression:
        dataframe_regression.check(df)


def test_sparameters_straight_mpi_pool(dataframe_regression):
    """Checks Sparameters for a straight waveguide using an MPI pool"""

    components = []
    for length in [2]:
        c = gf.components.straight(length=length)
        p = 3
        c = gf.add_padding_container(c, default=0, top=p, bottom=p)
        components.append(c)

    filepaths = gm.write_sparameters_meep_mpi_pool(
        [{"component": c, "overwrite": True} for c in components],
    )

    filepath = filepaths[0]
    df = pd.read_csv(filepath)

    filepath2 = sim.get_sparameters_path_meep(component=c, layer_stack=LAYER_STACK)
    assert (
        filepath2 == filepaths[0]
    ), f"filepath returned {filepaths[0]} differs from {filepath2}"

    # Check reasonable reflection/transmission
    assert np.allclose(df["s12m"], 1, atol=1e-02)
    assert np.allclose(df["s21m"], 1, atol=1e-02)
    assert np.allclose(df["s11m"], 0, atol=5e-02)
    assert np.allclose(df["s22m"], 0, atol=5e-02)

    if dataframe_regression:
        dataframe_regression.check(df)


if __name__ == "__main__":
    test_sparameters_straight_mpi_pool(None)
    # test_sparameters_straight_mpi(None)
    # test_sparameter_straight(None)
    # test_sparameter_crossing(None)
    # test_sparameters_straight_symmetric(False)
    # test_sparameters_crossing_symmetric(False)
