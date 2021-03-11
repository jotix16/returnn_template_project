#!/usr/bin/env python3


import os
import sys
import argparse
import numpy
import tensorflow as tf
import better_exchook
from returnn.rnn import init
from returnn.Config import get_global_config
from returnn.TFEngine import get_global_engine, Runner
from returnn.TFNetworkLayer import HDFDumpLayer
from returnn.Dataset import init_dataset
from returnn.Util import load_txt_vector


my_dir = os.path.dirname(os.path.abspath(__file__))
setup_base_dir = os.path.dirname(my_dir)
data_dir = "%s/data" % my_dir


def main():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("setup")
  arg_parser.add_argument("--align-layer", default="ctc_align")
  arg_parser.add_argument("--prior-scale", default=None)
  arg_parser.add_argument("--extern-prior")
  arg_parser.add_argument("--with-scores")
  arg_parser.add_argument("--do-train-only", action="store_true")
  arg_parser.add_argument("--do-dev-only", action="store_true")
  arg_parser.add_argument("--epoch", type=int)
  arg_parser.add_argument("--batch_size", type=int)
  args = arg_parser.parse_args()

  config_filename = "%s/config-train/%s.config" % (setup_base_dir, args.setup)
  setup_dir = "%s/data-train/%s" % (setup_base_dir, args.setup)
  assert os.path.exists(config_filename) and os.path.isdir(setup_dir)

  if args.extern_prior and not args.extern_prior.startswith("/"):
    args.extern_prior = "%s/%s" % (os.getcwd(), args.extern_prior)
  os.chdir(setup_dir)
  config_updates = {
          "need_data": False,
          }
  if args.epoch:
      config_updates["load"] = "net-model/network.%03d" % args.epoch
      # config_updates["start_epoch"] = args.epoch - 1
      # config_updates["load_epoch"] = args.epoch
      config_updates["model"] = ""  #  force no models to be found
  print(config_updates)
  init(
    config_filename=config_filename,
    extra_greeting="dump-align",
    config_updates=config_updates)
  config = get_global_config()

  datasets_dict = {"train": config.typed_dict["train"], "dev": config.typed_dict["dev"]}
  if args.do_train_only:
      datasets_dict.pop("dev")
  if args.do_dev_only:
      datasets_dict.pop("train")
  assert len(datasets_dict) > 0
  for dataset_name, dataset_dict in datasets_dict.items():
    assert isinstance(dataset_dict, dict)
    assert dataset_dict["class"] == "LibriSpeechCorpus"
    dataset_dict["partition_epoch"] = 1
    dataset_dict["seq_ordering"] = "sorted_reverse"
    if "epoch_wise_filter" in dataset_dict:
        dataset_dict.pop("epoch_wise_filter")
    if "fixed_random_subset" in dataset_dict:
        dataset_dict.pop("fixed_random_subset")
    dataset_dict["name"] = dataset_name

  dump_layer_name = "%s_dump" % args.align_layer

  def net_dict_post_proc(net_dict):
    """
    :param dict[str] net_dict:
    :rtype: dict[str]
    """
    if "/" in args.align_layer:
        net_dict
        base_layer, sub_layer = args.align_layer.split("/")
        assert sub_layer in net_dict[base_layer]["unit"]
    else:
        assert args.align_layer in net_dict

    def remove_hdf_dump_layer(dict_, name, desc, rec_stack):
        if not isinstance(desc, dict):
            return
        if not "class" in desc:
            return
        if desc["class"] == "hdf_dump":
            print("Removing the hdf_dump layer %s:" % (rec_stack + name))
            layer = dict_.pop(name)
            print(layer)
        if desc["class"] == "rec" and isinstance(desc.get("unit", False), dict):
            sub_dict = desc["unit"]
            old_sub_dict = sub_dict.copy()
            for sub_layer, sub_desc in old_sub_dict.items():
                remove_hdf_dump_layer(sub_dict, sub_layer, sub_desc, rec_stack + (name + "/"))
    old_net_dict = net_dict.copy()
    for layer, desc in old_net_dict.items():
        remove_hdf_dump_layer(net_dict, layer, desc, rec_stack="")

    net_dict[dump_layer_name] = {
      "class": "hdf_dump", "from": args.align_layer,
      "filename": None,  # this will be set after net construction, below
      "is_output_layer": True}
    if args.with_scores:
        net_dict[dump_layer_name]["extra"] = {"scores": "%s/scores" % args.align_layer},  # we expect this is a forced_align layer or similar
    if args.prior_scale is not None:
      # Now some assumptions about the net.
      align_scores_layer_name = net_dict[args.align_layer]["from"]
      assert isinstance(align_scores_layer_name, str)  # single source
      align_scores_layer_dict = net_dict[align_scores_layer_name]
      assert "eval_locals" in align_scores_layer_dict
      align_scores_eval_locals = align_scores_layer_dict["eval_locals"]
      assert "prior_scale" in align_scores_eval_locals
      align_scores_eval_locals["prior_scale"] = float(args.prior_scale)
    if args.extern_prior:
      log_prior = numpy.array(load_txt_vector(args.extern_prior), dtype="float32")
      # Now some assumptions about the net.
      align_scores_layer_name = net_dict[args.align_layer]["from"]
      assert isinstance(align_scores_layer_name, str)  # single source
      align_scores_layer_dict = net_dict[align_scores_layer_name]
      assert "eval_locals" in align_scores_layer_dict
      align_scores_eval_locals = align_scores_layer_dict["eval_locals"]
      assert "prior_scale" in align_scores_eval_locals  # just a check
      assert "safe_log(source(1))" in align_scores_layer_dict["eval"]  # just a check (expected in prob space...)
      assert len(align_scores_layer_dict["from"]) == 2  # posteriors and priors
      align_posterior_layer_name, align_prior_layer_name = align_scores_layer_dict["from"]
      align_posterior_layer_dict = net_dict[align_posterior_layer_name]
      dim = align_posterior_layer_dict["n_out"]
      assert log_prior.shape == (dim,)
      assert align_prior_layer_name in net_dict
      net_dict[align_prior_layer_name] = {  # overwrite
        "class": "eval", "from": [],
        "out_type": {"shape": (dim,), "batch_dim_axis": None, "time_dim_axis": None},
        "eval": lambda **kwargs: tf.exp(tf.constant(log_prior))}  # safe_log will just remove the tf.exp
    # Fixup some att configs, really heuristic...
    if "decision" in net_dict:
      net_dict.pop("decision")
    # if "output" in net_dict and net_dict["output"]["class"] == "rec" and isinstance(net_dict["output"]["unit"], dict):
      # net_dict.pop("output")
    return net_dict

  engine = get_global_engine()
  engine.init_network_from_config(net_dict_post_proc=net_dict_post_proc)
  print("Initialized network, epoch:", engine.epoch)

  dump_layer = engine.network.layers[dump_layer_name]
  assert isinstance(dump_layer, HDFDumpLayer)

  for dataset_name, dataset_dict in datasets_dict.items():
    print("Load data", dataset_name, "...")
    dataset = init_dataset(dataset_dict)
    print(dataset)
    out_filename_parts = [args.setup, "epoch-%i" % engine.epoch]
    if args.extern_prior:
      out_filename_parts += ["extern_prior"]
    if args.prior_scale is not None:
      out_filename_parts += ["prior-%s" % args.prior_scale.replace(".", "_")]
    out_filename_parts += ["data-%s" % dataset_name, "hdf"]
    output_hdf_filename = "%s/%s" % (data_dir, ".".join(out_filename_parts))
    print("Store HDF as:", output_hdf_filename)
    assert not os.path.exists(output_hdf_filename)
    dump_layer.filename = output_hdf_filename

    dataset_batches = dataset.generate_batches(
      recurrent_net=engine.network.recurrent,
      batch_size=args.batch_size or config.typed_value('batch_size', 1),
      max_seqs=config.int('max_seqs', -1),
      used_data_keys=engine.network.get_used_data_keys())

    runner = Runner(
      engine=engine, dataset=dataset, batches=dataset_batches,
      train=False, eval=False)
    runner.run(report_prefix=engine.get_epoch_str() + " %r dump align" % dataset_name)
    if not runner.finalized:
      print("Runner not finalized, quitting.")
      sys.exit(1)
    assert dump_layer.hdf_writer  # nothing written?
    engine.network.call_graph_reset_callbacks()
    assert os.path.exists(output_hdf_filename)
    assert not dump_layer.hdf_writer  # reset did not work?

  print("Finished.")


if __name__ == '__main__':
  better_exchook.install()
  main()
