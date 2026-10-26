from pathlib import Path

from Nullomers.NullomerGenerator import classify_nullomers
from Nullomers.NullomerGenerator import pan_nullomer

path_to_nullomers = Path("FakePan-Genome/4_Nullomers")
output_dir = path_to_nullomers / "classification"

distinct_nullomers = pan_nullomer.file_by_file(path_to_nullomers)

classified = classify_nullomers.classify_nullomers(
    path_to_nullomers,
    distinct_nullomers,
    output_dir=output_dir,
)

print("Classification files written to:", output_dir)
print("Core:", len(classified["Core Nullomers"]))
print("Softcore:", len(classified["Softcore Nullomers"]))
print("Shell:", len(classified["Shell Nullomers"]))
print("Cloud:", len(classified["Cloud Nullomers"]))