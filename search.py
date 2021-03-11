#!/usr/bin/env python3

import better_exchook
better_exchook.install()

import argparse
import sys
import os
import time
from subprocess import check_output

my_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "%s/tools-multisetup" % my_dir)
import tools

default_python_bin = tools.Settings.default_python
returnn_dir_name = "base/%s" % tools.Settings.returnn_dir_name


def run(args, **kwargs):
    import subprocess
    kwargs = kwargs.copy()
    print("$ %s" % " ".join(args), {k: v if k != "input" else "..." for (k, v) in kwargs.items()})
    try:
        subprocess.run(args, check=True, **kwargs)
    except AttributeError:
        subprocess.check_call(args, **kwargs)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        sys.exit(1)


argv = sys.argv[1:]
if "--" in argv:
    argv, returnn_argv = argv[:argv.index("--")], argv[argv.index("--") + 1:]
else:
    returnn_argv = []

argparser = argparse.ArgumentParser()
argparser.add_argument("model")
argparser.add_argument("epoch", type=int)
argparser.add_argument("--data", default="dev", help="cv, dev, hub5e_01, rt03s")
argparser.add_argument("--beam_size", type=int, default=12)
argparser.add_argument("--extra_recog_options", type=str)
argparser.add_argument("--device", default="cpu")
argparser.add_argument("--use_existing", action="store_true")
argparser.add_argument("--allow_tmp", action="store_true")
argparser.add_argument("--out_dir")
argparser.add_argument("--recog_prefix")
argparser.add_argument("--search_output_layer", default="decision")
args = argparser.parse_args(argv)

start_time = time.time()

config_fn = "base/config-train/%s.config" % args.model
assert os.path.exists(config_fn)
train_setup_dir = check_output(["base/tools-multisetup/_get_train_setup_dir.py", config_fn]).strip().decode("utf8")
assert os.path.lexists(train_setup_dir)
if not os.path.exists(train_setup_dir + "/base"):  # broken symlink
    print("Fixup base symlink.")
    os.remove(train_setup_dir + "/base")
    os.symlink(os.path.abspath("base"), train_setup_dir + "/base")

out_dir = "data-train/%s" % args.model
if args.out_dir:
    out_dir = args.out_dir
if args.recog_prefix:
    recog_prefix = "%s/%s" % (out_dir, args.recog_prefix)
else:
    recog_prefix = "%s/search.%s.ep%i.beam%i.recog" % (out_dir, args.data, args.epoch, args.beam_size)

extra_recog_opts = {}
if args.extra_recog_options:
    assert isinstance(args.extra_recog_options, str)
    assert args.extra_recog_options.startswith("{"), "extra recog options not a dict."
    extra_recog_opts = eval(args.extra_recog_options)
    print("Got extra recog options:", extra_recog_opts)

targets = extra_recog_opts.get("targets", "bpe")

assert targets in ("bpe", "chars")

recog_out_file = "%s.%s" % (recog_prefix, targets)
recog_words_file = "%s.words" % recog_prefix
recog_wer_file = "%s.scoring.wer" % recog_prefix


def check_recog_out_file():
    with open(recog_out_file, "w") as f:
        f.close()
    os.remove(recog_out_file)


if args.use_existing:
    assert os.path.exists(recog_out_file), "--use_existing but file does not exist"
    print("Using existing file: %s" % recog_out_file)

else:
    try:
        check_recog_out_file()
    except OSError as exc:
        if "Disk quota" in str(exc) and args.allow_tmp:
            print("Disk full? Using alternative path.")
            recog_prefix = "%s/.tmp-search.%s.%s.ep%i.beam%i.recog" % (my_dir, args.model, args.data, args.epoch, args.beam_size)
            if os.path.exists(recog_out_file):
                os.remove(recog_out_file)
            check_recog_out_file()
        else:
            raise

    run([
        default_python_bin,
        "%s/rnn.py" % returnn_dir_name, config_fn, "++load_epoch", "%i" % args.epoch,
        "++device", args.device,
        "--task", "search", "++search_data", "config:get_dataset(%r)" % args.data,
        "++beam_size", "%i" % args.beam_size,
        "++need_data", "False",  # the standard datasets (train, dev in config) are not needed to be loaded
        "++max_seq_length", "0",
        "++search_output_file", os.path.abspath(recog_out_file),
        "++search_output_file_format", "py",
        "++search_do_eval", "0",
        "++search_output_layer", args.search_output_layer,
        ] +
        returnn_argv,
        cwd=train_setup_dir)

    assert os.path.exists(recog_out_file)

if os.path.exists(recog_words_file):
    os.remove(recog_words_file)
if targets == "bpe":
    run(["tools/search-bpe-to-words.py", recog_out_file, "--out", recog_words_file])
elif targets == "chars":
    run(["tools/search-chars-to-words.py", recog_out_file, "--out", recog_words_file])
else:
    assert False


run([
    default_python_bin,
    "%s/tools/calculate-word-error-rate.py" % returnn_dir_name,
    "--expect_full",
    "--hyps", recog_words_file,
    "--refs", "base/dataset/%s.trans.raw" % args.data,
    "--out", recog_wer_file,
    ])

print("elapsed time: %s" % (time.time() - start_time))
