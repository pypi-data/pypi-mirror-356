# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=invalid-name, unused-argument, too-many-lines, import-outside-toplevel
# pylint: disable=no-else-return, inconsistent-return-statements, no-else-raise
"""
data loader of LLM
"""

import torch
import random


def set_seed(seed):
    import numpy as np

    np.random.seed(seed)
    torch.random.manual_seed(seed)


def get_wikitext2(data_name, nsamples, seed, seqlen, model):
    from datasets import load_dataset
    from transformers import AutoTokenizer

    if data_name == "wikitext":
        traindata = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
        testdata = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    else:
        traindata = load_dataset(data_name, split="train")
        testdata = load_dataset(data_name, split="test")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True, use_fast=False)
    except:
        tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True, use_fast=True)
    trainenc = tokenizer("\n\n".join(traindata["text"]), return_tensors="pt")
    testenc = tokenizer("\n\n".join(testdata["text"]), return_tensors="pt")

    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen - 1)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        attention_mask = torch.ones_like(inp)
        trainloader.append({"input_ids": inp, "attention_mask": attention_mask})
    return trainloader, testenc


def get_ptb(data_name, nsamples, seed, seqlen, model):
    from datasets import load_dataset
    from transformers import AutoTokenizer

    if data_name == "ptb":
        traindata = load_dataset("ptb_text_only", "penn_treebank", split="train")
        testdata = load_dataset("ptb_text_only", "penn_treebank", split="validation")
    else:
        traindata = load_dataset(data_name, split="train")
        testdata = load_dataset(data_name, split="test")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True, use_fast=False)
    except:
        tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True, use_fast=True)
    trainenc = tokenizer("\n\n".join(traindata["sentence"]), return_tensors="pt")
    testenc = tokenizer("\n\n".join(testdata["sentence"]), return_tensors="pt")

    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen - 1)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        attention_mask = torch.ones_like(inp)
        trainloader.append({"input_ids": inp, "attention_mask": attention_mask})
    return trainloader, testenc


def get_c4(data_name, nsamples, seed, seqlen, model):
    from datasets import load_dataset
    from transformers import AutoTokenizer

    if data_name == "c4":
        traindata = load_dataset(
            "allenai/c4",
            "allenai--c4",
            data_files={"train": "en/c4-train.00000-of-01024.json.gz"},
            split="train",
        )
        valdata = load_dataset(
            "allenai/c4",
            "allenai--c4",
            data_files={"validation": "en/c4-validation.00000-of-00008.json.gz"},
            split="validation",
        )
    else:
        traindata = load_dataset(
            data_name,
            data_files={"train": "en/c4-train.00000-of-01024.json.gz"},
            split="train",
        )
        valdata = load_dataset(
            data_name,
            data_files={"validation": "en/c4-validation.00000-of-00008.json.gz"},
            split="validation",
        )
    tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True, use_fast=False)

    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        while True:
            i = random.randint(0, len(traindata) - 1)
            trainenc = tokenizer(traindata[i]["text"], return_tensors="pt")
            if trainenc.input_ids.shape[1] >= seqlen:
                break
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen - 1)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        attention_mask = torch.ones_like(inp)
        trainloader.append({"input_ids": inp, "attention_mask": attention_mask})

    random.seed(0)
    valenc = []
    for _ in range(256):
        while True:
            i = random.randint(0, len(valdata) - 1)
            tmp = tokenizer(valdata[i]["text"], return_tensors="pt")
            if tmp.input_ids.shape[1] >= seqlen:
                break
        i = random.randint(0, tmp.input_ids.shape[1] - seqlen - 1)
        j = i + seqlen
        valenc.append(tmp.input_ids[:, i:j])
    valenc = torch.hstack(valenc)

    class TokenizerWrapper:
        def __init__(self, input_ids):
            self.input_ids = input_ids

    valenc = TokenizerWrapper(valenc)

    return trainloader, valenc


def get_ptb_new(data_name, nsamples, seed, seqlen, model):
    from datasets import load_dataset
    from transformers import AutoTokenizer

    if data_name == "ptb-new":
        traindata = load_dataset("ptb_text_only", "penn_treebank", split="train")
        testdata = load_dataset("ptb_text_only", "penn_treebank", split="test")
    else:
        traindata = load_dataset(data_name, split="train")
        testdata = load_dataset(data_name, split="test")

    tokenizer = AutoTokenizer.from_pretrained(model, use_fast=False)
    trainenc = tokenizer(" ".join(traindata["sentence"]), return_tensors="pt")
    testenc = tokenizer(" ".join(testdata["sentence"]), return_tensors="pt")

    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen - 1)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        attention_mask = torch.ones_like(inp)
        trainloader.append({"input_ids": inp, "attention_mask": attention_mask})
    return trainloader, testenc


def get_c4_new(data_name, nsamples, seed, seqlen, model):
    from datasets import load_dataset
    from transformers import AutoTokenizer

    if data_name == "c4-new":
        traindata = load_dataset(
            "allenai/c4",
            "allenai--c4",
            data_files={"train": "en/c4-train.00000-of-01024.json.gz"},
            split="train",
        )
        valdata = load_dataset(
            "allenai/c4",
            "allenai--c4",
            data_files={"validation": "en/c4-validation.00000-of-00008.json.gz"},
            split="validation",
        )
    else:
        traindata = load_dataset(
            data_name,
            data_files={"train": "en/c4-train.00000-of-01024.json.gz"},
            split="train",
        )
        valdata = load_dataset(
            data_name,
            data_files={"validation": "en/c4-validation.00000-of-00008.json.gz"},
            split="validation",
        )
    tokenizer = AutoTokenizer.from_pretrained(model, use_fast=False)

    random.seed(seed)
    trainloader = []
    for _ in range(nsamples):
        while True:
            i = random.randint(0, len(traindata) - 1)
            trainenc = tokenizer(traindata[i]["text"], return_tensors="pt")
            if trainenc.input_ids.shape[1] >= seqlen:
                break
        i = random.randint(0, trainenc.input_ids.shape[1] - seqlen - 1)
        j = i + seqlen
        inp = trainenc.input_ids[:, i:j]
        attention_mask = torch.ones_like(inp)
        trainloader.append({"input_ids": inp, "attention_mask": attention_mask})

    valenc = tokenizer(" ".join(valdata[:1100]["text"]), return_tensors="pt")
    valenc = valenc.input_ids[:, : (256 * seqlen)]

    class TokenizerWrapper:
        def __init__(self, input_ids):
            self.input_ids = input_ids

    valenc = TokenizerWrapper(valenc)

    return trainloader, valenc


def get_loaders(name, nsamples=128, seed=0, seqlen=2048, model=""):
    if "wikitext2" in name:
        return get_wikitext2(nsamples, seed, seqlen, model)
    if "ptb" in name:
        if "new" in name:
            return get_ptb_new(nsamples, seed, seqlen, model)
        return get_ptb(nsamples, seed, seqlen, model)
    if "c4" in name:
        if "new" in name:
            return get_c4_new(nsamples, seed, seqlen, model)
        return get_c4(nsamples, seed, seqlen, model)


if __name__ == "__main__":
    get_loaders("wikitext2")
