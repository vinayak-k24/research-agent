# Challenge 3: Quality & Safety Batch Evaluation (`4_evaluate/`)

Welcome to **Challenge 3** of **ManuscriptShield AI**. This module configures and executes cloud-based batch LLM-as-judge evaluations using the Microsoft Foundry SDK (`openai_client.evals.create`).

---

## 🔑 Key Methodologies

1. **Agent Targeting**: Targets deployed or in-code agents using `azure_ai_target_completions` and `azure_ai_agent`.
2. **Built-In Evaluators**: Evaluates task adherence (`builtin.task_adherence`), coherence (`builtin.coherence`), fluency (`builtin.fluency`), and safety (`builtin.violence`).
3. **Cloud Batch Execution**: Executes evaluation jobs asynchronously in Microsoft Foundry without local compute bottlenecks.
4. **Structured Output**: Saves row-level scores, pass/fail indicators, and reasoning explanations to `evaluation_results.json`.

---

## 📂 Files Included

* **`test_manuscripts.jsonl`**: JSON Lines benchmark dataset with test queries (fake DOIs, statistical contradictions, missing IRB approval).
* **`eval.yaml`**: Suite configuration specifying datasets, evaluators, and judge models.
* **`evaluate.py`**: Python execution script that creates cloud evaluation jobs and retrieves results.
* **`evaluation_results.json`**: Structured JSON schema output containing evaluation metrics.

---

## 🚀 How to Run

```bash
# Run batch evaluation
python 4_evaluate/evaluate.py
```
```