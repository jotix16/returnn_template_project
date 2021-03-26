# i6
import os

# Workdir path
if os.path.exists("/work"):
  workdir_base = "/work/asr3/zeyer"
else:
  workdir_base = "/tmp"

# Dataset path
if os.path.exists("/work"):
  dataset = "/work/asr3/zeyer/zhobro/setups-data/librispeech/dataset"
else:
  dataset = os.path.join(os.environ["HOME"], "datasets/LibriSpeech")
