# Loaded by tools-multisetup/tools/_init which calls tools-multisetup/tools/libs/load_config_py.
# It updates the main Settings in tools-multisetup/tools.py
# It holds settings for whole project.

import os

returnn_dir_name = "returnn"
recog_score_file = "scoring.wers"
recog_metric_name = "wer"
recog_get_score_tool = "tools/get-dev-other-wer.sh"
recog_score_lower_is_better = True
default_python = "python3"
