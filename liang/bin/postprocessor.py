# -*- coding: utf-8 -*-
# ! /usr/bin/python

import numpy as np
import getopt
import sys


class PostProcessor(object):

    @staticmethod
    def read_result(filename):
        fin = open(filename)
        fin.readline()
        ret = {}
        for line in fin:
            part = line.strip().split(',')
            ret[part[0]] = float(part[1])
        return ret

    @staticmethod
    def write_result(filename, ret):
        fout = open(filename, 'w')
        print >> fout, 'test_id,is_duplicate'
        for idx in ret:
            print >> fout, ','.join(map(str, [idx, ret[idx]]))
        fout.close()

    @staticmethod
    def merge(res_list):
        res = {}
        for idx in res_list[0]:
            res[idx] = np.average([res_list[x][idx] for x in range(len(res_list))])
        return res

    @staticmethod
    def inv_logit(p):
        p = np.array(p)
        return np.exp(p) / (1.0 + np.exp(p))

    @staticmethod
    def logit(p):
        p = np.array(p)
        return np.log(p / (1 - p))

    @staticmethod
    def merge_logit(res_list):
        res = {}
        for idx in res_list[0]:
            res[idx] = PostProcessor.inv_logit(np.average(PostProcessor.logit([res_list[x][idx] for x in range(len(res_list))])))
        return res

    @staticmethod
    def run_merge(argv):
        in_fnames = None
        out_fname = None

        try:
            opts, args = getopt.getopt(argv[1:], 'i:o:', ['in_fnames=', 'out_fname='])
        except getopt.GetoptError:
            print 'Postprocessor.run_merge -i <input_file_names> -o <output_file_name>'
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-i', '--in_fnames'):
                in_fnames = arg
            elif opt in ('-o', '--out_fname'):
                out_fname = arg

        assert None is not in_fnames, 'Postprocessor.run_merge -i <input_file_names> -o <output_file_name>'
        assert None is not out_fname, 'Postprocessor.run_merge -i <input_file_names> -o <output_file_name>'

        res_list = []
        for in_fname in in_fnames.strip().split(','):
            res = PostProcessor.read_result(in_fname)
            res_list.append(res)
        res_merge = PostProcessor.merge_logit(res_list)
        PostProcessor.write_result(out_fname, res_merge)

if __name__ == "__main__":
    PostProcessor.run_merge(sys.argv)

