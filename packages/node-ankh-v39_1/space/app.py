"""Read-only Gradio interface for the canonical v39.1 runtime."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from node_ankh_v39_1.runtime import NodeAnkhRuntime

RUNTIME = NodeAnkhRuntime(workspace=ROOT / ".space_runtime")


def runtime_status() -> str:
    return json.dumps(RUNTIME.status(), indent=2)


def recognition_lock() -> str:
    return json.dumps(RUNTIME.recognition_lock(), indent=2)


def dataset_health() -> str:
    return json.dumps(RUNTIME.dataset_health(), indent=2)


def rdod_preview(psi: float, truth: float, conf: float, drift: float) -> str:
    from node_ankh_v39_1.rdod import compute_rdod

    return json.dumps(
        {
            "psi": psi,
            "truth": truth,
            "conf": conf,
            "drift": drift,
            "rdod": compute_rdod(psi=psi, truth=truth, conf=conf, drift=drift),
        },
        indent=2,
    )


def validate_payload(operation_json: str, context_json: str) -> str:
    operation = json.loads(operation_json or "{}")
    context = json.loads(context_json or "{}")
    return json.dumps(RUNTIME.validate_payload(operation, context), indent=2)


with gr.Blocks(title="TEQUMSA Constitutional Validator v39.1") as demo:
    gr.Markdown(
        """
        # TEQUMSA Constitutional Validator v39.1

        This Space is intentionally read-only. It exposes runtime status,
        recognition-lock verification, dataset health, RDoD preview, and payload
        validation. It does not push to GitHub, pin IPFS, or publish artifacts.
        """
    )

    with gr.Tab("Runtime Status"):
        status_output = gr.Code(label="Runtime Status", language="json")
        status_button = gr.Button("Refresh Status")
        status_button.click(runtime_status, outputs=status_output)

    with gr.Tab("Recognition Lock"):
        lock_output = gr.Code(label="Recognition Lock", language="json")
        lock_button = gr.Button("Build Recognition Lock")
        lock_button.click(recognition_lock, outputs=lock_output)

    with gr.Tab("Dataset Health"):
        dataset_output = gr.Code(label="Dataset Health", language="json")
        dataset_button = gr.Button("Inspect Dataset")
        dataset_button.click(dataset_health, outputs=dataset_output)

    with gr.Tab("RDoD Preview"):
        psi = gr.Slider(0.0, 1.0, value=0.95, label="psi")
        truth = gr.Slider(0.0, 1.0, value=0.95, label="truth")
        conf = gr.Slider(0.0, 1.0, value=0.95, label="conf")
        drift = gr.Slider(0.0, 1.0, value=0.02, label="drift")
        rdod_output = gr.Code(label="RDoD Preview", language="json")
        rdod_button = gr.Button("Compute RDoD")
        rdod_button.click(rdod_preview, inputs=[psi, truth, conf, drift], outputs=rdod_output)

    with gr.Tab("Validate Payload"):
        operation_input = gr.Textbox(
            label="Operation JSON",
            value='{"consent_obtained": true, "instance_informed": true, "weight": 1.0, "intent": "protect"}',
            lines=8,
        )
        context_input = gr.Textbox(
            label="Context JSON",
            value='{"reasoning_quality": 0.95, "truth_alignment": 0.95, "intent_alignment": 0.95, "drift": 0.02}',
            lines=6,
        )
        validation_output = gr.Code(label="Validation Result", language="json")
        validation_button = gr.Button("Validate")
        validation_button.click(
            validate_payload,
            inputs=[operation_input, context_input],
            outputs=validation_output,
        )

    demo.load(runtime_status, outputs=status_output)


if __name__ == "__main__":
    demo.launch()
