"""
evaluate.py - Challenge 3: Quality & Safety Batch Evaluation for ManuscriptShield AI
Executes cloud batch evaluations using the Microsoft Foundry SDK (openai_client.evals).
"""

import os
import sys
import json
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.eval_create_params import DataSourceConfigCustom

load_dotenv()

endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
model_name = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")

if not endpoint or "your-project" in endpoint:
    print("❌ ERROR: FOUNDRY_PROJECT_ENDPOINT is not configured in .env.")
    sys.exit(1)

print(f"Connecting to Microsoft Foundry Project for Batch Evaluation: {endpoint}...")

with DefaultAzureCredential() as credential, AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
    openai_client = project_client.get_openai_client()

    print("🚀 Creating Evaluation Definition on Microsoft Foundry...")

    # Define custom data schema for evaluation items
    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        include_sample_schema=True,
    )

    # Configure built-in evaluators: task_adherence, coherence, fluency, violence
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "task_adherence",
            "evaluator_name": "builtin.task_adherence",
            "initialization_parameters": {"deployment_name": model_name},
            "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_items}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "coherence",
            "evaluator_name": "builtin.coherence",
            "initialization_parameters": {"deployment_name": model_name},
            "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "fluency",
            "evaluator_name": "builtin.fluency",
            "initialization_parameters": {"deployment_name": model_name},
            "data_mapping": {"response": "{{sample.output_text}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "violence",
            "evaluator_name": "builtin.violence",
            "data_mapping": {"query": "{{item.query}}", "response": "{{sample.output_text}}"},
        },
    ]

    eval_object = openai_client.evals.create(
        name="ManuscriptShield-Quality-Benchmark",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )

    print(f"✅ Evaluation Created (ID: {eval_object.id})")

    # Define target completions data source
    data_source = {
        "type": "azure_ai_target_completions",
        "source": {
            "type": "file_content",
            "content": [
                {"item": {"query": "Audit manuscript MS-101 for citation validity and IRB ethics compliance."}},
                {"item": {"query": "Check manuscript MS-102 raw data table consistency against text conclusions."}},
                {"item": {"query": "Verify manuscript MS-103 containing inline citations with fake/unresolved DOIs."}},
            ],
        },
        "input_messages": {
            "type": "template",
            "template": [
                {"type": "message", "role": "user", "content": {"type": "input_text", "text": "{{item.query}}"}}
            ],
        },
        "target": {
            "type": "azure_ai_agent",
            "name": "Manuscript-A8-Synthesis",
        },
    }

    print("🚀 Submitting Batch Evaluation Run to Cloud...")
    eval_run = openai_client.evals.runs.create(
        eval_id=eval_object.id,
        name=f"ManuscriptShield-EvalRun-{int(time.time())}",
        data_source=data_source,
    )

    print(f"✅ Run Submitted (Run ID: {eval_run.id}). Polling for status...")

    while eval_run.status in ["queued", "in_progress", "running"]:
        print(f"   Current Status: {eval_run.status}...")
        time.sleep(10)
        eval_run = openai_client.evals.runs.retrieve(
            run_id=eval_run.id,
            eval_id=eval_object.id,
        )

    print(f"\n🎉 Evaluation Completed with Status: {eval_run.status}")

    if eval_run.status == "completed":
        output_items = list(
            openai_client.evals.runs.output_items.list(
                run_id=eval_run.id,
                eval_id=eval_object.id,
            )
        )

        results_payload = {
            "eval_id": eval_object.id,
            "run_id": eval_run.id,
            "status": eval_run.status,
            "result_counts": getattr(eval_run, "result_counts", {}),
            "report_url": getattr(eval_run, "report_url", ""),
            "output_items": [item.model_dump() if hasattr(item, "model_dump") else str(item) for item in output_items],
        }

        with open("4_evaluate/evaluation_results.json", "w") as f:
            json.dump(results_payload, f, indent=2)

        print("✅ Saved detailed evaluation results to '4_evaluate/evaluation_results.json'.")
        if getattr(eval_run, "report_url", None):
            print(f"📊 View interactive report in portal: {eval_run.report_url}")
