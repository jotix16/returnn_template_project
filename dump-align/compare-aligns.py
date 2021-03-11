#!/usr/bin/env python3


import argparse
import numpy
from pprint import pprint
from returnn.HDFDataset import HDFDataset
from returnn.Log import log
from returnn.Util import Stats, progress_bar_with_time
# import editdistance
import Levenshtein

hdf_files = [
        # 20: 50.99
        "data/rnnt-fs.bpe1k.readout.lm-embed256.lr1e_3.no-curric.bs4k.accum3.epoch-40.data-dev.hdf",
        # "data/rnnt-fs.bpe1k.readout.lm-embed256.lr1e_3.no-curric.bs4k.accum3.epoch-80.data-dev.hdf",  # dev-other: 24.29
        "data/rnnt-fs.bpe1k.readout.lm-embed256.lr1e_3.no-curric.bs4k.accum3.epoch-160.data-dev.hdf", # dev-other: 16.65
        "data/rnnt-fs.bpe1k.readout.lm-embed256.lr1e_3.no-curric.bs4k.accum3.epoch-240.data-dev.hdf",  # dev-other: 14.12
        "data/rnnt-fs.bpe1k.readout.lm-embed256.lr1e_3.no-curric.bs4k.accum3.epoch-320.data-dev.hdf",  # dev-other: 12.52
  ]


def compare_two_alignments(hdf1, hdf2, seq_list_file=None, blank_idx=0):
    dataset1 = HDFDataset(files=[hdf1], unique_seq_tags=True,
                          seq_list_filter_file=seq_list_file, seq_ordering="sorted")
    dataset2 = HDFDataset(files=[hdf2], unique_seq_tags=True,
                          seq_list_filter_file=seq_list_file, seq_ordering="sorted")
    dataset1.init_seq_order(epoch=1)
    dataset2.init_seq_order(epoch=1)
    print("Comparing:\n  - '%s'\n  - '%s'" % (hdf1, hdf2))
    print("# seqs: %d and %d" % (dataset1.num_seqs, dataset2.num_seqs))
    # assert dataset1.num_seqs == dataset2.num_seqs

    stats = Stats()
    seq_idx = 0
    n_blanks, n_symbols = [0, 0], [0, 0]
    numpy.set_printoptions(linewidth=120)
    accum_edit_ops = {"delete": 0, "insert": 0, "replace": 0}
    reflen, hyplen, shift_pos = 0, 0, 0
    mismatch = 0
    while dataset1.is_less_than_num_seqs(seq_idx):
        dataset1.load_seqs(seq_idx, seq_idx + 1)
        dataset2.load_seqs(seq_idx, seq_idx + 1)
        tag1 = dataset1.get_tag(seq_idx)
        tag2 = dataset2.get_tag(seq_idx)
        # print("%04d:" % seq_idx, "tags:", tag1, tag2)
        assert tag1 == tag2
        if tag1 != tag2:
            mismatch += 1
            seq_idx += 1
            continue
        data1 = dataset1.get_data(seq_idx, "data")
        data2 = dataset2.get_data(seq_idx, "data")
        str1 = "".join(map(chr, data1))
        str2 = "".join(map(chr, data2))
        reflen += len(data1)
        hyplen += len(data2)

        for i, data in enumerate([data1, data2]):
            n_blanks[i] += numpy.count_nonzero(data == blank_idx)
            n_symbols[i] += numpy.count_nonzero(data != blank_idx)

        edits = Levenshtein.editops(str1, str2)
        for op_name, spos, dpos in edits:
          # accum_edit_ops[op_name] += 1
          shift_pos += spos - dpos
        len_ds1 = len(data1)
        # print("%40s" % tag1, dist)
        # stats.collect(numpy.array([dist/len_ds1]))

        # assert data.ndim == 1
        # data = numpy.concatenate([[args.initial_t], data], axis=0)
        # step_sizes = data[1:] - data[:-1]
        # assert (step_sizes >= 0).all()
        # stats.collect(step_sizes)
        progress_bar_with_time(dataset1.get_complete_frac(seq_idx), suffix=str(stats))
        seq_idx += 1

    # stats.dump()

    print("Reference total length:", reflen)
    print("Hypothesis total length:", hyplen)
    print("Shift positions:", shift_pos)
    print("Shift positions per seq:", float(shift_pos) / seq_idx)
    print("Mismatch tags:", mismatch)

    for hdf_file, n_blank, n_symbol in zip([hdf1, hdf2], n_blanks, n_symbols):
        print("Dataset '%s'" % hdf_file)
        print("# blanks :", n_blank)
        print("# symbols:", n_symbol)
        print("# blanks/symbols: %.3f (#blanks=%d, #symbols=%d)" % (n_blank/n_symbol, n_blank, n_symbol))
        print()
    # print("Shift-pos > 0: source-pos > dest-pos")
    # print("Shift-pos < 0: dest-pos > source-pos")
    # print("Insertions:", accum_edit_ops["insert"])
    # print("Deletions:", accum_edit_ops["delete"])
    # print("Substitutions:", accum_edit_ops["replace"])



def main():
    arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument("hdf1")
    # arg_parser.add_argument("hdf2")
    # args = arg_parser.parse_args()
    # seq_list_file = "dependencies/seg_train_2x_enclen"
    # seq_list_file = "dependencies/seg_cv_2x_enclen"
    # seq_list_file = "dependencies/seg_cv"
    seq_list_file = None
    assert len(hdf_files) > 1
    ref_hdf = hdf_files[0]
    for other_hdf in hdf_files[1:]:
        compare_two_alignments(ref_hdf, other_hdf, seq_list_file=seq_list_file, blank_idx=1056)
        print()



if __name__ == "__main__":
    import returnn.better_exchook
    returnn.better_exchook.install()
    main()


