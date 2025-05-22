import subprocess
import sys
from pathlib import Path
#------------------------------------
#run as; python batch_plotter.py /path/to/master_dir /path/to/af_plotter.py (name of conda env)afplotter
#I hope conda run works else you can make a shell script, like the following;
#-------------------------------------

##!/bin/bash
#source ~/anaconda3/etc/profile.d/conda.sh  # or your conda init path
#conda activate afplotter
#python batch_plotter.py /path/to/master_dir /path/to/af_plotter.py afplotter
#conda deactivate

def is_valid_target(json_path: Path) -> bool:
    parent_name = json_path.parent.name
    expected_filename = f"{parent_name}_confidences.json"
    return json_path.name == expected_filename

def main(master_dir, plotter_script, conda_env):
    master_path = Path(master_dir)

    json_files = [
        f for f in master_path.rglob("*_confidences.json")
        if is_valid_target(f)
    ]

    if not json_files:
        print("No *_confidences.json files found.")
        return

    for json_file in json_files:
        output_dir = json_file.parent
        print(f"Running plotter for: {json_file}")
        subprocess.run([
            "conda", "run", "-n", conda_env, "python",
            str(plotter_script),
            str(json_file),
            "--output", str(output_dir),
            "--glob", "*_confidences.json"
        ])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python batch_plotter.py /path/to/master_dir /path/to/af_plotter.py conda_env_name")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
