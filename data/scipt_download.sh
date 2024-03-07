#!/usr/bin/env bash
curr_dir=$(pwd)

mkdir -p data
mkdir -p data/datasets

wget -r -nH --cut-dirs=100 --reject "index.html*" --no-parent http://lavis.cs.hs-rm.de/storage/spert/public/datasets/conll04/ -P ${curr_dir}/data/datasets/conll04
wget -r -nH --cut-dirs=100 --reject "index.html*" --no-parent http://lavis.cs.hs-rm.de/storage/spert/public/datasets/scierc/ -P ${curr_dir}/data/datasets/scierc
wget -r -nH --cut-dirs=100 --reject "index.html*" --no-parent http://lavis.cs.hs-rm.de/storage/spert/public/datasets/ade/ -P ${curr_dir}/data/datasets/ade
wget -r -nH --cut-dirs=100 --reject "index.html*" --no-parent http://lavis.cs.hs-rm.de/storage/jerex/public/datasets/docred/ -P ${curr_dir}/data/datasets/docred
wget -r -nH --cut-dirs=100 --reject "index.html*" --no-parent http://lavis.cs.hs-rm.de/storage/jerex/public/datasets/docred_joint/ -P ${curr_dir}/data/datasets/docred_join