#!qint.py

concurrent part:
    20
    40
    80
    160
    320

concurrent part

# If you want to change the amount of iterations:
# * Above, rename "it-<number>" such that <number> = number of iterations.
# * In recog.pass1.init, change ITER = number of iterations.

parallel dump-align(qsub="-notify -hard -l h_vmem=32G -l h_rt=20:00:00 -l gpu=1 -l qname='*1080*|*TITAN*' -l num_proc=4 -l h_fsize=100G",qsub-log-dir="logs/"):
    echo "dump-align. JOB_ID $JOB_ID"

    /u/zeyer/dotfiles/system-tools/helpers/cgroup-mem-log-rss-max.py &
    /u/zeyer/dotfiles/system-tools/helpers/cgroup-mem-limit-watcher.py &

    trap 'echo "received SIGUSR1 in train.q.sh" ' USR1
    trap 'echo "received SIGUSR2 in train.q.sh" ' USR2

    source /etc/lsb-release
    echo "Ubuntu $DISTRIB_RELEASE $DISTRIB_CODENAME"
    source /u/standard/settings/sge_settings.sh
    source ../activate-cuda.sh
    source /work/asr3/zeyer/merboldt/py-envs/py3.8-tf2.3/bin/activate
    source settings.sh
    PY="python3"

    source settings.sh
    #stdbuf -oL $PY base/returnn/rnn.py config-train/$model.config | /u/zeyer/dotfiles/system-tools/bin/mt-cat.py
    stdbuf -oL $PY dump-align.py --align-layer output/fullsum_alignment0 --batch_size 12000 --epoch $TASK_ID $model | /u/zeyer/dotfiles/system-tools/bin/mt-cat.py
    exit ${PIPESTATUS[0]}
