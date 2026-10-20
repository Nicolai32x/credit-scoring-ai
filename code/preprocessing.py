"""Load the fixed data partitions and build unfitted preprocessing pipelines.

Encoding categories and scaling numeric inputs must be learned inside each
training fold. The factories below do not fit anything or load test data.
"""

from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path

import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, clone
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "german.data"
SPLIT_PATH = PROJECT_ROOT / "data" / "split.json"
SOURCE_SHA256 = "b21f3d81db8071257d5ff1deaeba1fd4303b62712e6fcc9715c7a86202cb5871"
RANDOM_SEED = 42
TARGET = "bad_risk"

# Names follow the original file order, not the order of the future form.
SOURCE_COLUMNS = [
    "checking_status", "duration_months", "credit_history", "purpose",
    "credit_amount", "savings_status", "employment_duration",
    "installment_rate", "personal_status_sex", "other_debtors",
    "residence_duration", "property", "age", "other_installment_plans",
    "housing", "existing_credits", "job", "dependants", "telephone",
    "foreign_worker", TARGET,
]
FEATURE_COLUMNS = [
    "credit_amount", "duration_months", "purpose", "checking_status",
    "savings_status", "employment_duration", "credit_history",
]
NUMERIC_FEATURES = ["credit_amount", "duration_months"]
CATEGORICAL_FEATURES = [
    "purpose", "checking_status", "savings_status",
    "employment_duration", "credit_history",
]


def load_dataset(source_path: Path = DATA_PATH) -> pd.DataFrame:
    """Name all source columns and map good/bad labels to 0/1.

    row_id is the zero-based original file position, not a customer ID or a
    model input. Exploratory notebooks should use load_partition() instead.
    """
    payload = Path(source_path).read_bytes()
    if sha256(payload).hexdigest() != SOURCE_SHA256:
        raise ValueError("Source checksum differs from the reviewed UCI original.")
    frame = pd.read_csv(BytesIO(payload), sep=r"\s+", header=None)
    if frame.shape != (1000, 21) or frame.isna().any().any():
        raise ValueError("Expected 1,000 complete source rows with 21 fields.")
    frame.columns = SOURCE_COLUMNS
    if set(frame[TARGET].unique()) != {1, 2}:
        raise ValueError("Expected original credit-risk labels 1 and 2.")
    frame[TARGET] = frame[TARGET].map({1: 0, 2: 1}).astype("int64")
    frame.index.name = "row_id"
    return frame


def validate_split(manifest: dict, frame: pd.DataFrame) -> None:
    """Reject a changed source, input schema, or overlapping/incomplete split."""
    if not isinstance(manifest, dict):
        raise ValueError("Split manifest must be a JSON object.")
    if (
        manifest.get("source_sha256") != SOURCE_SHA256
        or manifest.get("feature_columns") != FEATURE_COLUMNS
        or manifest.get("target") != TARGET
        or manifest.get("target_mapping") != {"1": 0, "2": 1}
        or manifest.get("random_seed") != RANDOM_SEED
        or manifest.get("test_size") != 0.2
    ):
        raise ValueError("Split metadata does not match the agreed source and setup.")
    ids = manifest.get("row_ids", {})
    if not isinstance(ids, dict):
        raise ValueError("Split row_ids must contain the two partition lists.")
    development = ids.get("development", [])
    test = ids.get("test", [])
    if (
        not isinstance(development, list) or not isinstance(test, list)
        or not all(type(value) is int for value in development + test)
        or len(development) != 800 or len(test) != 200
        or len(set(development)) != 800 or len(set(test)) != 200
        or set(development) & set(test)
        or set(development) | set(test) != set(frame.index)
    ):
        raise ValueError("Split must contain 800 and 200 unique, disjoint source rows.")
    for partition, expected in [(development, {0: 560, 1: 240}), (test, {0: 140, 1: 60})]:
        if frame.loc[partition, TARGET].value_counts().to_dict() != expected:
            raise ValueError("Split does not preserve the documented class balance.")


def reserve_split(manifest_path: Path = SPLIT_PATH) -> dict:
    """Create the manifest once, or validate and reuse it without reshuffling."""
    frame = load_dataset()
    manifest_path = Path(manifest_path)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_split(manifest, frame)
        return manifest

    development, test = train_test_split(
        frame.index.to_numpy(), test_size=0.2,
        random_state=RANDOM_SEED, stratify=frame[TARGET],
    )
    manifest = {
        "source_file": "german.data",
        "source_sha256": SOURCE_SHA256,
        "row_id_definition": "Zero-based original file row, not a customer identifier",
        "feature_columns": FEATURE_COLUMNS,
        "target": TARGET,
        "target_mapping": {"1": 0, "2": 1},
        "random_seed": RANDOM_SEED,
        "test_size": 0.2,
        "created_with_scikit_learn": sklearn.__version__,
        "row_ids": {
            "development": sorted(int(value) for value in development),
            "test": sorted(int(value) for value in test),
        },
    }
    validate_split(manifest, frame)
    # Exclusive creation prevents accidental replacement of an existing split.
    with manifest_path.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(manifest, indent=2) + "\n")
    return manifest


def load_partition(
    partition: str = "development", manifest_path: Path = SPLIT_PATH,
) -> tuple[pd.DataFrame, pd.Series]:
    """Return only the requested partition as seven inputs and a separate target.

    The default is development. Use 'test' only for final evaluation after
    freezing the modeling decisions; this is a workflow convention, not a lock.
    """
    if partition not in {"development", "test"}:
        raise ValueError("Partition must be 'development' or 'test'.")
    frame = load_dataset()
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    validate_split(manifest, frame)
    selected = frame.loc[manifest["row_ids"][partition]]
    return selected[FEATURE_COLUMNS].copy(), selected[TARGET].copy()


def build_preprocessor(*, scale_numeric: bool = True) -> ColumnTransformer:
    """Return a fresh, unfitted transformation of the seven named inputs.

    Scale numbers for logistic regression; use scale_numeric=False for a
    tree model. Categories are learned from the fit data only. A category
    unseen during fitting produces zeros in that feature's one-hot block.
    Combined source categories such as A65 are kept as categories.
    """
    numeric = StandardScaler() if scale_numeric else "passthrough"
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric, NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(
                handle_unknown="ignore", sparse_output=False,
            ), CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def build_model_pipeline(
    model: BaseEstimator, *, scale_numeric: bool = True,
) -> Pipeline:
    """Keep preprocessing and an unfitted model together for cross-validation.

    Pass raw seven-column DataFrames to this pipeline. Do not transform the
    complete development set before cross-validation. Cloning the supplied
    estimator prevents reuse of previously fitted model state.
    """
    return Pipeline([
        ("preprocessing", build_preprocessor(scale_numeric=scale_numeric)),
        ("model", clone(model)),
    ])


if __name__ == "__main__":
    reserve_split()
    print("Source verified; fixed split reserved: 800 development / 200 test rows.")
    print("Target: bad_risk (0 = good risk; 1 = bad risk).")
    print("No feature transformations or model evaluation performed.")
