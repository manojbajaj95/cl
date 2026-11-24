# GPT-2 forward-only trace compile probe

One GPT-2 small checkpoint, one layer, three seeded reassignments of 20 real city tokens to nonce names, including a new pairing and train/held-out template split each seed. The trace query is fixed; the other ten templates split five/five. No gradients, answer tokens in evaluation prompts, or trained external editor. A four-fact disjoint pilot picks the zero-indexed layer from 3/5/7/9 by mean isolated patch gain. The payload is the block-output residual difference at the final position, between a query with its fact stated in a prefix and the bare query.

- GPT-2's MLP output matrix stores the transpose of the usual linear-map convention. Let k be the input to its output projection, v be the trace, and C the uncentered key second moment on 2,048 WikiText-2 training positions, stabilized by 0.1 × mean diagonal. The single-key and mean-key arms use C⁻¹k / (kᵀC⁻¹k). Least squares minimizes departure from unit firing on the trace key and five train paraphrase keys, in the whitened coordinates from C. Its analytical dual is C⁻¹Kᵀ(KC⁻¹Kᵀ)⁺1, where K has keys as rows. All use the same payload.
- A direct patch adds the trace only at each queried final position, even on wrong subjects and WikiText; for two facts it adds both traces unconditionally. It is a value-sufficiency control, not a selective two-fact oracle. Random writes match each single-key update's Frobenius norm with independent random key and value directions. The base has no intervention.
- Measure target probability and top-1 on the trace query, train and held-out templates. Add two independently compiled updates, then query both facts separately with both writes installed; also query each fact with both names in the same context. Neither measures a task requiring a computation over both learned values. Wrong-subject leakage is the change in probability for the edited city and full-distribution KL on the unedited partner's trace template. General retention is KL(base ‖ edit) and greedy next-token flip rate on the final 25 positions of each of eight nonoverlapping 32-token WikiText-2 test windows, after a solo edit.
- Mean and 95% percentile intervals resample the ten pairs independently within each of the three fixed seeds (4,000 draws). This preserves both directions of an interference pair and the seed balance, not independence of templates, vocabulary, or WikiText positions across runs. These are descriptive conditional intervals, not general-population confidence bounds.

## Reproduce on CPU

From this directory, with Python 3.10:

    python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu 'torch==2.5.1+cpu' transformers==4.48.3 pyarrow==19.0.1 numpy==2.2.6
    curl -fL https://huggingface.co/datasets/Salesforce/wikitext/resolve/b08601e04326c79dfdd32d625aee71d232d685c3/wikitext-2-raw-v1/train-00000-of-00001.parquet -o /path/to/wiki-train.parquet
    curl -fL https://huggingface.co/datasets/Salesforce/wikitext/resolve/b08601e04326c79dfdd32d625aee71d232d685c3/wikitext-2-raw-v1/test-00000-of-00001.parquet -o /path/to/wiki-test.parquet
    python probe.py --model /path/to/gpt2 --wiki-train /path/to/wiki-train.parquet --wiki-test /path/to/wiki-test.parquet --output results.json

The local GPT-2 snapshot is [openai-community/gpt2 at 607a30d](https://huggingface.co/openai-community/gpt2/tree/607a30d783dfa663caf39e06633721c8d4cfcd7e); download config.json, model.safetensors, merges.txt, vocab.json, tokenizer.json and tokenizer_config.json to the model directory. Use a fresh environment to avoid unrelated packages affecting the Transformers import. The default uses four Torch threads.
