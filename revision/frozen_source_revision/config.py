"""Strict, schema-free relation-prediction configuration.

This is the exact configuration used for the multi-seed strict study
(CoDEx-S, CoDEx-M, FB15k-237; seeds 13/42/2025). The dataset and the
ablation configuration are selected per run through environment variables
(KGC_DATASET, KGC_EXPERIMENT_ID, KGC_SEED); see IMPLEMENTATION_NOTES.md.
"""
import os
import torch

SEED = int(os.environ.get("KGC_SEED", "42"))
DETERMINISTIC = os.environ.get("KGC_DETERMINISTIC", "1") == "1"
DATASET_NAME = os.environ.get("KGC_DATASET", "CoDEx-S")  # overridden per run: CoDEx-S | CoDEx-M | FB15k-237
DATA_ROOT = os.environ.get("KGC_DATA_ROOT", os.path.join(os.path.dirname(__file__), "data"))
OUTPUT_ROOT = os.environ.get("KGC_OUTPUT_ROOT", os.path.join(os.path.dirname(__file__), "outputs"))
EXPERIMENT_ID = os.environ.get("KGC_EXPERIMENT_ID", "B2").strip().upper()
ALLOW_OUTPUT_REUSE = os.environ.get("KGC_ALLOW_OUTPUT_REUSE", "0") == "1"

EXPERIMENT_NAMES = {
    "B0": "endpoint_only",
    "B1": "fixed_role_aware_context",
    "B2": "adaptive_role_aware_context",
    "H_ONLY": "adaptive_head_context_only",
    "T_ONLY": "adaptive_tail_context_only",
}
if EXPERIMENT_ID not in EXPERIMENT_NAMES:
    raise ValueError(f"Unsupported KGC_EXPERIMENT_ID={EXPERIMENT_ID!r}; choose one of {sorted(EXPERIMENT_NAMES)}")

EXPERIMENT_OUTPUT_DIR = os.path.join(
    OUTPUT_ROOT, DATASET_NAME, "strict_final", EXPERIMENT_ID, f"seed_{SEED}"
)
DATASETS = [{
    "name": DATASET_NAME,
    "TRAIN_FILE_PATH": os.path.join(DATA_ROOT, DATASET_NAME, "train.txt"),
    "VALID_FILE_PATH": os.path.join(DATA_ROOT, DATASET_NAME, "valid.txt"),
    "TEST_FILE_PATH": os.path.join(DATA_ROOT, DATASET_NAME, "test.txt"),
    "MODEL_SAVE_PATH": EXPERIMENT_OUTPUT_DIR,
    "ENTITY_TYPE_FILE": None,
    "ENTITY_LABEL_FILE": None,
    "RELATION_LABEL_FILE": None,
}]

if torch.cuda.is_available():
    NUM_GPUS = torch.cuda.device_count()
    DEVICE = torch.device("cuda")
else:
    NUM_GPUS = 0
    DEVICE = torch.device("cpu")
MASTER_PORT = os.environ.get("MASTER_PORT", "29500")
DDP_BACKEND = "nccl"

MODEL_NAME = os.environ.get("KGC_MODEL_NAME", "distilbert-base-uncased")
MAX_LENGTH = 128
BATCH_SIZE = 64
PER_GPU_BATCH_SIZE = max(1, BATCH_SIZE // max(NUM_GPUS, 1))
LEARNING_RATE = 5e-5
NUM_EPOCHS = 20
GRADIENT_ACCUMULATION_STEPS = 2
EARLY_STOPPING_PATIENCE = 3
EARLY_STOPPING_MIN_DELTA = 0.0
SAVE_EVERY_EPOCH = False
CHECKPOINT_METRIC = "mrr"
CHECKPOINT_MRR_WEIGHT = 0.7
CHECKPOINT_MACRO_F1_WEIGHT = 0.3

NUM_WORKERS = int(os.environ.get("KGC_NUM_WORKERS", "0"))
PREFETCH_FACTOR = int(os.environ.get("KGC_PREFETCH_FACTOR", "2"))
PIN_MEMORY = True
PRETOKENIZE = False
DYNAMIC_PADDING = True

SPECIAL_TOKENS = [
    "[HEAD]", "[TAIL]", "[HEAD_TYPE]", "[TAIL_TYPE]", "[HEAD_SCHEMA]", "[TAIL_SCHEMA]",
    "[HEAD_CTX]", "[TAIL_CTX]", "[PAIR_CTX]", "[H_IN]", "[H_OUT]", "[T_IN]", "[T_OUT]",
    "[PATH]", "[TYPE]", "[SCHEMA]", "[2HOP]",
]
NORMALIZE_ENTITY_TEXT = True
NORMALIZE_RELATION_TEXT = True
USE_LABEL_MAPS = True

CONTEXT_MODE = "adaptive"
MAX_DEGREE = 30
MIN_CONTEXT = 5
BASE_CONTEXT = 15
MAX_CONTEXT = 30
MAX_HEAD_CONTEXT_TOKENS = 40
MAX_TAIL_CONTEXT_TOKENS = 40
MAX_PAIR_CONTEXT_TOKENS = 24
MAX_PATH_CONTEXT_TOKENS = 20
W_DEGREE = float(os.environ.get("KGC_W_DEGREE", "1.0"))
W_REL_RARITY = float(os.environ.get("KGC_W_REL_RARITY", "0.35"))
W_REDUNDANCY = float(os.environ.get("KGC_W_REDUNDANCY", "0.15"))
GROUP_CONTEXT_BY_RELATION = True
MAX_NEIGHBORS_PER_RELATION = 3

USE_SECOND_HOP_CONTEXT = False
SECOND_HOP_BUDGET = 5
USE_PAIR_CONTEXT = False
MAX_COMMON_NEIGHBORS = 5
MAX_PAIR_MOTIFS = 5
INCLUDE_OTHER_PAIR_RELATIONS = False
USE_PATH_CONTEXT = False
PATH_CONTEXT_MODE = "motif"
MAX_PATHS = 3

USE_ENTITY_TYPES = False
DEFAULT_ENTITY_TYPE = "UNK"
USE_TYPE_RELATION_MASK = False
APPLY_TYPE_MASK_DURING_TRAINING = False
USE_SCHEMA_TOKENS = os.environ.get("KGC_USE_SCHEMA_TOKENS", "0") == "1"
USE_SCHEMA_PRIOR = os.environ.get("KGC_USE_SCHEMA_PRIOR", "0") == "1"
SCHEMA_MODE = "relation_signature"
SCHEMA_TOP_RELATIONS = 3
SCHEMA_PRIOR_WEIGHT = 0.10
SCHEMA_PRIOR_SMOOTHING = 1.0

LOSS_TYPE = "ce"
REWEIGHT_START_EPOCH = 3
LABEL_SMOOTHING = 0.0
FOCAL_GAMMA = 2.0
CLASS_WEIGHT_SMOOTHING = 1.2
TRAIN_SAMPLER = "random"
RELATION_SAMPLER_POWER = 0.5

FILTERED_RELATION_EVAL = True
RARE_RELATION_THRESHOLD = 10
MEDIUM_RELATION_THRESHOLD = 100

EXPERIMENT_MATRIX = {
    "B0": {
        "description": "Endpoints only; no endpoint context, pair evidence, paths, second hop, or schema.",
        "CONTEXT_MODE": "adaptive",
        "MAX_HEAD_CONTEXT_TOKENS": 0,
        "MAX_TAIL_CONTEXT_TOKENS": 0,
    },
    "B1": {
        "description": "Fixed role-aware one-hop context at both endpoints.",
        "CONTEXT_MODE": "fixed",
        "MIN_CONTEXT": 15,
        "BASE_CONTEXT": 15,
        "MAX_CONTEXT": 15,
        "MAX_HEAD_CONTEXT_TOKENS": 40,
        "MAX_TAIL_CONTEXT_TOKENS": 40,
    },
    "B2": {
        "description": "Adaptive role-aware one-hop context at both endpoints.",
        "CONTEXT_MODE": "adaptive",
        "MAX_HEAD_CONTEXT_TOKENS": 40,
        "MAX_TAIL_CONTEXT_TOKENS": 40,
    },
    "H_ONLY": {
        "description": "B2 with head-side one-hop context only; head and tail endpoints remain visible.",
        "CONTEXT_MODE": "adaptive",
        "MAX_HEAD_CONTEXT_TOKENS": 40,
        "MAX_TAIL_CONTEXT_TOKENS": 0,
    },
    "T_ONLY": {
        "description": "B2 with tail-side one-hop context only; head and tail endpoints remain visible.",
        "CONTEXT_MODE": "adaptive",
        "MAX_HEAD_CONTEXT_TOKENS": 0,
        "MAX_TAIL_CONTEXT_TOKENS": 40,
    },
}
for _key, _value in EXPERIMENT_MATRIX[EXPERIMENT_ID].items():
    if _key != "description":
        globals()[_key] = _value
EXPERIMENT_DESCRIPTION = EXPERIMENT_MATRIX[EXPERIMENT_ID]["description"]

METRICS_JSON = "metrics.jsonl"
CONFIG_JSON = "run_config.json"
GRAPH_CACHE_PREFIX = "graph_stats_train_only"
GRAPH_CACHE_VERSION = "v7_strict_final_ddp_safe_hf_local"
PAIR_OVERLAP_AUDIT_JSON = "pair_overlap_audit.json"

def print_config_summary():
    print(f"Dataset: {DATASET_NAME}")
    print(f"Experiment: {EXPERIMENT_ID} — {EXPERIMENT_DESCRIPTION}")
    print(f"Seed: {SEED}; Deterministic: {DETERMINISTIC}")
    print(f"Output directory: {EXPERIMENT_OUTPUT_DIR}")
    print(f"Device: {DEVICE}; GPUs: {NUM_GPUS}; DataLoader workers: {NUM_WORKERS}")
    print(f"Model: {MODEL_NAME}; batch={BATCH_SIZE}; max_length={MAX_LENGTH}")
    print(f"Context: mode={CONTEXT_MODE}, head_budget={MAX_HEAD_CONTEXT_TOKENS}, tail_budget={MAX_TAIL_CONTEXT_TOKENS}")
    print("Strict exclusions: pair=False, other-pair-relations=False, paths=False, second-hop=False, schema=False")
