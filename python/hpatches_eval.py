"""Evaluation code for the HPatches homography patches dataset.

Usage:
  hpatches_eval.py (-h | --help)
  hpatches_eval.py --version
  hpatches_eval.py --descr-name=<> --task=<>... [--descr-dir=<>] [--split=<>] [--dist=<>] [--delimiter=<>] [--pcapl=<>] [--del=<>]
Options:
  -h --help        Show this screen.
  --version        Show version.
  --descr-name=<>  Descriptor name, e.g. sift
  --descr-dir=<>   Descriptor results root folder  [default: ../data/descriptors]
  --task=<>        Task name. Valid tasks are {verification,matching,retrieval}.
  --split=<>       Split name. Valid are {a,b,c,full,illum,view} [default: a].
  --dist=<>        Distance name. Valid are {L1,L2} [default: L2]
  --delimiter=<>   Delimiter used in the csv files [default: ,]
  --pcapl=<>       Compute results for pca-power law descr [default: no]
  --del=<>          Compute anyway [default: 0]

For more visit: https://github.com/hpatches/
"""
from utils.hpatch import *
from utils.tasks import *
from utils.misc import *
from utils.docopt import docopt
import os
import time
import dill

# cahnge delimiter to ; to evaluate rootsift

if __name__ == '__main__':
    opts = docopt(__doc__, version='HPatches 1.0')
    path = os.path.join(opts['--descr-dir'],opts['--descr-name'])

    try:
        assert os.path.exists(path)
    except:
       print("%r does not exist." % (path))
       exit(0)
    
    if not os.path.exists('results'):
        os.makedirs('results')

    descr_name = opts['--descr-name']
    print('\n>> Running HPatch evaluation for %s' % blue(descr_name))
        
    descr = load_descrs(path,dist=opts['--dist'],sep=opts['--delimiter'])
    print('AAAAA')

    with open('../tasks/splits/splits.json') as f:
        splits = json.load(f)

    splt = splits[opts['--split']]
    
    for t in opts['--task']:
        if os.path.exists("results/"+descr_name+"_"+t+"_"+splt['name']+".p") and opts['--del']!='1':
            print("Results for the %s, %s task, split %s, already cached!" %\
                  (descr_name,t,splt['name']))
        else:
            res = methods[t](descr,splt)
            dill.dump( res, open( "results/"+descr_name+"_"+t+"_"+splt['name']+".p", "wb"))

    # do the PCA/power-law evaluation if wanted
    if opts['--pcapl']!='no':
        print('>> Running evaluation for %s normalisation' % blue("pca/power-law"))
        compute_pcapl(descr,splt)
        for t in opts['--task']:
            if os.path.exists("results/"+descr_name+"_pcapl_"+t+"_"+splt['name']+".p"):
                print("Results for the %s, %s task, split %s,PCA/PL already cached!" %\
                      (descr_name,t,splt['name']))
            else:
                res = methods[t](descr,splt)
                dill.dump( res, open( "results/"+descr_name+"_pcapl_"+t+"_"+splt['name']+".p", "wb"))

# HardNet_handpicked_v3_png_id:26_PS:30000PP_WF:Hessian_PG:sumImg_masks:1_ang:0_spx:0_spy:0_min_tps:5000000_camsB:0_ep:20_as