import numpy as np
import pytest
import amd


def test_AMD(reference_data):
    for name in reference_data:
        for s in reference_data[name]:
            calc_amd = amd.AMD(s["PeriodicSet"], 100)

            if not np.allclose(calc_amd, s["AMD100"]):
                n = s["PeriodicSet"].name
                ref_amd = str(s["AMD100"])

                pytest.fail(
                    f"AMD of structure {n} disagrees with reference. "
                    f"reference: {ref_amd}, calculated: {calc_amd}"
                )


def test_PDD(reference_data):
    for name in reference_data:
        for s in reference_data[name]:
            calc_pdd = amd.PDD(s["PeriodicSet"], 100, lexsort=False)

            # Not ideal, but it seems different Python versions can make
            # floating point changes that reorders the rows of the PDD.
            if not np.allclose(calc_pdd, s["PDD100"]):
                # if not amd.EMD(s["PDD100"], calc_pdd) < 1e-14:
                abs_diffs = np.abs(calc_pdd - s["PDD100"])
                diffs = str(np.sort(abs_diffs.flatten())[::-1][:10])
                n = s["PeriodicSet"].name
                ref_pdd = str(s["PDD100"])

                pytest.fail(
                    f"PDD of structure {n} disagrees with reference; "
                    f"reference: {ref_pdd}, calculated: {calc_pdd}; "
                    f"Largest elementwise diff between PDDs: {diffs}; "
                    f"PDD EMD: {amd.EMD(s['PDD100'], calc_pdd)}"
                )


def test_PDD_to_AMD(reference_data):
    for name in reference_data:
        for s in reference_data[name]:
            calc_pdd = amd.PDD(s["PeriodicSet"], 100, lexsort=False)
            calc_amd = amd.AMD(s["PeriodicSet"], 100)
            amd_from_pdd = amd.PDD_to_AMD(calc_pdd)

            if not np.allclose(calc_amd, amd_from_pdd):
                n = s["PeriodicSet"].name
                pytest.fail(
                    f"Directly calculated AMD of structure {n} disagrees "
                    "with AMD calculated from PDD."
                )


def test_AMD_finite():
    trapezium = np.array([[0, 0], [1, 1], [3, 1], [4, 0]])
    kite = np.array([[0, 0], [1, 1], [1, -1], [4, 0]])
    trap_amd = amd.AMD_finite(trapezium)
    kite_amd = amd.AMD_finite(kite)
    dist = np.linalg.norm(trap_amd - kite_amd)

    if not abs(dist - 0.6180339887498952) < 1e-16:
        pytest.fail(
            "AMDs of finite sets trapezium and kite are different than expected."
        )


def test_PDD_finite():
    trapezium = np.array([[0, 0], [1, 1], [3, 1], [4, 0]])
    kite = np.array([[0, 0], [1, 1], [1, -1], [4, 0]])
    trap_pdd = amd.PDD_finite(trapezium)
    kite_pdd = amd.PDD_finite(kite)
    dist = amd.EMD(trap_pdd, kite_pdd)

    if not abs(dist - 0.874032045) < 1e-8:
        pytest.fail(
            "PDDs of finite sets trapezium and kite are different than " "expected."
        )
