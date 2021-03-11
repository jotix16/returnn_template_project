#!qint.py

concurrent part:
    dev-clean
    dev-other
    test-clean
    test-other

concurrent final:
    final


concurrent part

parallel search(qsub="-notify -hard -l h_vmem=15G -l h_rt=01:40:00 -l gpu=1 -l num_proc=2"):
    echo "Recog. JOB_ID $SGE_JOB_ID, $JOB_ID, $TASK_ID"

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

    echo "CUDA_VISIBLE_DEVICES = '$CUDA_VISIBLE_DEVICES'"

    source settings.sh
    stdbuf -oL $PY base/search.py $model $epoch \
        --data $TASK_ID \
        --recog_prefix scoring-$TASK_ID --out_dir . \
        --extra_recog_options "${extra_recog_options}" \
        --device gpu \
        -- \
        ++batch_size 40000 \
        | /u/zeyer/dotfiles/system-tools/bin/mt-cat.py
    exit ${PIPESTATUS[0]}


# Do a single final action to make sure everything went through.
concurrent final

sequential finish(qsub="-notify -hard -l h_vmem=500M -l h_rt=00:01:00"):
    (for corpus in dev-clean dev-other test-clean test-other; do
        f=scoring-$corpus.scoring.wer
        echo "$corpus: $(cat $f)"
    done) > scoring.wers
