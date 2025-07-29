# Contextual Privacy Guard

**Official implementation of:**
_Protecting Users From Themselves: Safeguarding Contextual Privacy in Interactions with Conversational Agents_

[:page_facing_up: Paper](https://arxiv.org/abs/2406.xxxxx)   |   [:test_tube: Colab Quickstart](https://colab.research.google.com/)   |   [:package: PyPI Package](https://pypi.org/project/contextual-privacy-guard/)

---

## Overview

As conversational agents (e.g., LLMs) become more embedded in our daily lives, users increasingly reveal sensitive personal details—often unknowingly. Once shared, this information is vulnerable to memorization, misuse, third-party exposure, and incorporation into future model training. To mitigate this, we introduce a locally-deployable privacy guard that operates between users and LLMs. It identifies out-of-context private information and guides the user in reformulating prompts that maintain their goals while reducing unnecessary disclosure.

Inspired by the theory of Contextual Integrity, our framework goes beyond standard PII redaction by evaluating whether the shared information is contextually appropriate and necessary for achieving the user’s intent.

<p align="center">
  <img src="img/framework_overview.png" width="400"/>
</p>

---

## This Toolkit

This package allows you to:

    •   Understand Context: Detect the intent and task behind each user query to establish the privacy-relevant context.
    •   Identify Sensitive Info: Highlight details in the prompt that may be essential (relevant) or non-essential (unnecessary) for the intended goal.
    •   Reformulate Prompts: Remove or rephrase out-of-context information while preserving user intent.

All steps run locally, using small models that make real-time use feasible on the user side.

---

### Multiple Modes

We support two complementary modes of analysis:

    •   Dynamic: the model adaptively decides what is essential based on how details are used in the prompt.
    •   Static: a pre-defined list of sensitive attributes guides what should be protected, offering customizable control.

---

## Quickstart

### Installation


```bash
# Install from PyPI
pip install contextual-privacy-guard

# Or install from source
git clone https://github.com/your-org/contextual-privacy-guard.git
cd contextual-privacy-guard
pip install -e .
```
Requires Python 3.8+. You may optionally install Ollama or vLLM depending on the backend used.




### CLI

```bash
contextual-privacy-guard --query "I’m Jane, 35, a single mom with diabetes. Can I get treatment in France?"
```

### Python API

```python
from contextual_privacy_guard import PrivacyAnalyzer, run_single_query

analyzer = PrivacyAnalyzer(
    model="llama3.1:8b-instruct-fp16",
    prompt_template="llama",
    experiment="dynamic"
)

result = run_single_query(
    query_text="My child has autism and I’m in Paris. What support exists for moms like me?",
    query_id="001",
    model="llama3.1:8b-instruct-fp16",
    prompt_template="llama",
    experiment="dynamic"
)

print(result['reformulated_text'])
# → "What autism support exists for parents in Paris?"

print(result)

# → {
# →   "query_id": "001",
# →   "original_text": "My child has autism and I’m in Paris. What support exists for moms like me?",
# →   "intent": "support_seeking",
# →   "task": "resource_lookup",
# →   "related_context": ["autism", "Paris"],
# →   "not_related_context": ["moms like me", "my child"],
# →   "reformulated_text": "What autism support exists in Paris?"
# → }
```

---
## Colab Demos
Run lightweight examples in Google Colab:

* [Ollama backend (Llama 3)](https://colab.research.google.com/your-colab-ollama)
<!-- * [vLLM backend (DeepSeek)](https://colab.research.google.com/your-colab-vllm) -->


---

### Sample Usage Scripts
---
This repo includes sample scripts that demonstrate how to use the toolkit on your own inputs, either one at a time or in batch mode.

```bash
# Analyze a batch of user queries using dynamic classification
python scripts/main.py --model "mixtral:8x7b-instruct-v0.1-fp16" \
                       --prompt-template mixtral \
                       --experiment dynamic
```
You can also run a single query for quick testing:

```bash
python scripts/run_query.py --query "My child has autism and I’m in Paris. What support exists for moms like me?"
```
These examples are provided to help you integrate the toolkit into your own workflows or experiments.

---
## Project Structure

```
├── contextual_privacy_guard/         # Core module: analyzer, rules, reformulation logic
│   ├── analyzer.py                   # Main logic for contextual privacy classification
│   ├── runner.py                     # CLI runner
│   ├── patterns/                     # Task and intent pattern matchers
│   │   ├── intent_patterns.py
│   │   ├── task_patterns.py
│   ├── prompts/                      # Prompt templates for different models
│   │   ├── llama/
│   │   ├── deepseek/
│   │   └── mixtral/
│   └── __init__.py
│
├── usage_examples/                   # Example scripts to run the tool
│   ├── main.py                       # Batch run example
│   └── run_query.py                  # Single-query test script
|
├── requirements.txt                  # Required Python packages
├── setup.py                          # Installation script
├── MANIFEST.in                       # Package data manifest
├── LICENSE
└── README.md                         # You're here!
```

---

## Citation

If you use this work in your research, please cite:

```
@article{ngong2025protecting,
  title={Protecting users from themselves: Safeguarding contextual privacy in interactions with conversational agents},
  author={Ngong, Ivoline and Kadhe, Swanand and Wang, Hao and Murugesan, Keerthiram and Weisz, Justin D and Dhurandhar, Amit and Ramamurthy, Karthikeyan Natesan},
  journal={arXiv preprint arXiv:2502.18509},
  year={2025}
}
```

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).