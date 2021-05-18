# i6
import os

# Workdir path
if os.path.exists("/work"):
  workdir_base = "/work/asr3/zeyer"
else:
  workdir_base = "/tmp"

# Dataset path
# if os.path.exists("/work"):
#   dataset = "/work/asr3/zeyer/zhobro/setups-data/librispeech/dataset"
# else:
dataset = os.path.join(os.environ["HOME"], "datasets")

# Dump-align
if os.path.exists("/work"):
  dump_align = "/work/asr4/zeyer/setups-data/switchboard/2019-10-22--e2e-bpe1k/dump-align/"
else:
  dump_align = "/tmp"
