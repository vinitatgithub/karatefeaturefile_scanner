# python3

# List of not to-be-scanned files
not_to_be_scanned_file_names = ["common.feature", "setup.feature", "common_defs.feature"]

import os
import sys


class ScanFeatureFiles:
    def __init__(self, raise_exception=True):
        self.test_summary = 'Test Summary for '
        self.feature_count = 0
        self.scenario_count = 0
        self.raise_exception = raise_exception

    def extract_features_and_scenarios_from_feature_file(self, file_path):
        with open(file_path, 'r') as in_file:
            lines = in_file.readlines()
            feature_found = False
            for line in lines:
                if 'Feature:' in line:
                    if 'Feature:' == line.strip():
                        if self.raise_exception:
                            raise SystemError(f"Empty feature field found in {file_path}")
                        else:
                            print(f"Empty feature field found in {file_path}")
                    feature_found = True
                    self.feature_count += 1 
                    self.test_summary += f'### {line.strip()}\n'
                    continue
                if 'Scenario:' in line and not feature_found:
                    if self.raise_exception:
                        raise SystemError(f"Scenario found without a valid feature being defined in {file_path}")
                    else:
                        print(f"Scenario found without a valid feature being defined in {file_path}")
                if 'Scenario:' in line and feature_found:
                    self.test_summary += f'* {line.strip()}\n'
                    self.scenario_count += 1

    def walk_dir(self, scanning_directory):
        self.test_summary += f'{scanning_directory}\n\n'
        print(scanning_directory)
        for root, dirs, files in os.walk(scanning_directory):
            path = root.split(os.sep)
            # print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                if ".feature" in file and file not in not_to_be_scanned_file_names:
                    print(len(path) * '---', file)
                    file_path = f"{root}/{file}"
                    print(f"FilePath: {file_path}")
                    self.extract_features_and_scenarios_from_feature_file(file_path)

    def generate_testsuite_md(self):
        with open('testSuite.md', 'w') as out_file:
            out_file.write(self.test_summary)


if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    scanning_directory = sys.argv[1]
    sff = ScanFeatureFiles(raise_exception=False)
    sff.walk_dir(scanning_directory)
    sff.generate_testsuite_md()
    print(sff.test_summary)
    print(f"Feature Count: {sff.feature_count}, Scenario Count: {sff.scenario_count}")
