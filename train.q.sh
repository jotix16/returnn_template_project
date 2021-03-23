#!qint.py
# Usage qint.py train.q.sh  (-g 3 for guarded 3 tries)

concurrent part:
    trainset 1

concurrent part

# If you want to change the amount of iterations:
# * Above, rename "it-<number>" such that <number> = number of iterations.
# * In recog.pass1.init, change ITER = number of iterations.

parallel train(qsub="-notify -hard -l h_vmem=32G -l h_rt=150:00:00 -l gpu=1 -l qname='*2080*|*1080*|*TITAN*' -l num_proc=4 -l h_fsize=100G"):
    echo "Train. JOB_ID $JOB_ID"

    /u/zeyer/dotfiles/system-tools/helpers/cgroup-mem-log-rss-max.py &
    /u/zeyer/dotfiles/system-tools/helpers/cgroup-mem-limit-watcher.py &

    trap 'echo "received SIGUSR1 in train.q.sh" ' USR1
    trap 'echo "received SIGUSR2 in train.q.sh" ' USR2

    source /etc/lsb-release
    echo "Ubuntu $DISTRIB_RELEASE $DISTRIB_CODENAME"
    source /u/standard/settings/sge_settings.sh
    source base/activate-cuda.sh
    source /work/asr3/zeyer/merboldt/py-envs/py3.8-tf2.3/bin/activate
    PY="python3"

    source settings.sh # hear we source the variable $model
    stdbuf -oL $PY base/returnn/rnn.py config-train/$model.config | /u/zeyer/dotfiles/system-tools/bin/mt-cat.py
    exit ${PIPESTATUS[0]}
