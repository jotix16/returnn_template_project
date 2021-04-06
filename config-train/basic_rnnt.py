#!crnn/rnn.py
# kate: syntax python;
# vim: ft=python sw=2:
# based on Andre Merboldt rnnt-fs.bpe1k.readout.zoneout.lm-embed256.lr1e_3.no-curric.bs12k.mgpu.retrain1.config

from returnn.import_ import import_

import_("github.com/jotix16/returnn-experiments", "common", None)
from returnn_import.github_com.jotix16.returnn_experiments.dev.common.common_config import *
from returnn_import.github_com.jotix16.returnn_experiments.dev.common.datasets.asr.librispeech import oggzip_2 as oggzip
from returnn_import.github_com.jotix16.returnn_experiments.dev.common.models.transducer.transducer_fullsum import make_net
from returnn_import.github_com.jotix16.returnn_experiments.dev.common.training.pretrain import Pretrain

from pathlib import Path
dataset_path = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute(), "base/dataset_symlink/LibriSpeech")
# data
globals().update(oggzip.Librispeech(path=dataset_path, audio_dim=40, vocab=oggzip.bpe10k).get_config_opts())
