# Project
The setup consists of several training experiments, and each training experiment can have a recognition on each of its epochs.
Every training experiment has one config in config-train, and that config name defines the experiment name. For the recognition, the same config will be used.

The directory (at least the configs, scores, train/recog scripts, etc) is under Git.
Returnn (crnn) and tools-multisetup (the scripts for managing the setup) are Git submodules.

All data files (models checkpoints etc) are on the work file-server as specified
in [setup-data-dir-info.py](setup-data-dir-info.py) using the symlink
[setup-data-dir-symlink](setup-data-dir-symlink) in the base_dir. Similiarly the dataset's location is
specified in [dataset-dir-info.py](dataset-dir-info.py) and symlinked with [dataset_symlink](dataset_symlink). 
The symlinks are automatically managed with [setup-data-dir.py](setup-data-dir.py). 

The files/folders kept in the work file-server [setup-data-dir-symlink](setup-data-dir-symlink) are:
- **data-train** -- logs, checkpoints created during training
- **data-recog** -- scores, logs created during recognition
- **logs-archive** -- not sure yet

The files/folders kept in the work file-server [dataset_symlink](dataset_symlink) are:
- **dataset_symlink** -- should link to the used dataset

### Creating a new setup directory
``` python
git clone https://github.com/jotix16/returnn_template_project my_project  # could clone an arbitrary project
cd my_project
./setup.sh  # to setup the submodules
python setup_data_dir.py  # to create the links to the work file-servers such as dataset/ and setup-data-dir-symlink/ ..
```
To check if experiment is working: on cluster-cn-211 or local PC: go to data-train/$experiment, 
- `qint.py train.q.sh -t 0`, or 
- `python crnn/rnn.py config-train/$experiment.config`.

### Training
Let's say you have config/$experiment.config.
1. `./create-train.py $experiment` -> creates **data-train/\$experiment for config-train/\$experiment.config**
2. `./start-train.sh $experiment` -> submit to cluster
3. `./get-status.py`: status of all experiments, also running training/recognition jobs

**data-train/$experiment/qdir/q.log/*** holds stdout of the training.


### Recognition
1. `./create-recog.sh $experiment $epoch` -> creates **data-recog/\$experiment.$epoch**
2. `./start-recog.sh $experiment $epoch` -> starts the recognition of given model at the given epoch.
3. `./extract-scores.py` -> collect scores from data-train and data-recog, saves it in **scores/*** and **logs-archive/***
4. `./auto-recog.py`: automatically calls extract-scores.py to get the current
  scores, then automatically calls {create,start}-recog on suggested recognition
  epochs, and also commits all scores changes to Git. It also automatically
  cleans up finished recognitions (i.e. the **data-recog/\$experiment.\$epoch**
  directory will be deleted; all important logs should have been saved in
  **logs-archive/\$experiment.\$epoch.recog**).

Based on the scores (via extract-scores.py), some of the tools, e.g. get-status.py will automatically suggest which epoch might be interesting to do a recognition on, e.g. the one which has the best dev score, etc.


### Tools
Most of the tools are symlinked to [tools-multisetup](tools-multisetup/), and via these tools, everything is managed. 
For the moment these should be run on the cluster (e.g. cluster-cn-01) but we'll
try to make them available for noncluster training too, such as colab, gcp or
single gpu training at home. A full description of all tools can be found in [Tools](Tools).

Other tools:
* /u/beck/bin/gpu_status.py: how much other gpu jobs in the queue
* compare to https://github.com/syhw/wer_are_we
