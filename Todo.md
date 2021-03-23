# Documentation of the scripts

## base_dir
- [x] Todo.md -- todo stuff
- [x] README.md -- basic workflow
- [x] notes.txt -- notes about the setups
- [x] settings.py  -- It updates the main Settings in tools-multisetup/tools.py which holds settings for the whole project.
- [x] setup-data-dir-info.py -- where the working directory should be kept(we register only links to it in base_dir) e.g.: workdir_base = "/tmp"
- [x] setup-data-dir.py -- creates the working directory. If setup-data-dir-info.py not filled it uses /tmp for the workdir
- [x] setup.sh -- setup the project
- [x] setup.py -- same as setup.sh but uses python
- [x] train.q.sh -- used to submit a training job to i6 cluster(e.g. qint.py train.q.sh -g 3)
- [x] recog.q.sh -- simple beam search recognition
- [x] recog.lm-gridsearch.q.sh -- does beam search recognition with LM shallow fusion

## tools-multisetup
- [x] _get_train_setup_dir.py -- Prints corresponding path of working dir data-train/$experiment/ for the given experiment config path. Used in shell scripts.
- [x] cleanup-all-except.py -- Cleans all setups except the ones given as arguments. For cleaning it calls `reset-train.py` and than deletes the config under config-train/*.config.
- [x] cleanup-old-models.py -- If use `--doit` it cleans otherwise prints old models in `data-train/model/net-model` that can be cleaned.
- [ ] collect-lur-stats.py
- [x] create-recog.sh $experiment $poch -- Creates a strucuture under data-recog with folders for each epoch the recognition is performed.
- [ ] auto-recog.py
- [x] qstat-recog.sh --- !!! WEIRD command pqstat !!!
- [x] start-recog.sh -- Makes sure the files in data-train and data-recog exist and Call `qint.py recog.q.sh -g 3` from `recog_dir/model/`
- [x] create-train.py $experiment -- Creates the structure of data-train where the data for different experiments are saved. (net-mode, log, qlog)
- [x] create-train.sh $experiment -- Calls create-train.py
- [x] start-train.sh $experiment -- Calls qint.py train.q.sh -g 3 from the data-train/experiment
- [x] qstat-train.sh -- !!! WEIRD command pqstat !!!
- [x] reset-train.py -- Stops training for $experiment, deletes `data-train/$experiment` and removes the corresponding files in scores/* and logs-archive/*.
- [x] stop-train.py $experiment -- Calls qdel after finding the jobid for the $experiment.
- [x] get-best-train-info-scores.py -- It extracts score information from score files, e.g. epoch with max score. If no file given it checks all files for the specified --key score_type. If file specified it prints information about all score_types for that file. With score type we mean the the name of the dataset the score is calculated on, e.g. devtrain_score, train_score etc.
- [ ] extract-scores.py
- [x] mark-finished-train.py -- Motivation: Used to mark a setup config as finished with a comment # multistep: $reason
- [x] rm-old-train-models.py -- Filter out N best setups(net-model/) - don't delete anything from them. From the remaining, delete all but the best epoch.
- [x] get-status.py -- Prints informaion about finished & incomplete running/not-running training and running jobs.
- [x] score-regression.py -- Reads in scores, tries to fit them to some simple model
- [x] show-log.py -- !! do a link to tools-multistep rather than copy.!! Simplifies navigating through the qlogs in qdir. It calls `$less $fn`for either recog(in data-recog/) or train(in data-train/) qlog files.
- [x] time-stats.py -- Allows you to collect time related information about trained models and maybe plot runtime vs wer.
- [ ] tools.py

- [ ] crnn@ -> ../returnn
- [ ] i6lib@ -> libs/i6lib
- [ ] lib@ -> libs/lib
- [ ] libs/

