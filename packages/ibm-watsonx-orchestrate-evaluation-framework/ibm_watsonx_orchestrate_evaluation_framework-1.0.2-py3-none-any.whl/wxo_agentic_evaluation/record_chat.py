from wxo_agentic_evaluation.type import Message
from wxo_agentic_evaluation.arg_configs import (
    ChatRecordingConfig,
    KeywordsGenerationConfig,
)
from wxo_agentic_evaluation.inference_backend import (
    WXOClient,
    WXOInferenceBackend,
    get_wxo_client,
)
from wxo_agentic_evaluation.data_annotator import DataAnnotator
from wxo_agentic_evaluation.utils.utils import is_saas_url
from wxo_agentic_evaluation.service_instance import tenant_setup

import json
import os
import rich
from datetime import datetime
import time
from typing import List
from jsonargparse import CLI
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def get_all_runs(wxo_client: WXOClient):
    limit = 20  # Maximum allowed limit per request
    offset = 0
    all_runs = []

    if is_saas_url(wxo_client.service_url):
        path = "v1//orchestrate/runs"
    else:
        path = "/orchestrate/runs"

    initial_response = wxo_client.get(
        path, {"limit": limit, "offset": 0}
    ).json()
    total_runs = initial_response["total"]
    all_runs.extend(initial_response["data"])

    while len(all_runs) < total_runs:
        offset += limit
        response = wxo_client.get(
            path, {"limit": limit, "offset": offset}
        ).json()
        all_runs.extend(response["data"])

    # Sort runs by completed_at in descending order (most recent first)
    # Put runs with no completion time at the end
    all_runs.sort(
        key=lambda x: (
            datetime.strptime(x["completed_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if x.get("completed_at")
            else datetime.min
        ),
        reverse=True,
    )

    return all_runs


def pull_messages_from_thread_id(thread_id: str, wxo_client: WXOClient):
    inference_backend = WXOInferenceBackend(wxo_client=wxo_client)
    messages = inference_backend.get_messages(thread_id)
    return messages


def annotate_messages(
    messages: List[Message], keywords_generation_config: KeywordsGenerationConfig
):
    annotator = DataAnnotator(
        messages=messages, keywords_generation_config=keywords_generation_config
    )
    return annotator.generate()


def record_chats(config: ChatRecordingConfig):
    """Record chats in background mode"""
    start_time = datetime.utcnow()
    processed_threads = set()

    rich.print(
        f"[green]INFO:[/green] Starting chat recording at {start_time}. Press Ctrl+C to stop."
    )
    if config.token is None:
        token = tenant_setup(config.service_url, config.tenant_name)
    else:
        token = config.token
    wxo_client = get_wxo_client(config.service_url, token)
    try:
        while True:
            all_runs = get_all_runs(wxo_client)
            seen_threads = set()

            # Process only new runs that started after our recording began
            for run in all_runs:
                thread_id = run.get("thread_id")
                if thread_id in seen_threads:
                    continue
                seen_threads.add(thread_id)
                started_at = run.get("started_at")

                if not thread_id or not started_at:
                    continue

                try:
                    started_time = datetime.strptime(
                        started_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    if started_time > start_time:
                        if thread_id not in processed_threads:
                            os.makedirs(config.output_dir, exist_ok=True)
                            rich.print(
                                f"\n[green]INFO:[/green] New recording started at {started_at}"
                            )
                            rich.print(
                                f"[green]INFO:[/green] Messages saved to: {os.path.join(config.output_dir, f'{thread_id}_messages.json')}"
                            )
                            rich.print(
                                f"[green]INFO:[/green] Annotations saved to: {os.path.join(config.output_dir, f'{thread_id}_annotated_data.json')}"
                            )
                        processed_threads.add(thread_id)

                        try:
                            messages = pull_messages_from_thread_id(
                                thread_id, wxo_client
                            )
                            annotated_data = annotate_messages(
                                messages, config.keywords_generation_config
                            )

                            messages_filename = os.path.join(
                                config.output_dir, f"{thread_id}_messages.json"
                            )
                            annotation_filename = os.path.join(
                                config.output_dir, f"{thread_id}_annotated_data.json"
                            )

                            with open(messages_filename, "w") as f:
                                json.dump(
                                    [msg.model_dump() for msg in messages], f, indent=4
                                )

                            with open(annotation_filename, "w") as f:
                                json.dump(annotated_data, f, indent=4)
                        except Exception as e:
                            rich.print(
                                f"[red]ERROR:[/red] Failed to process thread {thread_id}: {str(e)}"
                            )
                except (ValueError, TypeError) as e:
                    rich.print(
                        f"[yellow]WARNING:[/yellow] Invalid timestamp format for thread {thread_id}: {str(e)}"
                    )

            time.sleep(2)  # Poll every 2 seconds

    except KeyboardInterrupt:
        rich.print("\n[yellow]Recording stopped by user[/yellow]")


if __name__ == "__main__":
    record_chats(CLI(ChatRecordingConfig, as_positional=False))
