# Documentation of the scripts

## base_dir
- [Todo.md](Todo.md) -- todo stuff
- [README.md](README.md) -- basic workflow
- [notes.txt](notes.txt) -- notes about the setups
- [settings.py](settings.py)  -- Configuration file that updates/overwrites the main Settings in `tools-multisetup/tools.py` which holds settings for the whole project.
- [setup-data-dir-info.py](setup-data-dir-info.py) -- where the working directory should be kept(we register only links to it in base_dir) e.g.: `workdir_base = "/tmp"`
- [setup-data-dir.py](setup-data-dir.py) -- creates the working directory. If [setup-data-dir-info.py](setup-data-dir-info.py) not filled it uses `/tmp` for the workdir
- [setup.sh](setup.sh) -- setup the project
- [setup.py](setup.py) -- same as setup.sh but uses python
- [train.q.sh](train.q.sh) -- used to submit a training job to i6 cluster(e.g. `qint.py train.q.sh -g 3`)
- [recog.q.sh](recog.q.sh) -- simple beam search recognition
- [recog.lm-gridsearch.q.sh](recog.lm-gridsearch.q.sh) -- does beam search recognition with LM shallow fusion
- [search py](search.py) --
- [activate-cuda.sh](activate-cuda.sh) -- sources executables required for cuda
- [dataset-dir-info.py](dataset-dir-info.py) -- holds the path for the datasets
- [dataset](dataset) -- link to the datasets given in [dataset-dir-info.py](dataset-dir-info.py)

## Links from tools-multisetup/
1. [auto-recog.py](tools-multisetup/auto-recog.py) --
2. [create-train.sh](tools-multisetup/create-train.sh) \$**experiment** -- Calls [create-train.py](create-train.py)
3. [start-train.sh](tools-multisetup/start-train.sh) \$**experiment** -- Calls `qint.py train.q.sh -g 3` from the `data-train/experiment`
4. [stop-train.py](tools-multisetup/stop-train.py) \$**experiment** -- Calls qdel after finding the jobid for the \$**experiment**.
5. [extract-scores.py](tools-multisetup/extract-scores.py) --
6. [get-status.py](tools-multisetup/get-status.py) -- Prints informaion about finished & incomplete running/not-running training and running jobs.
7. [organize-configs.py](tools-multisetup/organize-configs.py) --
8. [reset-train.py](tools-multisetup/reset-train.py) -- Stops training for $experiment, deletes `data-train/\$experiment` and removes the corresponding files in `scores/*` and `logs-archive/*`.
9. [start-recog.sh](tools-multisetup/start-recog.sh) -- Makes sure the files in data-train and data-recog exist and Call `qint.py recog.q.sh -g 3` from `recog_dir/model/`


## tools-multisetup
1. [_get_train_setup_dir.py](tools-multisetup/_get_train_setup_dir.py) -- Prints corresponding path of working dir `data-train/$experiment/` for the given experiment config path. Used in shell scripts.
2. [cleanup-all-except.py](tools-multisetup/cleanup-all-except.py) -- Cleans all setups except the ones given as arguments. For cleaning it calls `reset-train.py` and than deletes the config under config-train/*.config.
3. [cleanup-old-models.py](tools-multisetup/cleanup-old-models.py) -- If use `--doit` it cleans otherwise prints old models in `data-train/model/net-model` that can be cleaned.
4. [collect-lur-stats.py](tools-multisetup/collect-lur-stats.py) --
5. [create-recog.sh](tools-multisetup/create-recog.sh) \$**experiment** \$**epoch** -- Creates a strucuture under data-recog with folders for each epoch the recognition is performed.
6. [qstat-recog.sh](tools-multisetup/qstat-recog.sh) -- !!! WEIRD command pqstat !!!
7. [create-train.py](tools-multisetup/create-train.py) \$**experiment** -- Creates the structure of data-train where the data for different experiments are saved. (net-mode, log, qlog)
8. [qstat-train.sh](tools-multisetup/qstat-train.sh) -- !!! WEIRD command pqstat !!!
9. [get-best-train-info-scores.py](tools-multisetup/get-best-train-info-scores.py) -- It extracts score information from score files, e.g. epoch with max score. If no file 10. given it checks all files for the specified --key score_type. If file specified it prints information about all score_types for that file. With 11. score type we mean the the name of the dataset the score is calculated on, e.g. devtrain_score, train_score etc.
12. [mark-finished-train.py](tools-multisetup/mark-finished-train.py) -- Used to mark a setup config as finished with a comment `# multistep: $reason`
13. [rm-old-train-models.py](tools-multisetup/rm-old-train-models.py) -- Filter out N best setups in `net-model/` - don't delete anything from them. From the remaining, delete all but the best epoch.
14. [score-regression.py](tools-multisetup/score-regression.py) -- Reads in scores, tries to fit them to some simple model
15. [show-log.py](tools-multisetup/show-log.py) -- !! do a link to tools-multistep rather than copy.!! Simplifies navigating through the qlogs in `qdir`. It calls `$less $fn`for either recog(in `data-recog/`) or train(in `data-train/`) qlog files.
16. [time-stats.py](tools-multisetup/time-stats.py) -- Allows you to collect time related information about trained models and maybe plot runtime vs wer.
17. [tools.py](tools-multisetup/tools.py) --


## Folders
- [ ] [crnn@](crnn) [->]() ../returnn
- [ ] [libs@](libs) -- tools to work with shell
- [ ] [i6lib@](i6lib) [->]() libs/i6lib
- [ ] [lib@](lib) [->]() libs/lib

