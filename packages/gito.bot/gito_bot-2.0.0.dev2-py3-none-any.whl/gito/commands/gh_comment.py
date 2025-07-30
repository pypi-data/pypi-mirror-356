"""
Fix issues from code review report
"""

import logging
import os
import re
from pathlib import Path
from typing import Optional
import zipfile

import requests
import typer
from fastcore.basics import AttrDict
from gito.project_config import ProjectConfig
from gito.utils import extract_gh_owner_repo
from microcore import ui
from ghapi.all import GhApi
import git

from ..bootstrap import app
from ..constants import JSON_REPORT_FILE_NAME
from .fix import fix
from ..utils import is_running_in_github_action


@app.command()
def react_to_comment(
    comment_id: int = typer.Argument(),
    gh_token: str = typer.Option(
        "",
        "--gh-token",
        "--token",
        "-t",
        "--github-token",
        help="GitHub token for authentication",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-d", help="Only print changes without applying them"
    ),
):
    repo = git.Repo(".")  # Current directory
    owner, repo_name = extract_gh_owner_repo(repo)
    logging.info(f"Using repository: {ui.yellow}{owner}/{repo_name}{ui.reset}")
    gh_token = (
        gh_token or os.getenv("GITHUB_TOKEN", None) or os.getenv("GH_TOKEN", None)
    )
    api = GhApi(owner=owner, repo=repo_name, token=gh_token)
    comment = api.issues.get_comment(comment_id=comment_id)
    logging.info(
        f"Comment by {ui.yellow('@' + comment.user.login)}: "
        f"{ui.green(comment.body)}\n"
        f"url: {comment.html_url}"
    )

    cfg = ProjectConfig.load_for_repo(repo)
    if not any(
        trigger.lower() in comment.body.lower() for trigger in cfg.mention_triggers
    ):
        ui.error("No mention trigger found in comment, no reaction added.")
        return
    if not is_running_in_github_action():
        # @todo: need service account to react to comments
        logging.info("Comment contains mention trigger, reacting with 'eyes'.")
        api.reactions.create_for_issue_comment(comment_id=comment_id, content="eyes")

    pr = int(comment.issue_url.split("/")[-1])
    print(f"Processing comment for PR #{pr}...")
    out_folder = "artifact"
    download_latest_code_review_artifact(
        api, pr_number=pr, gh_token=gh_token, out_folder=out_folder
    )

    issue_ids = extract_fix_args(comment.body)
    if not issue_ids:
        ui.error("Can't identify target command in the text.")
        return
    logging.info(f"Extracted issue IDs: {ui.yellow(str(issue_ids))}")

    fix(
        issue_ids[0],  # @todo: support multiple IDs
        report_path=Path(out_folder) / JSON_REPORT_FILE_NAME,
        dry_run=dry_run,
        commit=not dry_run,
        push=not dry_run,
    )
    logging.info("Fix applied successfully.")


def last_code_review_run(api: GhApi, pr_number: int) -> AttrDict | None:
    pr = api.pulls.get(pr_number)
    sha = pr["head"]["sha"]  # noqa
    branch = pr["head"]["ref"]

    runs = api.actions.list_workflow_runs_for_repo(branch=branch)["workflow_runs"]
    # Find the run for this SHA
    run = next(
        (
            r
            for r in runs  # r['head_sha'] == sha and
            if (
                any(
                    marker in r["path"].lower()
                    for marker in ["code-review", "code_review", "cr"]
                )
                or "gito.yml" in r["name"].lower()
            )
            and r["status"] == "completed"
        ),
        None,
    )
    return run


def download_latest_code_review_artifact(
    api: GhApi, pr_number: int, gh_token: str, out_folder: Optional[str] = "artifact"
) -> tuple[str, dict] | None:
    run = last_code_review_run(api, pr_number)
    if not run:
        raise Exception("No workflow run found for this PR/SHA")

    artifacts = api.actions.list_workflow_run_artifacts(run["id"])["artifacts"]
    if not artifacts:
        raise Exception("No artifacts found for this workflow run")

    latest_artifact = artifacts[0]
    url = latest_artifact["archive_download_url"]
    print(f"Artifact: {latest_artifact['name']}, Download URL: {url}")
    headers = {"Authorization": f"token {gh_token}"} if gh_token else {}
    zip_path = "artifact.zip"
    try:
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Unpack to ./artifact
        os.makedirs("artifact", exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("artifact")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

    print("Artifact unpacked to ./artifact")


def extract_fix_args(text: str) -> list[int]:
    pattern1 = r"fix\s+(?:issues?)?(?:\s+)?#?(\d+(?:\s*,\s*#?\d+)*)"
    match = re.search(pattern1, text)
    if match:
        numbers_str = match.group(1)
        numbers = re.findall(r"\d+", numbers_str)
        issue_numbers = [int(num) for num in numbers]
        return issue_numbers
    return []
