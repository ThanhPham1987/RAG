# PyGaggle: Baselines on [MS MARCO Document Retrieval](https://github.com/microsoft/TREC-2019-Deep-Learning)

This page contains instructions for running various neural reranking baselines on the MS MARCO *document* ranking task. 
Note that there is also a separate [MS MARCO *passage* ranking task (dev subset)](https://github.com/castorini/pygaggle/blob/master/docs/experiments-msmarco-passage-subset.md) and a separate [MS MARCO *passage* ranking task (entrie dev set)](https://github.com/castorini/pygaggle/blob/master/docs/experiments-msmarco-passage-entire.md).

Prior to running this, we suggest looking at our first-stage [BM25 ranking instructions](https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-doc.md).
We rerank the BM25 run files that contain ~1000 documents per query using monoT5.
monoT5 is a pointwise reranker. This means that each document is scored independently using T5.

Since it can take many hours to run these models on all of the 5193 queries from the MS MARCO dev set, we will instead use a subset of 50 queries randomly sampled from the dev set. 

Note 1: Run the following instructions at root of this repo.
Note 2: Make sure that you have access to a GPU
Note 3: Installation must have been done from source and make sure the [anserini-eval](https://github.com/castorini/anserini-eval) submodule is pulled. 
To do this, first clone the repository recursively.

```
git clone --recursive https://github.com/castorini/pygaggle.git
```

Then install PyGaggle using:

```
pip install pygaggle/
```

## Models

+ monoT5-base: Document Ranking with a Pretrained Sequence-to-Sequence Model [(Nogueira et al., 2020)](https://arxiv.org/pdf/2003.06713.pdf)

## Data Prep

We're first going to download the queries, qrels and run files corresponding to the MS MARCO set considered. The run file is generated by following the BM25 ranking instructions. We'll store all these files in the `data` directory.

```
wget https://www.dropbox.com/s/8lvdkgzjjctxhzy/msmarco_doc_ans_small.zip -P data
```

To confirm, `msmarco_doc_ans_small.zip` should have MD5 checksum of `aeed5902c23611e21eaa156d908c4748`.

Next, we extract the contents into `data`. 

```
unzip data/msmarco_doc_ans_small.zip -d data
```

`msmarco_doc_ans_small` contains two disjoint sets, `fh` and `sh`, and each set has 25 queries.

Let's download the pre-built MS MARCO index :

```
wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/index-msmarco-doc-20201117-f87c94.tar.gz
```

`index-msmarco-doc-20201117-f87c94.tar.gz` should have MD5 checksum of `ac747860e7a37aed37cc30ed3990f273`.
Then, we can extract it into into `indexes`:

```
tar xvfz index-msmarco-doc-20201117-f87c94.tar.gz -C indexes
rm index-msmarco-doc-20201117-f87c94.tar.gz
```

Now, we can begin with re-ranking the set.

## Re-Ranking with monoT5

Let us now re-rank the first half:

```
python -um pygaggle.run.evaluate_document_ranker --split dev \
                                                --method t5 \
                                                --model castorini/monot5-base-msmarco \
                                                --dataset data/msmarco_doc_ans_small/fh \
                                                --model-type t5-base \
                                                --task msmarco \
                                                --index-dir indexes/index-msmarco-doc-20201117-f87c94 \
                                                --batch-size 32 \
                                                --output-file runs/run.monot5.doc_fh.dev.tsv
```

The following output will be visible after it has finished:

```
precision@1 0.2
recall@3  0.56
recall@50  0.84
recall@1000 0.88
mrr     0.38882
mrr@10   0.38271
```

It takes about 5 hours to re-rank this subset on MS MARCO using a P100. 
It is worth noting again that you might need to modify the batch size to best fit the GPU at hand.

Upon completion, the re-ranked run file `runs/run.monot5.doc_fh.dev.tsv` will be available in the `runs` directory.

We can modify the argument for `--dataset` to `data/msmarco_doc_ans_small/sh` to re-rank the second half of the dataset, and don't forget to change output file name.

The results are as follows:

```
precision@1 0.28
recall@3  0.32
recall@50  0.8
recall@1000 0.88
mrr     0.33617
mrr@10   0.31978
```




If you were able to replicate these results, please submit a PR adding to the replication log!


## Replication Log

+ Results replicated by [@HangCui0510](https://github.com/HangCui0510) on 2020-07-08 (commit [`f2e078e`](https://github.com/HangCui0510/pygaggle/commit/f2e078e47c87156925a9151632753be861ec403d)) (Tesla P100)
+ Results replicated by [@mrkarezina](https://github.com/mrkarezina) on 2020-07-20 (commit [`c1a54cb`](https://github.com/castorini/pygaggle/commit/c1a54cb012a1d4ea24a2ce2bc24298417279a9c4)) (Tesla T4)
+ Results replicated by [@justinborromeo](https://github.com/justinborromeo) on 2020-09-08 (commit[`94befbd`](https://github.com/castorini/pygaggle/commit/94befbd58b19c3e46d930e67797102bf174efd01)) (GTX960M)
+ Results replicated by [@yuxuan-ji](https://github.com/yuxuan-ji) on 2020-09-09 (commit[`94befbd`](https://github.com/castorini/pygaggle/commit/94befbd58b19c3e46d930e67797102bf174efd01)) (Tesla T4 on Colab)
+ Results replicated by [@LizzyZhang-tutu](https://github.com/LizzyZhang-tutu) on 2020-09-09 (commit[`8eeefa5`](https://github.com/castorini/pygaggle/commit/8eeefa578c65e2da78be129c87dfb40beb74099c)) (Tesla T4 on Colab)
+ Results replicated by [@qguo96](https://github.com/qguo96) on 2020-09-10 (commit[`a1461f5`](https://github.com/castorini/pygaggle/commit/a1461f5e6bd7c2c5fd00d3586d9eef735d978f06)) (Tesla K80 on Colab)
+ Results replicated by [@wiltan-uw](https://github.com/wiltan-uw) on 2020-09-13 (commit[`41513a9`](https://github.com/castorini/pygaggle/commit/41513a9f496bd59523993ce134cc35a7b881e5a1)) (RTX 2070S)
+ Results replicated by [@jhuang265](https://github.com/jhuang265) on 2020-10-18 (commit[`e815051`](https://github.com/castorini/pygaggle/commit/e815051f2cee1af98b370ee030b66c07a8a287f3)) (Tesla P100 on Colab)
+ Results replicated by [@stephaniewhoo](https://github.com/stephaniewhoo) on 2020-10-25 (commit[`e815051`](https://github.com/castorini/pygaggle/commit/e815051f2cee1af98b370ee030b66c07a8a287f3)) (Tesla V100 on Compute Canada)
+ Results replicated by [@Dahlia-Chehata](https://github.com/Dahlia-Chehata) on 2021-01-20 (commit[`623285a`](https://github.com/castorini/pygaggle/commit/623285ae5092a9b27bc15a4a3b72bbe25910db49)) (Tesla K80 on Colab)
+ Results replicated by [@KaiSun314](https://github.com/KaiSun314) on 2021-01-27 (commit[`46bb71d`](https://github.com/castorini/pygaggle/commit/46bb71d39bfaa636ba44624434b83c0dc42654e8)) (Nvidia GeForce GTX 1060)