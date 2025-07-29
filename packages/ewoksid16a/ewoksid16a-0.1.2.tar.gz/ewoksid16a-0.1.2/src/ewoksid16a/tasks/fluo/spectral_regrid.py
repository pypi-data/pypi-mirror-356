import h5py
import hdf5plugin  # noqa: F401
from silx.io import h5py_utils
import numpy as np
from ewokscore import Task


class SpectralRegrid(
    Task,
    input_names=["bliss_scan_uri", "output_root_uri", "counter_name"],
    optional_input_names=[],
    output_names=["bliss_scan_uri", "output_root_uri"],
):
    """Regrid raw spectrums"""

    def run(self):
        _uris = self.inputs.bliss_scan_uri.split("::")
        filename_src = _uris[0]
        scan_src = _uris[1]
        cntnam = self.inputs.counter_name

        fscanuri = f"{scan_src}/instrument/fscan_parameters"

        print(f"Waiting to open {filename_src}")
        with h5py_utils.open_item(filename_src, "/") as fd:  # type: ignore[reportGeneralTypeIssues]
            print(f"{filename_src} open!")
            fastmot = fd[f"{fscanuri}/fast_motor"][()].decode()
            mode = fd[f"{fscanuri}/fast_motor_mode"][()].decode()
            fast_n = int(fd[f"{fscanuri}/fast_npoints"][()].decode())
            slow_n = int(fd[f"{fscanuri}/slow_npoints"][()].decode())

            cnt = fd[f"{scan_src}/instrument/{cntnam}/data"]
            cnt_shape = cnt.shape
            cnt_dtype = cnt.dtype

        A = np.arange(fast_n * slow_n)
        A.shape = (fast_n, slow_n)

        if fastmot.endswith("z"):
            A = A.swapaxes(0, 1)

        if mode == "ZIGZAG":
            A[1::2, :] = A[1::2, :][:, ::-1]

        _uris = self.inputs.output_root_uri.split("::")
        filename = _uris[0]
        scan = _uris[1]

        print(f"Waiting to open {filename}")
        with h5py_utils.open_item(filename, "/", mode="a") as fd:  # type: ignore[reportGeneralTypeIssues]
            print(f"{filename} open!")
            grp = fd
            S = scan.split("/")

            for i, s in enumerate(S):
                if s == "":
                    continue

                grp = grp.require_group(s)

                if i == len(S) - 1:
                    grp.attrs.update(
                        {
                            "NX_class": "NXdata",
                            "signal": "data",
                            "interpretation": "image",
                        }
                    )
                else:
                    grp.attrs.update({"NX_class": "NXcollection", "default": S[i + 1]})

            virtual = False

            if not virtual:
                ds = np.empty(shape=(cnt_shape[1], *A.shape), dtype=cnt_dtype)

                #                with h5py_utils.open_item(filename_src, f"{scan_src}/instrument/{cntnam}/data", mode='r') as src:
                src = fd[f"{scan_src}/instrument/{cntnam}/data"]
                for i in range(cnt_shape[0]):
                    ds[(slice(None), *np.unravel_index(i, A.shape))] = src[A.flat[i]]

                grp.create_dataset(
                    "data",
                    data=ds,
                    chunks=(1, *A.shape),
                    shuffle=True,
                    compression="gzip",
                )

            else:
                layout = h5py.VirtualLayout(
                    shape=(
                        cnt_shape[1],
                        *A.shape,
                    ),
                    dtype=cnt_dtype,
                )
                layoutpymca = h5py.VirtualLayout(
                    shape=(
                        *A.shape,
                        cnt_shape[1],
                    ),
                    dtype=cnt_dtype,
                )
                vsource = h5py.VirtualSource(
                    filename_src,
                    f"{scan_src}/instrument/{cntnam}/data",
                    shape=cnt_shape,
                    dtype=cnt.dtype,
                )

                for i in range(cnt_shape[0]):
                    # print(np.unravel_index(i, A.shape), layout.shape, vsource[A.flat[i]].shape)

                    layout[(slice(None), *np.unravel_index(i, A.shape))] = vsource[
                        A.flat[i]
                    ]
                    layoutpymca[(*np.unravel_index(i, A.shape), slice(None))] = vsource[
                        A.flat[i]
                    ]
                grp.create_virtual_dataset("data", layout, fillvalue=-1)
                grp.create_virtual_dataset("pymca", layoutpymca, fillvalue=-1)
