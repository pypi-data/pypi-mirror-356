# import h5py
# import hdf5plugin # noqa: F401
from silx.io import h5py_utils
import os
from ewokscore import Task
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from PIL import Image


class TiffExporterFromRegrid(
    Task,
    input_names=[
        "regrid_uri",
        "output_path",
    ],
    optional_input_names=[
        "output_prefix",
        "output_suffix",
        "output_gallery_path",
    ],
    output_names=[],
):
    def run(self):
        regrid_uri = self.inputs.regrid_uri
        output_path = self.inputs.output_path
        output_prefix = self.get_input_value("output_prefix", "IMG_")
        output_suffix = self.get_input_value("output_suffix", "")
        output_gallery_path = self.get_input_value("output_gallery_path", None)

        os.makedirs(output_path, exist_ok=True)
        if output_gallery_path is not None:
            os.makedirs(output_gallery_path, exist_ok=True)

        uris = regrid_uri.split("::")
        input_filename = uris[0]
        grp = uris[1]

        with h5py_utils.open_item(input_filename, "/") as fd:  # type: ignore[reportGeneralTypeIssues]
            _res = fd[grp]
            is_nxdata = "NX_class" in _res.attrs and _res.attrs["NX_class"] == "NXdata"

            while not is_nxdata:
                _res = _res[_res.attrs["default"]]
                is_nxdata = (
                    "NX_class" in _res.attrs and _res.attrs["NX_class"] == "NXdata"
                )

            grps = []
            if "signal" in _res.attrs:
                grps += [
                    _res.attrs["signal"],
                ]

            if "auxiliary_signals" in _res.attrs:
                grps += list(_res.attrs["auxiliary_signals"])

            kwargs = {}
            axes = []
            axnames = []
            if "axes" in _res.attrs:
                resolutions = []
                for a in _res.attrs["axes"]:
                    axnames += [
                        a,
                    ]
                    d = np.array(_res[a])
                    axes += [
                        d,
                    ]
                    resolutions += [
                        1e4 / float(np.mean(np.diff(d))),
                    ]

                kwargs["resolution_unit"] = 3
                kwargs["resolution"] = resolutions

            cmap = "jet"

            for g in grps:
                data = np.array(_res[g], dtype=np.float32)
                im = Image.fromarray(data, mode="F")
                gg = g.replace(" ", "_")
                im.save(
                    os.path.join(
                        output_path, f"{output_prefix}{gg}{output_suffix}.tiff"
                    ),
                    **kwargs,
                )

                # ArraySave.save2DArrayListAsMonochromaticTiff([data], os.path.join(output_path, f"{output_prefix}{gg}.tiff"), dtype=np.float32)
                if output_gallery_path is not None:
                    norm = mpl.colors.Normalize(0, np.max(data))
                    f, ax = plt.subplots()
                    ax.pcolor(*axes, data, norm=norm, cmap=cmap)
                    ax.invert_yaxis()

                    if len(axnames) == 2:
                        ax.set_xlabel(f"{axnames[1]} (um)")
                        ax.set_ylabel(f"{axnames[0]} (um)")

                    f.suptitle(g)
                    f.colorbar(
                        mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                        ax=ax,
                        label="Areal mass density ($ng/mm^2$)",
                    )
                    f.savefig(
                        os.path.join(
                            output_gallery_path,
                            f"{output_prefix}{gg}{output_suffix}.jpg",
                        )
                    )
