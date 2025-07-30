# Copyright (c) Sebastian Raschka under Apache License 2.0 (see LICENSE.txt).
# Source for "Build a Large Language Model From Scratch"
#   - https://www.manning.com/books/build-a-large-language-model-from-scratch
# Code: https://github.com/rasbt/LLMs-from-scratch

import torch


def generate_text_simple(model, idx, max_new_tokens, context_size=None, use_cache=True):
    model.eval()

    if context_size is None:
        ctx_len = model.tok_emb.num_embeddings  # max supported length, e.g. 1024
    else:
        ctx_len = context_size
    if use_cache:
        # Init cache with full prompt
        model.reset_kv_cache()
        with torch.no_grad():
            logits = model(idx[:, -ctx_len:], use_cache=use_cache)

        for _ in range(max_new_tokens):
            # Pick the token with the highest log-probability (greedy sampling)
            next_idx = logits[:, -1].argmax(dim=-1, keepdim=True)
            # Append it to the running sequence
            idx = torch.cat([idx, next_idx], dim=1)
            # Feed model only the new token
            with torch.no_grad():
                logits = model(next_idx, use_cache=use_cache)
    else:
        for _ in range(max_new_tokens):
            with torch.no_grad():
                logits = model(idx[:, -ctx_len:], use_cache=False)
            next_idx = logits[:, -1].argmax(dim=-1, keepdim=True)
            idx = torch.cat([idx, next_idx], dim=1)

    return idx
