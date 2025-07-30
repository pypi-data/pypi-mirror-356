import hashlib
import logging
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import git.cmd
from git import Repo

# Create a module-level logger
logger = logging.getLogger(__name__)


def get_changed_files(repo_path: Path, revision: str) -> list[Path]:
    """Get list of files that differ between current HEAD and another revision.

    Args:
        repo_path: Path to the repository
        revision: The revision to compare against (e.g. 'master', 'origin/master', a SHA)

    Returns:
        List of Paths (relative to repo root) of files that differ
    """
    repo = Repo(repo_path)

    # Make sure we have the latest version if it's a remote branch
    if revision.startswith("origin/"):
        branch = revision[len("origin/") :]
        repo.git.fetch("origin", branch)

    # Get the diff between HEAD and revision
    diff = repo.git.diff("--name-only", revision, "HEAD").splitlines()

    # Convert to Path objects
    return [Path(f) for f in diff]


def get_merge_base(repo_path: Path, revision: str) -> str:
    """Get the merge base (most recent common ancestor) between HEAD and another revision.

    Args:
        repo_path: Path to the repository
        revision: The revision to find common ancestor with

    Returns:
        The SHA of the merge base commit
    """
    repo = Repo(repo_path)
    return repo.git.merge_base("HEAD", revision).strip()


def get_repo_metadata(repo_path: Path) -> Dict:
    """Get essential metadata about the repository state for reproducibility.

    Args:
        repo_path: Path to the local repository

    Returns:
        Dict containing:
            - commit_time: ISO formatted UTC timestamp of when the commit was made
            - remote_url: URL of the origin remote
            - sha: full commit hash
            - branch: current branch name or HEAD if detached
    """
    repo = Repo(repo_path)
    commit = repo.head.commit

    # Get remote URL
    remote_url = repo.remotes.origin.url
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    # Get current branch or HEAD if detached
    try:
        current_branch = repo.active_branch.name
    except TypeError:  # HEAD is detached
        current_branch = "HEAD"

    return {
        "commit_time": commit.committed_datetime.isoformat(),
        "remote_url": remote_url,
        "sha": commit.hexsha,
        "branch": current_branch,
    }


def get_git_blame_info(repo_path: Path, file_path: Path, line_number: int) -> dict:
    """Get git blame information for a specific line."""
    repo = Repo(repo_path)
    blame = repo.blame("HEAD", str(file_path), L=f"{line_number},{line_number}")[0]
    commit = blame[0]

    # Hash author email
    normalized_email = commit.author.email.lower().strip()
    author_email_hash = hashlib.sha256(normalized_email.encode()).hexdigest()[:12]

    return {
        "commit": commit.hexsha,
        "author_email_hash": author_email_hash,
        "date": commit.authored_datetime.isoformat(),
    }


def prepare_repository(
    remote_url: str,
    branch: str,
    head_sha: Optional[str],
    lean_data: Path,
) -> Path:
    """Prepare a repository for analysis by cloning or updating it and checking out a specific commit.

    Args:
        remote_url: Git remote URL (HTTPS or SSH)
        branch: Branch name
        head_sha: Commit SHA to checkout (if None, will use HEAD of branch)
        lean_data: Base directory for checkouts

    Returns:
        Path to checked out repository

    Raises:
        RuntimeError: If cloning or checking out fails
    """
    # Create a directory name from the remote URL
    repo_name = remote_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    checkout_path = lean_data / repo_name

    # If the repository hasn't already been cloned, clone it
    if not checkout_path.exists():
        try:
            logger.info(f"Cloning {remote_url} branch {branch}...")
            repo = Repo.clone_from(remote_url, checkout_path)

        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            raise RuntimeError(f"Error cloning repository: {e}")
    else:  # Repository already exists, open it and fetch latest changes
        try:
            logger.info(
                f"Repository already exists at {checkout_path}, fetching latest changes..."
            )
            repo = Repo(checkout_path)
            repo.git.fetch("--all")
        except Exception as e:
            logger.error(f"Error fetching latest changes: {e}")
            raise RuntimeError(f"Error fetching latest changes: {e}")

    # Checkout specific commit on head_sha or branch
    try:
        logger.info(f"Checking out {head_sha}...")
        if head_sha:
            repo.git.checkout(head_sha)
        elif branch:
            repo.git.switch(branch)
        return checkout_path
    except Exception as e:
        logger.error(f"Error checking out commit {head_sha}: {e}")
        raise RuntimeError(f"Error checking out commit {head_sha}: {e}")


def get_default_branch(repo_path: Path) -> str:
    """Get the default branch of the repository."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def remote_heads(remote_url: str) -> list[dict]:
    """Get all branch heads from a remote repository.

    Args:
        remote_url: Git remote URL (HTTPS or SSH)

    Returns:
        List of dicts, each containing:
            - branch: name of the branch
            - sha: SHA of the HEAD commit
    """
    # Use git.cmd.Git for running git commands directly
    logger.debug(f"Getting remote heads for {remote_url}")
    git_cmd = git.cmd.Git()
    logger.debug(f"Running git command: git ls-remote --heads {remote_url}")
    output = git_cmd.ls_remote("--heads", remote_url)

    # Parse the output into a list of dicts
    heads = []
    for line in output.splitlines():
        if not line.strip():
            continue

        # Each line is of format: "<sha>\trefs/heads/<branch>"
        sha, ref = line.split("\t")
        branch = ref.replace("refs/heads/", "")

        heads.append({"branch": branch, "sha": sha})
    if len(heads) == 0:
        logger.warning(f"No branches found for {remote_url}")
    else:
        logger.debug(f"Found {len(heads)} branches in {remote_url}")
    return heads


def remote_heads_hash(remote_url: str) -> str | None:
    """Get a hash of the (sorted) set of unique branch heads in a remote repository.

    Args:
        remote_url: Git remote URL (HTTPS or SSH)

    Returns:
        First 12 characters of SHA-256 hash of sorted set of unique head SHAs
    """
    heads = remote_heads(remote_url)
    if not heads:
        return None

    # Extract unique SHAs and sort them
    shas = sorted(set(head["sha"] for head in heads))
    # Join them with a delimiter and hash
    combined = "_".join(shas)
    return hashlib.sha256(combined.encode()).hexdigest()[:12]


def leaf_commits(remote_url: str) -> list[dict]:
    """Get all branch heads with commit dates from a remote repository.

    Args:
        remote_url: Git remote URL (HTTPS or SSH)

    Returns:
        List of dicts, each containing:
            - branch: name of the branch
            - sha: SHA of the HEAD commit
            - date: ISO formatted date of the commit
    """
    try:
        logger.info(f"Getting leaf commits for {remote_url}")

        # Create a temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone the repository with all branches but minimal depth
            logger.debug(f"Cloning {remote_url} with depth=1 and all branches")
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--no-single-branch",
                    remote_url,
                    temp_dir,
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            # Get information about all remote branches
            logger.debug("Getting branch information")
            result = subprocess.run(
                [
                    "git",
                    "for-each-ref",
                    "--format=%(refname) %(objectname) %(creatordate:iso)",
                    "refs/remotes/origin",
                ],
                cwd=temp_dir,
                check=True,
                capture_output=True,
                text=True,
            )
            logger.debug(f"Result of branch information: {result}")

            # Parse the output into a list of dicts
            commits = []
            for line in result.stdout.splitlines():
                logger.debug(f"Processing git ouptut line: {line}")
                if not line.strip() or line.startswith(
                    "refs/remotes/origin/HEAD"
                ):  # Skip empty lines and HEAD pointer
                    continue
                # Format: "refs/remotes/origin/branch sha date"
                parts = line.split()
                branch = parts[0].replace("refs/remotes/origin/", "")
                sha = parts[1]
                date_str = " ".join(parts[2:])
                # Process date string
                try:
                    date = datetime.fromisoformat(date_str)
                    date = date.astimezone(timezone.utc)
                    date_iso = date.isoformat()
                except ValueError:
                    logger.warning(f"Failed to parse date: {date_str}")
                    continue
                logger.debug(f"Parsed branch: {branch}, sha: {sha}, date: {date_iso}")
                commits.append({"branch": branch, "sha": sha, "date": date_iso})

            if len(commits) == 0:
                logger.warning(f"No branches found for {remote_url}")
            else:
                logger.info(
                    f"Found {len(commits)} branches with commit dates in {remote_url}"
                )
            return commits

    except Exception as e:
        logger.error(f"Error getting leaf commits for {remote_url}: {e}")
        return []
