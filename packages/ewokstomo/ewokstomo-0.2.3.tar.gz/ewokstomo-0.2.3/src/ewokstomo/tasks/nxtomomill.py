from ewokscore import Task
import subprocess  # nosec: B404

from pathlib import Path


class H5ToNx(
    Task, input_names=["bliss_hdf5_path", "output_dir"], output_names=["nx_path"]
):

    def run(self):
        """
        Executes a subprocess that runs nxtomomill to convert the input_scan to nx format
        :return: The path to the created nx file
        """

        hdf5_path = Path(self.inputs.bliss_hdf5_path)
        output_dir = Path(self.inputs.output_dir)

        if not hdf5_path.is_file():
            raise FileNotFoundError(f"Input file not found: {hdf5_path}")

        command = [
            "nxtomomill",
            "h52nx",
            self.inputs.bliss_hdf5_path,
            self.inputs.output_dir,
        ]
        subprocess.run(
            command, capture_output=True, text=True, check=True, shell=False
        )  # nosec: B603
        self.outputs.nx_path = str(output_dir)
