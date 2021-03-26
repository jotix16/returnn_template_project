import os

if os.path.exists("/work"):
  dataset = "/work/asr3/zeyer/zhobro/setups-data/librispeech/dataset"
else:
  dataset = os.path.join(os.environ["HOME"], "datasets/LibriSpeech")