Switchboard 300h

see also:
* ../2018-10-02--e2e-bpe1k
* ../2018-01-03--end2end
* /u/irie/setups/switchboard/2018-02-13--end2end-zeyer
* /u/irie/setups/switchboard/2018-03-09--end2end-lmscale
* /u/merboldt/setups/2018-02-15--thesis-attention
* /u/zeyer/Documents/2018-asr-att-paper
* .history*


This dir:

Some more info how I handle these setups, maybe you want to follow that:

* There is a README in that dir, which also has some of this information.
* The setup consists of several training experiments, and each training experiment can have a recognition on each of its epochs.
* Every training experiment has one config in config-train, and that config name defines the experiment name. For the recognition, the same config will be used.
* The directory (at least the configs, scores, train/recog scripts, etc) is under Git, so I keep track of all changes.
* Returnn (crnn) and tools-multisetup (the scripts for managing the setup) are Git submodules.
* All data files (models etc) are on the work file-server and my script /u/zeyer/dotfiles/bin/setup-data-dir.py automatically manages symlinks. The file setup-data-dir-info.py controls how setup-data-dir.py works (e.g. on what work file-server to create the data dirs).
* To create a new setup directory, I often use /u/zeyer/dotfiles/bin/git-clone-setup.py, which basically does git clone, and updates the Git submodules, and then it setups the paths on the work file-servers.
* To check if experiment is working: on cluster-cn-211 or local PC: go to data-train/$experiment, `qint.py train.q.sh -t 0`, or `python crnn/rnn.py config-train/$experiment.config`.

Then I symlinked some of the tools in tools-multisetup to the base setup directory, and via these tools, I basically manage everything. These should be run on the cluster (e.g. cluster-cn-01).
Let's say you have config/$experiment.config.

* ./get-status.py: status of all experiments, also running training/recognition jobs
* ./create-train.py $experiment -> creates data-train/$experiment for config-train/$experiment.config
* ./start-train.sh $experiment -> submit to cluster
* data-train/$experiment/qdir/q.log/* has stdout of the training
* ./extract-scores.py -> collect scores from data-train and data-recog, saves it in scores/* and logs-archive/*
* ./create-recog.sh $experiment $epoch -> creates data-recog/$experiment.$epoch
* ./start-recog.sh $experiment $epoch

Based on the scores (via extract-scores.py), some of the tools, e.g. get-status.py will automatically suggest which epoch might be interesting to do a recognition on, e.g. the one which has the best dev score, etc.

* ./auto-recog.py: automatically calls extract-scores.py to get the current scores, then automatically calls {create,start}-recog on suggested recognition epochs, and also commits all scores changes to Git. It also automatically cleans up finished recognitions (i.e. the data-recog/$experiment.$epoch directory will be deleted; all important logs should have been saved in logs-archive/$experiment.$epoch.recog).


Other tools:

* /u/beck/bin/gpu_status.py: how much other gpu jobs in the queue


* compare to https://github.com/syhw/wer_are_we



Trafo LM:
Example: /u/zeyer/setups/switchboard/2018-10-02--e2e-bpe1k/config-train/hard-att-local-win10-imp-retrain1-recog-lm.ls01.laplace1000.hlr.config

LSTM LM:
Example: /u/irie/setups/switchboard/2018-03-09--end2end-lmscale/config-train/base2.specaug4.lstm_lm_fusion.config
    lm_model_filename = "/work/asr3/irie/experiments/lm/switchboard/2018-01-23--lmbpe-zeyer/data-train/bpe1k_clean_i256_m2048_m2048.sgd_b16_lr0_cl2.newbobabs.d0.2/net-model/network.023"
      "lm_output": { "class": "subnetwork", "from": ["prev:output"], "load_on_init": lm_model_filename, "n_out": 1030,
        "subnetwork": {
          "input": {"class": "linear", "n_out": 256, "activation": "identity"},
          "lstm0": {"class": "rnn_cell", "unit": "LSTMBlock", "dropout": 0.2, "n_out": 2048, "unit_opts": {"forget_bias": 0.0}, "from": ["input"]},
          "lstm1": {"class": "rnn_cell", "unit": "LSTMBlock", "dropout": 0.2, "n_out": 2048, "unit_opts": {"forget_bias": 0.0}, "from": ["lstm0"]},
          "output": {"class": "linear", "from": ["lstm1"], "activation": "identity", "dropout": 0.2, "n_out": 1030}
          }},
      "lm_output_prob" : {"class": "activation", "activation": "softmax", "from": ["lm_output"], "target": "bpe"},
