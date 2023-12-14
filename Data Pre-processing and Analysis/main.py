"""
COMP20008 Elements of Data Processing
2023 Semester 2
Assignment 1

DO NOT CHANGE THIS FILE!
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from enum import Enum
from typing import Optional
from sklearn.model_selection import train_test_split

ERROR_MARK = "❌"
PASS_MARK = "✔️"

# Max values to show in error message
SHOW_LIMIT = 3


class RunMode(Enum):
    # Verify the contents against sample data.
    SAMPLE = 0
    # Run the contents against the full dataset.
    FULL = 1
    # Perform extra actions.
    EXTRA = 2

    def get_mode_string(mode):
        handled_modes = [RunMode.SAMPLE, RunMode.FULL, RunMode.EXTRA]
        match mode:
            case RunMode.SAMPLE:
                return "verifying against sample data"
            case RunMode.FULL:
                return "running against full dataset"
            case RunMode.EXTRA:
                return "running extra functions"
            case other:
                assert other in handled_modes, \
                    "ERROR: Mode was unhandled {}".format(other)

    def get_handled_mode_strings():
        return ["sample", "full", "extra"]

    def get_mode_for_string(string: str):
        assert string in RunMode.get_handled_mode_strings(), \
            "Unhandled mode {}, use one of {}".format(
                string,
                ", ".join(RunMode.get_handled_mode_strings()))
        match string:
            case "sample":
                return RunMode.SAMPLE
            case "full":
                return RunMode.FULL
            case "extra":
                return RunMode.EXTRA


def get_lowercase_keymap(dictionaries, names):
    mapping = {}
    for name in names:
        mapping[name] = {}
    for dictionary, name in zip(dictionaries, names):
        for key in dictionary.keys():
            assert key.lower() not in mapping[name].keys(), \
                "Duplicate keys for lowercased form {}, keys first colliding were {} and {}".format(
                    key.lower(),
                    mapping[name][key.lower()],
                    key.lower()
                )
            mapping[name][key.lower()] = key
    return mapping


def get_lowercase_col_indexmap(lists, names):
    mapping = {}
    for name in names:
        mapping[name] = {}
    for list_i, name in zip(lists, names):
        for col in list_i:
            assert col.lower() not in mapping[name].keys(), \
                "Duplicate columns for lowercased form {}, columns first colliding were {} and {}".format(
                    col.lower(),
                    mapping[name][col.lower()],
                    col
                )
            mapping[name][col.lower()] = col
    return mapping


#def check_task1(textlist_to_check, expected_contents):
    #return check_task_text_list(textlist_to_check, expected_contents)


def check_task2(csv_to_check, expected_csv):
    return check_task_csv(csv_to_check, expected_csv)


#def check_task3(csv_to_check, expected_csv):
    #return check_task_csv(csv_to_check, expected_csv)

def check_task4(csv_to_check, expected_csv):
    return check_task_csv(csv_to_check, expected_csv)

#def check_task6(csv_to_check, expected_csv):
    #return check_task_csv(csv_to_check, expected_csv)


def check_task_json(json_to_check, expected_json, item_name):
    list_of_keys = set([key.lower() for key in json_to_check.keys()])
    list_of_expected_keys = set([key.lower() for key in expected_json.keys()])
    if not list_of_keys == list_of_expected_keys:
        missing_keys = list_of_expected_keys.difference(list_of_keys)
        extra_keys = list_of_keys.difference(list_of_expected_keys)
        if len(missing_keys) > 0:
            print("\t {} Missing keys {}".format(
                ERROR_MARK,
                ", ".join(['"{}"'.format(key) for key in sorted(list(missing_keys))]))
            )
        if len(extra_keys) > 0:
            if len(extra_keys) > SHOW_LIMIT:
                print("\t {} Extra keys   {}".format(
                    ERROR_MARK,
                    ", ".join(['"{}"'.format(key) for key in sorted(list(extra_keys))[:SHOW_LIMIT]]) + ", ...")
                )
            else:
                print("\t {} Extra keys   {}".format(
                    ERROR_MARK,
                    ", ".join(['"{}"'.format(key) for key in sorted(list(extra_keys))]))
                )
        return False

    lowercase_keymap = get_lowercase_keymap(
        [json_to_check, expected_json],
        ["check", "expected"]
    )

    for key in lowercase_keymap["expected"].keys():
        json_to_check_values = set([link.lower() for link in json_to_check[lowercase_keymap["check"][key]]])
        expected_json_values = set([link.lower() for link in expected_json[lowercase_keymap["expected"][key]]])
        if not json_to_check_values == expected_json_values:
            missing_vals = expected_json_values.difference(json_to_check_values)
            extra_vals = json_to_check_values.difference(expected_json_values)
            if len(missing_vals) > 0:
                if len(missing_vals) > SHOW_LIMIT:
                    print("\t {} For seed link {}, missing {} {}".format(
                        ERROR_MARK,
                        key,
                        item_name,
                        ", ".join(['"{}"'.format(key) for key in sorted(list(missing_vals))[:SHOW_LIMIT]]) + ", ..."
                        )
                    )
                else:
                    print("\t {} For seed link {}, missing {} {}".format(
                        ERROR_MARK,
                        key,
                        item_name,
                        ", ".join(['"{}"'.format(key) for key in sorted(list(missing_vals))]))
                    )
            if len(extra_vals) > 0:
                if len(extra_vals) > SHOW_LIMIT:
                    print("\t {} For seed link {}, extra {}   {}".format(
                        ERROR_MARK,
                        key,
                        item_name,
                        ", ".join(['"{}"'.format(key) for key in sorted(list(extra_vals))[:SHOW_LIMIT]]) + ", ..."
                        )
                    )
                else:
                    print("\t {} For seed link {}, extra {}   {}".format(
                        ERROR_MARK,
                        key,
                        item_name,
                        ", ".join(['"{}"'.format(key) for key in sorted(list(extra_vals))])
                        )
                    )
            return False
    return True


def verify_task1(mode: RunMode):
    try:
        from task1 import task1
    except ImportError:
        print("Task 1's function not successfully imported.")
        return

    print("=" * 80)
    print(f"Executing Task 1 for {RunMode.get_mode_string(mode)}...\n")
    handled_modes = [RunMode.SAMPLE, RunMode.FULL, RunMode.EXTRA]
    dataset_filename = []
    json_filename = ""
    match mode:
        case RunMode.SAMPLE:
            dataset_filename = "datafile_sample.csv"
        case RunMode.FULL:
            dataset_filename = "datafile.csv"
        case RunMode.EXTRA:
            assert mode in handled_modes, "No extra behaviour for Task 1"
        case other:
            assert other in handled_modes, \
                "ERROR: Mode was unhandled {}".format(other)
    output_data = task1(dataset_filename)

    print("Checking Task 1's output...\n")
    if not type(output_data) == list:
        print(f"\t {ERROR_MARK} Task 1 is expected to return a list of the " +
              "strings which were printed out. Type was: ", type(output_data))
        print("\t Returned output (as its Python data representation) was:")
        print(output_data)
    elif not len(output_data) == 2:
        print(f"\t {ERROR_MARK} Task 1 is expected to return a list of " +
              "two strings.")
        print("\t These are meant to be of the form:")
        print("\t\t (item 0) Number of rows: X")
        print("\t\t (item 1) Number of columns: Y\n")
        print("\t but were:")
        for idx, item in enumerate(output_data):
            print("\t\t (item {}) {}".format(idx, item))
    elif not all([type(item) == str for item in output_data]):
        print(f"\t {ERROR_MARK} Task 1 is expected to return a list of " +
              "strings.")
        print("\t These are meant to be of the form:")
        print("\t\t (item 0, str) Number of rows: X")
        print("\t\t (item 1, str) Number of columns: Y\n")
        print("\t but were:")
        for idx, item in enumerate(output_data):
            print("\t\t (item {}, {}) {}".format(idx, type(item).__name__, item))
    else:
        sample_solution = [
            "Number of rows: 20",
            "Number of columns: 3"
        ]
        if mode == RunMode.SAMPLE:
            matches = True
            for lidx, line in enumerate(sample_solution):
                if sample_solution[lidx] == output_data[lidx]:
                    print(f"\t {PASS_MARK} Your output matches the sample for"
                          + f" line #{lidx} of Task 1.")
                else:
                    print(f"\t {ERROR_MARK} Your output does not match the "
                          + f"sample for line # {lidx} of Task 1.")
                    print("\t\t sample: \"{}\"".format(sample_solution[lidx]))
                    print("\t\t return: \"{}\"".format(output_data[lidx]))


    print("Finished Task 1.")
    print("=" * 80)


def verify_task2(mode: RunMode, extra_mode_url: Optional[str] = None):

    try:
        from task2 import task2
    except ImportError:
        print("Task 2's function not successfully imported.")
        return

    print("=" * 80)
    print(f"Executing Task 2 for {RunMode.get_mode_string(mode)}...\n")

    handled_modes = [RunMode.SAMPLE, RunMode.FULL]
    dataset_filename = ""
    output_filename = ""

    match mode:
        case RunMode.SAMPLE:
            dataset_filename = "datafile_sample.csv"
            output_filename = "task2_my_sample.csv"
        case RunMode.FULL:
            dataset_filename = "datafile.csv"
            output_filename = "task2_my_full.csv"
        case RunMode.EXTRA:
            assert mode in handled_modes, "No extra behaviour for Task 2"
        case other:
            assert other in handled_modes, \
                "ERROR: Mode was unhandled {}".format(other)

    task2(dataset_filename, output_filename)

    print("Checking Task 2's output...\n")
    if os.path.isfile(output_filename):
        print("\tTask 2's CSV output found.\n")
    else:
        print(f"\t {ERROR_MARK} Task 2's CSV output NOT found. "
              "Please check your code.\n")

    sample_filename = "task2_sample.csv"
    if mode == RunMode.SAMPLE:
        if os.path.isfile(output_filename):
            if os.path.isfile(sample_filename):
                my_csv = pd.read_csv(output_filename)
                sample_csv = pd.read_csv(sample_filename)
                if check_task2(my_csv, sample_csv):
                    print(f"\t {PASS_MARK} Your output matches the sample for "
                          "Task 2.")
                else:
                    print(f"\t {ERROR_MARK} Your output does not match the "
                          "sample for Task 2.")
            else:
                print(f"\t {ERROR_MARK} The sample output file is missing, "
                      "download and replace it from the Sample data slide.")

    print("Finished Task 2.")
    print("=" * 80)


def check_task_csv(csv_to_check, expected_csv):
    # Check columns match.
    check_cols = csv_to_check.columns
    expected_cols = expected_csv.columns

    lowercase_keymap = get_lowercase_col_indexmap(
        [check_cols, expected_cols],
        ["check", "expected"]
    )

    check_cols_lower = set([c.lower() for c in check_cols])
    expected_cols_lower = set([c.lower() for c in expected_cols])

    if not check_cols_lower == expected_cols_lower:
        missing_vals = expected_cols_lower.difference(check_cols_lower)
        extra_vals = check_cols_lower.difference(expected_cols_lower)
        if len(missing_vals) > 0:
            if len(missing_vals) > SHOW_LIMIT:
                print("\t {} CSV is missing columns {}".format(
                    ERROR_MARK,
                    ", ".join(['"{}"'.format(key) for key in sorted(list(missing_vals))[:SHOW_LIMIT]]) + ", ..."
                    )
                )
            else:
                print("\t {} CSV is missing columns {}".format(
                    ERROR_MARK,
                    ", ".join(['"{}"'.format(key) for key in sorted(list(missing_vals))]))
                )
            if len(extra_vals) > 0:
                if len(extra_vals) > SHOW_LIMIT:
                    print("\t {} CSV has extra columns  {}".format(
                        ERROR_MARK,
                        ", ".join(['"{}"'.format(key) for key in sorted(list(extra_vals))[:SHOW_LIMIT]]) + ", ..."
                        )
                    )
                else:
                    print("\t {} CSV has extra columns  {}".format(
                        ERROR_MARK,
                        ", ".join(['"{}"'.format(key) for key in sorted(list(extra_vals))])
                        )
                    )
            return False

    for column in lowercase_keymap["expected"].keys():
        # Check counts
        check_values = set(csv_to_check[lowercase_keymap["check"][column]].values)
        expected_values = set(expected_csv[lowercase_keymap["expected"][column]].values)
        if not check_values == expected_values:
            missing_vals = expected_values.difference(check_values)
            extra_vals = check_values.difference(expected_values)
            # Check values match
            if len(missing_vals) > 0:
                if len(missing_vals) > SHOW_LIMIT:
                    print("\t {} For column {}, missing {} {}".format(
                        ERROR_MARK,
                        column,
                        "value",
                        ", ".join(['"{}"'.format(key) for key in sorted(list(missing_vals))[:SHOW_LIMIT]]) + ", ..."
                        )
                    )
                else:
                    print("\t {} For column {}, missing {} {}".format(
                        ERROR_MARK,
                        column,
                        "value",
                        ", ".join(['"{}"'.format(key) for key in sorted(list(missing_vals))]))
                    )
            if len(extra_vals) > 0:
                if len(extra_vals) > SHOW_LIMIT:
                    print("\t {} For column {}, extra {}   {}".format(
                        ERROR_MARK,
                        column,
                        "value",
                        ", ".join(['"{}"'.format(key) for key in sorted(list(extra_vals))[:SHOW_LIMIT]]) + ", ..."
                        )
                    )
                else:
                    print("\t {} For column {}, extra {}   {}".format(
                        ERROR_MARK,
                        column,
                        "value",
                        ", ".join(['"{}"'.format(key) for key in sorted(list(extra_vals))])
                        )
                    )
            return False
        # Check counts of each value match
        counts_check = csv_to_check[lowercase_keymap["check"][column]].value_counts()
        counts_expected = expected_csv[lowercase_keymap["expected"][column]].value_counts()

        difference = counts_expected - counts_check

        difference = difference[abs(difference) > 0]

        if difference.size > 0:
            print("\t {} For column {}, difference in counts for each value".format(
                ERROR_MARK,
                column
                )
            )
            print(difference.head(SHOW_LIMIT))
            if difference.size > SHOW_LIMIT:
                print("\t ...")
            return False

        # Check order matches.
        if not all(csv_to_check[lowercase_keymap["check"][column]] == expected_csv[lowercase_keymap["expected"][column]]):
            print("\t {} For column {}, there was an error in the ordering of the data.".format(
                ERROR_MARK,
                column
                )
            )

            print("\t Items should be ordered:")
            print(expected_csv[lowercase_keymap["expected"][column]][~(csv_to_check[lowercase_keymap["check"][column]] == expected_csv[lowercase_keymap["expected"][column]])].head(SHOW_LIMIT))
            print("\n\t But were ordered:")
            print(csv_to_check[lowercase_keymap["expected"][column]][~(csv_to_check[lowercase_keymap["check"][column]] == expected_csv[lowercase_keymap["expected"][column]])].head(SHOW_LIMIT))

            return False
    return True


def verify_task3(mode):

    try:
        from task3 import task3
    except ImportError:
        print("Task 3's function not successfully imported.")
        return

    print("=" * 80)
    print(f"Executing Task 3 for {RunMode.get_mode_string(mode)}...\n")

    handled_modes = [RunMode.SAMPLE, RunMode.FULL, RunMode.EXTRA]
    csv_filename = ""
    output_filename = ""
    match mode:
        case RunMode.SAMPLE:
            csv_filename = "task2_sample.csv"
            output_filename = "task3_my_sample.png"
            if not os.path.isfile(csv_filename):
                print(
                    f"\t {ERROR_MARK} The sample output file for Task 2 is "
                    "required for Task 3 but was missing, download and "
                    "replace it from the Sample data slide."
                )
        case RunMode.FULL:
            csv_filename = "task2_my_full.csv"
            output_filename = "task3_my_full.png"
            if not os.path.isfile(csv_filename):
                print(
                    f"\t {ERROR_MARK} The full running mode for Task 3 "
                    "requires the output for Task 2 to be present, "
                    "ensure it was correctly created."
                )
        case RunMode.EXTRA:
            assert mode in handled_modes, "No extra behaviour for Task 3"
        case other:
            assert other in handled_modes, \
                "ERROR: Mode was unhandled {}".format(other)

    task3(csv_filename, output_filename)

    print("Checking Task 3's output...\n")
    if os.path.isfile(output_filename):
        print("\tTask 3's plot output found.\n")
        # Check size is sensible.
        if os.path.getsize(output_filename) <= 0:
            print(f"\t {ERROR_MARK} Task 3's plot appears to have "
                  "been created, but the file is empty. Check it has "
                  "output as expected.")
    else:
        print(f"\t {ERROR_MARK} Task 3's plot output NOT found. "
              "Please check your code.\n")

    print("Finished executing Task 3.")
    print("=" * 80)


def verify_task4(mode):

    try:
        from task4 import task4
    except ImportError:
        print("Task 4's function not successfully imported.")
        return

    print("=" * 80)
    print(f"Executing Task 4 for {RunMode.get_mode_string(mode)}...\n")

    handled_modes = [RunMode.SAMPLE, RunMode.FULL]
    dataset_filename = ""
    output_filename = ""
    match mode:
        case RunMode.SAMPLE:
            dataset_filename = "task2_sample.csv"
            output_filename = "task4_my_sample.csv"
            if not os.path.isfile(dataset_filename):
                print(
                    f"\t {ERROR_MARK} The sample output file for Task 2 is "
                    "required for Task 4 but was missing, download and "
                    "replace it from the Sample data slide."
                )
        case RunMode.FULL:
            dataset_filename = "task2_my_full.csv"
            output_filename = "task4_my_full.csv"
            if not os.path.isfile(dataset_filename):
                print(
                    f"\t {ERROR_MARK} The full running mode for Task 4 "
                    "requires the output for Task 2 to be present, "
                    "ensure it was correctly created."
                )
        case RunMode.EXTRA:
            assert mode in handled_modes, "No extra behaviour for Task 4"
        case other:
            assert other in handled_modes, \
                "ERROR: Mode was unhandled {}".format(other)

    task4(dataset_filename, output_filename)

    print("Checking Task 4's output...\n")
    if os.path.isfile(output_filename):
        print("\tTask 4's CSV output found.\n")
    else:
        print(f"\t {ERROR_MARK} Task 4's CSV output NOT found. "
              "Please check your code.\n")

    sample_filename = "task4_sample.csv"
    if mode == RunMode.SAMPLE:
        if os.path.isfile(output_filename):
            if os.path.isfile(sample_filename):
                my_csv = pd.read_csv(output_filename)
                sample_csv = pd.read_csv(sample_filename)
                if check_task4(my_csv, sample_csv):
                    print(f"\t {PASS_MARK} Your output matches the sample for "
                          "Task 4.")
                else:
                    print(f"\t {ERROR_MARK} Your output does not match the "
                          "sample for Task 4.")
            else:
                print(f"\t {ERROR_MARK} The sample output file is missing, "
                      "download and replace it from the Sample data slide.")

    print("Finished executing Task 4.")
    print("=" * 80)


def verify_task5(mode):
    try:
        from task5 import task5
    except ImportError:
        print("Task 5's function not successfully imported.")
        return

    print("=" * 80)
    print(f"Executing Task 5 for {RunMode.get_mode_string(mode)}...\n")

    handled_modes = [RunMode.SAMPLE, RunMode.FULL]

    dataset_filename = ""
    json_output_filename = ""
    plot_output_filename = ""

    match mode:
        case RunMode.SAMPLE:
            dataset_filename = "task4_sample.csv"
            json_output_filename = "task5_my_sample.json"
            plot_output_filename = "task5_my_sample.png"
            if not os.path.isfile(dataset_filename):
                print(
                    f"\t {ERROR_MARK} The sample output file for Task 4 is "
                    "required for Task 5 but was missing, download and "
                    "replace it from the Sample data slide."
                )
        case RunMode.FULL:
            dataset_filename = "task4_my_full.csv"
            json_output_filename = "task5_my_full.json"
            plot_output_filename = "task5_my_full.png"
            if not os.path.isfile(dataset_filename):
                print(
                    f"\t {ERROR_MARK} The full running mode for Task 5 "
                    "requires the output for Task 4 to be present, "
                    "ensure it was correctly created."
                )
        case RunMode.EXTRA:
            assert mode in handled_modes, "No extra behaviour for Task 5"
        case other:
            assert other in handled_modes, \
                "ERROR: Mode was unhandled {}".format(other)

    task5(dataset_filename, json_output_filename, plot_output_filename)

    print("Checking Task 5's output...\n")
    json_check = True
    if os.path.isfile(json_output_filename):
        print("\tTask 5's JSON output found.\n")
        # Check size is sensible.
        if os.path.getsize(json_output_filename) <= 0:
            print(f"\t {ERROR_MARK} Task 5's JSON output appears to have "
                  "been created, but the file is empty. Check it has "
                  "output as expected.")
    else:
        print(f"\t {ERROR_MARK} Task 5's JSON output NOT found. "
              "Please check your code.\n")
        json_check = False

    if os.path.isfile(plot_output_filename):
        print("\tTask 5's plot output found.\n")
        # Check size is sensible.
        if os.path.getsize(plot_output_filename) <= 0:
            print(f"\t {ERROR_MARK} Task 5's plot appears to have "
                  "been created, but the file is empty. Check it has "
                  "output as expected.")
    else:
        print(f"\t {ERROR_MARK} Task 5's plot output NOT found. "
              "Please check your code.\n")

    sample_filename = "task5_sample.json"
    if mode == RunMode.SAMPLE:
        if json_check:
            # Load in JSON output for testing.
            with open(json_output_filename) as f:
                my_json_output = json.load(f)

            if os.path.isfile(sample_filename):
                with open(sample_filename) as f:
                    sample_word_averages = json.load(f)
                if set(sample_word_averages.keys()) == set(my_json_output.keys()):
                            print(f"\t {PASS_MARK} Your Task 5 JSON output contains the right words.")
                else:
                    print(f"\t {ERROR_MARK} Your Task 5 JSON output was:")
                    print("[{}{}]".format(
                        ", ".join(sorted(list(my_json_output.keys()))[:11]),
                        ", ..." if len(my_json_output.keys()) > 10 else "")
                    )
                    print("\t but should have been:")
                    print("[{}]".format(", ".join(
                        sorted(list(sample_word_averages.keys()))[:11]))
                    )
                for word in sample_word_averages.keys():
                    if word not in my_json_output.keys():
                        print(f"\t {ERROR_MARK} Your Task 5 JSON output was missing the word \"{word}\"")
                    elif abs(my_json_output[word] - sample_word_averages[word]) > 0.0001:
                        print(f"\t {ERROR_MARK} Your average views for the word \"{word}\" was {my_json_output[word]} but should have been {sample_word_averages[word]}")
                    else:
                        print(f"\t {PASS_MARK} Your output matches the sample for "
                            f"Task 5 for word \"{word}\".")

            else:
                print(f"\t {ERROR_MARK} The sample words file is missing, "
                        "download and replace it from the Sample data slide.")


    print("Finished executing Task 5.")
    print("=" * 80)


def verify_task6():

    print("Checking if task6.pdf exists...\n")
    if os.path.isfile("task6.pdf"):
        print(f"\t {PASS_MARK} Report task6.pdf found.\n")
        if os.path.getsize("task6.pdf") <= 0:
            print(f"\t {ERROR_MARK} Report task6.pdf was empty! Please check it uploaded correctly.\n")
    else:
        print(f"\t {ERROR_MARK} Report task6.pdf NOT found. Please check the file name or upload the file.\n")

    print("Finished Task 6.")
    print("=" * 80)


def main():
    args = sys.argv
    assert len(args) >= 2, "Please provide a task."
    task = args[1]
    assert task in ["all"] + ["task" + str(i) for i in range(1, 8)], \
        "Invalid task."
    if len(args) > 2:
        assert args[2].lower() in RunMode.get_handled_mode_strings(), \
            "Run mode was invalid, should be one of [{}]".format(
            ", ".join(RunMode.get_handled_mode_strings()))
        mode = RunMode.get_mode_for_string(args[2])
    else:
        mode = None
    if task == "task1":
        assert mode is not None, "Please ensure you have also provided a mode."
        verify_task1(mode)
    elif task == "task2":
        assert mode is not None, "Please ensure you have also provided a mode."
        verify_task2(mode)
    elif task == "task3":
        assert mode is not None, "Please ensure you have also provided a mode."
        verify_task3(mode)
    elif task == "task4":
        assert mode is not None, "Please ensure you have also provided a mode."
        verify_task4(mode)
    elif task == "task5":
        assert mode is not None, "Please ensure you have also provided a mode."
        verify_task5(mode)
    elif task == "task6":
        verify_task6()
    elif task == "all":
        assert mode is not None, "Please ensure you have also provided a mode."
        verify_task1(mode)
        verify_task2(mode)
        verify_task3(mode)
        verify_task4(mode)
        verify_task5(mode)
        verify_task6()

if __name__ == "__main__":
    main()


