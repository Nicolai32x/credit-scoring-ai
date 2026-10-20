"""Check source identity and holdout isolation without fitting any model."""

from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from preprocessing import (  # noqa: E402
    DATA_PATH, FEATURE_COLUMNS, SPLIT_PATH, TARGET,
    load_dataset, load_partition, reserve_split, validate_split,
)


class DataSplitTests(unittest.TestCase):
    def test_label_mapping_and_feature_positions(self):
        frame = load_dataset()
        source_first = DATA_PATH.read_text().splitlines()[0].split()
        self.assertEqual(frame.loc[0, TARGET], int(source_first[20]) - 1)
        self.assertEqual(frame.loc[0, "credit_amount"], int(source_first[4]))
        self.assertEqual(frame.loc[0, "duration_months"], int(source_first[1]))
        self.assertEqual(frame.loc[0, "purpose"], source_first[3])
        for name, column in [("checking_status", 0), ("credit_history", 2),
                             ("savings_status", 5), ("employment_duration", 6)]:
            self.assertEqual(frame.loc[0, name], source_first[column])
        self.assertEqual(frame[TARGET].value_counts().to_dict(), {0: 700, 1: 300})

    def test_partitions_are_disjoint_complete_and_stratified(self):
        development, dev_target = load_partition()
        test, test_target = load_partition("test")
        self.assertEqual(development.shape, (800, 7))
        self.assertEqual(test.shape, (200, 7))
        self.assertTrue(set(development.index).isdisjoint(test.index))
        self.assertEqual(set(development.index) | set(test.index), set(range(1000)))
        self.assertEqual(dev_target.value_counts().to_dict(), {0: 560, 1: 240})
        self.assertEqual(test_target.value_counts().to_dict(), {0: 140, 1: 60})
        self.assertEqual(list(development.columns), FEATURE_COLUMNS)
        self.assertNotIn(TARGET, development.columns)
        self.assertNotIn("row_id", development.columns)
        self.assertTrue(development.index.equals(dev_target.index))

    def test_manifest_reproduction_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "split.json"
            created = reserve_split(path)
            self.assertEqual(created["row_ids"], json.loads(SPLIT_PATH.read_text())["row_ids"])
            before = path.read_bytes()
            reserve_split(path)
            self.assertEqual(path.read_bytes(), before)
            default_x, default_y = load_partition()
            reproduced_x, reproduced_y = load_partition(manifest_path=path)
            pd.testing.assert_frame_equal(default_x, reproduced_x)
            pd.testing.assert_series_equal(default_y, reproduced_y)

    def test_overlapping_manifest_is_rejected(self):
        frame = load_dataset()
        manifest = json.loads(SPLIT_PATH.read_text())
        manifest["row_ids"]["test"][0] = manifest["row_ids"]["development"][0]
        with self.assertRaises(ValueError):
            validate_split(manifest, frame)

    def test_changed_setup_is_rejected_without_overwriting_file(self):
        manifest = json.loads(SPLIT_PATH.read_text())
        for key, value in [("source_sha256", "changed"), ("random_seed", 99),
                           ("feature_columns", FEATURE_COLUMNS + [TARGET]),
                           ("target_mapping", {"1": 1, "2": 0})]:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as directory:
                changed = deepcopy(manifest)
                changed[key] = value
                path = Path(directory) / "split.json"
                path.write_text(json.dumps(changed), encoding="utf-8")
                before = path.read_bytes()
                with self.assertRaises(ValueError):
                    reserve_split(path)
                self.assertEqual(path.read_bytes(), before)

    def test_modified_original_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "german.data"
            path.write_bytes(DATA_PATH.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "checksum"):
                load_dataset(path)

    def test_invalid_partition_is_rejected(self):
        with self.assertRaises(ValueError):
            load_partition("all")

    def test_malformed_manifest_is_rejected(self):
        frame = load_dataset()
        for manifest in [[], {"row_ids": []}]:
            with self.subTest(manifest=manifest), self.assertRaises(ValueError):
                validate_split(manifest, frame)


if __name__ == "__main__":
    unittest.main()
