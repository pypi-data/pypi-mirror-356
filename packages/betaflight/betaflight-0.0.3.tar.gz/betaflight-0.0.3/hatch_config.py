from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import subprocess
import os

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        server_dir = os.path.join(os.path.dirname(__file__), "betaflight/firmware")
        subprocess.run(["make", "TARGET=SITL"], cwd=server_dir, check=True)
