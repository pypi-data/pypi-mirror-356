from pyread_swift import SwiftSnapshot
import os 
import numpy as np
import pytest

SWIFT_FNAME = "EAGLE_ICs_6.hdf5"
NPARTS = [800648, 830584, 0, 0, 29847, 53]
SKIP_PARTS = [2,3]

def _check_we_have_snapshot():
    exists = os.path.isfile(SWIFT_FNAME)
    if not exists:
        raise FileNotFoundError(
            "You have not downloaded the test snapshot, run 'get_ics.sh' first!"
        )

@pytest.mark.parametrize("att", ["Coordinates", "Masses"])
def test_read(att):

    # Check we have the example snapshot.
    _check_we_have_snapshot()

    # Swift read object.
    swift = SwiftSnapshot(SWIFT_FNAME)
    bs = swift.header["BoxSize"]

    for i in range(len(NPARTS)):
        if i in SKIP_PARTS: continue

        swift.select_region(i, 0, bs, 0, bs, 0, bs)
        swift.split_selection()
       
        # Load coordinates.
        data = swift.read_dataset(i, att)
    
        if att == "Coordinates":
            assert data.dtype == np.float64, f"Bad read parttype {i} (1)"
            assert data.shape == (NPARTS[i], 3), f"Bad read parttype {i} (2)"
        else:
            assert data.dtype == np.float32, f"Bad read parttype {i} (1)"
            assert data.shape == (NPARTS[i],), f"Bad read parttype {i} (2)"

def test_read_header():
    
    # Check we have the example snapshot.
    _check_we_have_snapshot()

    # Swift read object.
    swift = SwiftSnapshot(SWIFT_FNAME)

    assert swift.header["BoxSize"].dtype == np.float64
    assert swift.header["BoxSize"] == 4.235625
    assert np.array_equal(swift.header["NumPart_ThisFile"], swift.header["NumPart_Total"])
    for i in range(len(NPARTS)):
        if i in SKIP_PARTS: continue
        assert swift.header["NumPart_ThisFile"][i] == NPARTS[i]
