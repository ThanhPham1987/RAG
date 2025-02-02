from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_evaluator import AccEvaluator
from opencompass.datasets import openbookqaDataset
from opencompass.utils.text_postprocessors import first_option_postprocess
from opencompass.datasets import omniDataset

_input_columns = [
    ["question_stem", "A", "B", "C", "D"],
]
_template = [
    dict(
        round=[dict(role="HUMAN", prompt="{classification_query}")],
    )
]


obqa_reader_cfg = dict(input_columns=["classification_query", "query"], output_column="answer")
obqa_infer_cfg = dict(
    prompt_template=dict(type=PromptTemplate, template=_template[0]),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)
obqa_eval_cfg = dict(
    evaluator=dict(type=AccEvaluator),
    pred_role="BOT",
    pred_postprocessor=dict(type=first_option_postprocess, options="ABCD"),
)


obqa_datasets = [
    dict(
        abbr="openbookqa",
        type=omniDataset,
        path="/data/zfr/finalTest/opencompass/generate_docs/true_hh_results/",
        name="obqa",
    )
]
obqa_datasets[0]["reader_cfg"] = obqa_reader_cfg
obqa_datasets[0]["infer_cfg"] = obqa_infer_cfg
obqa_datasets[0]["eval_cfg"] = obqa_eval_cfg
