import io
import os
from importlib.resources import files
from pathlib import Path

import gradio
import huggingface_hub


def deploy_as_space(
    title: str,
    dataset_id: str | None = None,
):
    if (
        os.getenv("SYSTEM") == "spaces"
    ):  # in case a repo with this function is uploaded to spaces
        return

    trackio_path = files("trackio")

    hf_api = huggingface_hub.HfApi()
    whoami = None
    login = False
    try:
        whoami = hf_api.whoami()
        if whoami["auth"]["accessToken"]["role"] != "write":
            login = True
    except OSError:
        login = True
    if login:
        print("Need 'write' access token to create a Spaces repo.")
        huggingface_hub.login(add_to_git_credential=False)
        whoami = hf_api.whoami()

    space_id = huggingface_hub.create_repo(
        title,
        space_sdk="gradio",
        repo_type="space",
        exist_ok=True,
    ).repo_id
    assert space_id == title  # not sure why these would differ

    with open(Path(trackio_path, "README.md"), "r") as f:
        readme_content = f.read()
        readme_content = readme_content.replace("{GRADIO_VERSION}", gradio.__version__)
        readme_buffer = io.BytesIO(readme_content.encode("utf-8"))
        hf_api.upload_file(
            path_or_fileobj=readme_buffer,
            path_in_repo="README.md",
            repo_id=space_id,
            repo_type="space",
        )

    huggingface_hub.utils.disable_progress_bars()
    hf_api.upload_folder(
        repo_id=space_id,
        repo_type="space",
        folder_path=trackio_path,
        ignore_patterns=["README.md"],
    )

    hf_token = huggingface_hub.utils.get_token()
    if hf_token is not None:
        huggingface_hub.add_space_secret(space_id, "HF_TOKEN", hf_token)
    if dataset_id is not None:
        huggingface_hub.add_space_variable(space_id, "TRACKIO_DATASET_ID", dataset_id)
        # So that the dataset id is available to the sqlite_storage.py file
        # if running locally as well.
        os.environ["TRACKIO_DATASET_ID"] = dataset_id
