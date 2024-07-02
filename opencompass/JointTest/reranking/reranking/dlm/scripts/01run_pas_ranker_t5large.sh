python evaluate_passage_ranker.py --split dev \
                                                --method t5 \
                                                --model castorini/monot5-large-msmarco \
                                                --dataset ../data/msmarco_ans_small \
                                                --model-type t5-large \
                                                --task msmarco \
                                                --index-dir ../indexes/index-msmarco-passage-20191117-0ed488 \
                                                --batch-size 32 \
                                                --output-file runs/run.monot5-large.ans_small.dev.tsv