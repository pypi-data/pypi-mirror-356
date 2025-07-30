from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
import subprocess
import shutil
import os


class build_shmw(_build_py):
    def run(self):
        # Compile shmw.c to shmw binary
        src = os.path.join("src", "tmuxer", "shmw.c")
        out = os.path.join("src", "tmuxer", "shmw")
        subprocess.check_call(["gcc", "-std=c11", "-Wall", "-O2", src, "-o", out])
        # Copy the binary to the tmux package directory so it is installed as package data
        package_dir = os.path.join(self.build_lib, "tmuxer")
        os.makedirs(package_dir, exist_ok=True)
        shutil.copy(out, os.path.join(package_dir, "shmw"))
        super().run()


setup(
    packages=["tmuxer"],
    package_dir={"": "src"},
    cmdclass={"build_py": build_shmw},
    include_package_data=True,
    package_data={"tmuxer": ["shmw"]},
)
