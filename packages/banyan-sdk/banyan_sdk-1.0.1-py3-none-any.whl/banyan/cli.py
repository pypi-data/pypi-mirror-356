"""
Banyan CLI

A command-line interface for managing your Banyan prompt versions.
"""

import typer
import sys
import os
import json
import getpass
import hashlib
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.syntax import Syntax
import logging

from .core import BanyanAPIClient, APIResponse
from .cli_utils import (
    BanyanProjectManager, 
    BanyanConfig, 
    PromptFile, 
    MergeState,
    validate_api_key,
    validate_prompt_name,
    validate_project_id,
)

# Initialize Typer app
app = typer.Typer(
    name="banyan",
    help="Banyan CLI - prompt management for your LLM applications",
    no_args_is_help=True,
    add_completion=False
)

# Rich console for pretty output
console = Console()

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def get_api_client(config: BanyanConfig) -> Optional[BanyanAPIClient]:
    """Get authenticated API client from config"""
    if not config.api_key:
        console.print("fatal: No API key configured. Run 'banyan login' first.")
        return None
    
    return BanyanAPIClient(
        api_key=config.api_key,
        base_url=config.base_url,
        project_id=config.project_id
    )

def error_exit(message: str, code: int = 1):
    """Print error message and exit"""
    console.print(f"fatal: {message}")
    raise typer.Exit(code)

def warning(message: str):
    """Print warning message"""
    console.print(f"warning: {message}")

def success(message: str):
    """Print success message"""
    console.print(f"✓ {message}")

@app.command()
def init(
    project_id: Optional[str] = typer.Option(None, "--project", "-p", help="Project ID"),
    base_url: Optional[str] = typer.Option(None, "--url", help="Custom Banyan server URL"),
    branch: str = typer.Option("main", "--branch", "-b", help="Default branch name")
):
    """Initialize a new Banyan project in the current directory."""
    
    if not project_id:
        project_id = Prompt.ask("Project ID")

    if not validate_project_id(project_id):
        error_exit("Invalid project ID. Provide a valid project ID")

    project_manager = BanyanProjectManager()
    
    # Check if already initialized
    if project_manager.is_banyan_project():
        if not Confirm.ask("Reinitialize existing Banyan project?"):
            return
    
    # Initialize project
    success_init = project_manager.init_project(
        project_id=project_id,
        base_url=base_url,
        branch=branch
    )
    
    if not success_init:
        error_exit("Failed to initialize project")

    
    success("Initialized Banyan project")
    console.print("Created .banyan directory structure")
    console.print("\nNext steps:")
    console.print("  banyan login        # Authenticate with API key")
    console.print("  banyan add .        # Stage your prompts")
    console.print("  banyan commit       # Create first version")
    console.print("  banyan push         # Push to Banyan")

@app.command()
def login(
    api_key: Optional[str] = typer.Option(None, "--api-key", help="API key"),
    global_config: bool = typer.Option(False, "--global", help="Save to global config")
):
    """Authenticate with Banyan using your API key."""
    
    project_manager = BanyanProjectManager()
    
    # Get API key from user if not provided
    if not api_key:
        api_key = getpass.getpass("API key: ")
    
    # Validate API key format
    if not validate_api_key(api_key):
        error_exit("Invalid API key format. Keys should start with 'psk_'")
    
    # Test API key
    client = BanyanAPIClient(api_key=api_key)
    response = client.validate_api_key()
    
    if not response.success:
        error_exit(f"Authentication failed: {response.error}")
    
    # Fetch author information
    author_info = project_manager.get_author_info_from_database(client)
    
    # Save configuration
    if global_config:
        global_config_obj = project_manager.load_global_config()
        global_config_obj.api_key = api_key
        if author_info.get('author_name'):
            global_config_obj.author_name = author_info['author_name']
        if author_info.get('author_email'):
            global_config_obj.author_email = author_info['author_email']
        project_manager.save_global_config(global_config_obj)
        success("Authentication saved globally")
    else:
        if not project_manager.is_banyan_project():
            error_exit("Not in a Banyan project. Use --global or run 'banyan init' first")
        
        config = project_manager.load_config()
        config.api_key = api_key
        if author_info.get('author_name'):
            config.author_name = author_info['author_name']
        if author_info.get('author_email'):
            config.author_email = author_info['author_email']
        project_manager.save_config(config)
        success("Authentication saved to project")
        
        if author_info.get('author_name'):
            console.print(f"Logged in as {author_info['author_name']}")

@app.command()
def push(
    force: bool = typer.Option(False, "--force", "-f", help="Force push")
):
    """Push local prompt versions to Banyan."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Load configuration
    config = project_manager.load_config()
    client = get_api_client(config)
    if not client:
        raise typer.Exit(1)
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        error_exit("No active prompt. Use 'banyan prompt <name>' to set one")
    
    # Check for conflicts first
    if project_manager.has_prompt_conflicts(state.prompt_name, state.branch_name):
        error_exit("You have unresolved merge conflicts. Please resolve them before pushing.")
    
    # Validate push preconditions
    if not force:
        validation = project_manager.validate_push_preconditions(client, state.prompt_name, state.branch_name)
        if not validation['can_push']:
            if validation['reason'] == 'remote_ahead':
                console.print(f"To {config.base_url}")
                console.print(f" ! [rejected]        {state.branch_name} -> {state.branch_name} (pull first)")
                console.print("error: failed to push some refs to remote")
                console.print("hint: Updates were rejected because the remote contains work that you do")
                console.print("hint: not have locally. This is usually caused by another repository pushing")
                console.print("hint: to the same ref. You may want to first integrate the remote changes")
                console.print("hint: (e.g., 'banyan pull ...') before pushing again.")
                console.print("hint: See the 'Note about fast-forwards' in 'banyan push --help' for details.")
                return
            elif validation['reason'] == 'uncommitted_changes':
                error_exit("You have uncommitted changes. Please commit them before pushing.")
            elif validation['reason'] == 'nothing_to_push':
                console.print("Everything up-to-date")
                return
            else:
                error_exit(validation['message'])
    
    # Load unpushed versions
    unpushed_versions = project_manager.get_unpushed_prompt_versions(state.prompt_name, state.branch_name)
    
    if not unpushed_versions:
        console.print("Everything up-to-date")
        return
    
    remote_prompts = {}
    try:
        remote_response = client.list_prompts(project_id=config.project_id)
        if remote_response.success:
            for prompt in remote_response.data.get('prompts', []):
                remote_prompts[prompt.get('name')] = prompt
    except Exception as e:
        warning(f"Could not check remote prompts: {e}")
    
    success_count = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(f"Pushing to origin...", total=len(unpushed_versions))
    
    for version in unpushed_versions:
        progress.update(task, description=f"Pushing {version.name} v{version.version}")
        
        try:
            # Check if prompt exists remotely
            if version.name not in remote_prompts:
                # Load prompt metadata (including description)
                metadata = project_manager.load_prompt_metadata(version.name)
                description = metadata.get("description", "")
                
                create_response = client.create_prompt(
                    name=version.name,
                    content=version.content,
                    branch=version.branch,
                    metadata={"description": description} if description else None,
                    project_id=config.project_id
                )
                
                if not create_response.success:
                    console.print(f"error: Failed to create {version.name}: {create_response.error}")
                    continue
                    
                remote_prompts[version.name] = {'name': version.name}
            
            # Create the version with author info
            author_name = version.metadata.get('author_name', config.author_name or 'Unknown')
            author_email = version.metadata.get('author_email', config.author_email or '')
            
            version_metadata = {
                'author_name': author_name,
                'author_email': author_email,
                'timestamp': version.metadata.get('timestamp', ''),
                'created_by': 'banyan-cli'
            }
            
            response = client.create_prompt_version(
                name=version.name,
                content=version.content,
                version=version.version,
                change_message=version.message,
                branch=version.branch,
                project_id=config.project_id,
                metadata=version_metadata
            )
            
            if response.success:
                version.pushed = True
                success_count += 1
            else:
                console.print(f"error: Failed to push {version.name}: {response.error}")
                
        except Exception as e:
            console.print(f"error: Failed to push {version.name}: {e}")
        
        progress.advance(task)
    
    # Mark successfully pushed versions
    if success_count > 0:
        pushed_hashes = [v.hash for v in unpushed_versions if v.pushed]
        project_manager.mark_prompt_versions_as_pushed(state.prompt_name, state.branch_name, pushed_hashes)
        
        if success_count == len(unpushed_versions):
            console.print(f"Pushed {success_count} version(s) to origin")
        else:
            console.print(f"Pushed {success_count}/{len(unpushed_versions)} version(s)")
    else:
        error_exit("Failed to push any versions")

@app.command()
def pull(
    force: bool = typer.Option(False, "--force", "-f", help="Force pull (overwrite local changes)"),
    prompt_name: Optional[str] = typer.Option(None, "--prompt", "-p", help="Pull specific prompt"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Pull prompts from Banyan to local directory."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Load configuration
    config = project_manager.load_config()
    client = get_api_client(config)
    if not client:
        raise typer.Exit(1)
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    
    # If pulling a specific prompt, handle with conflict detection
    if prompt_name:
        if not state or state.prompt_name != prompt_name:
            # Set the prompt as active for pull operation
            if project_manager.prompt_exists(prompt_name):
                project_manager.set_active_prompt(prompt_name, "main")
                state = project_manager.get_current_prompt_state()
            else:
                # Prompt doesn't exist locally, we'll create it
                pass
        
        if state:
            # Use Git-like pull with conflict handling for current prompt
            result = project_manager.handle_pull_with_conflicts(client, prompt_name, state.branch_name, force)
            
            if result['success']:
                console.print(result['message'])
                if result['action'] == 'merged':
                    console.print("Fast-forward")
                elif result['action'] == 'overwritten':
                    console.print("(forced update)")
            else:
                if result.get('action') == 'conflict_created':
                    console.print(f"Auto-merging {prompt_name}")
                    console.print(f"CONFLICT (content): Merge conflict in {result['conflict_file']}")
                    console.print("Automatic merge failed; fix conflicts and then commit the result.")
                    error_exit("")
                else:
                    error_exit(result['message'])
            return
    
    # Handle bulk pull (existing logic for backward compatibility)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Fetching from origin...", total=None)
        response = client.list_prompts(project_id=config.project_id)
    
    if not response.success:
        error_exit(f"Failed to fetch prompts: {response.error}")
    
    remote_prompts = response.data.get('prompts', [])
    
    if not remote_prompts:
        console.print("No prompts found in remote project")
        return
    
    # Get unique prompt names
    unique_prompts = {}
    for prompt in remote_prompts:
        name = prompt.get('name')
        if name and name not in unique_prompts:
            unique_prompts[name] = prompt
    
    if verbose:
        console.print(f"Found {len(unique_prompts)} prompt(s)")
    
    # Confirm before pulling if not forced
    if not force and len(unique_prompts) > 1:
        if not Confirm.ask(f"Pull {len(unique_prompts)} prompts?"):
            console.print("Aborted")
            return
    
    success_count = 0
    conflict_count = 0
    total_branches_synced = 0
    
    for i, (prompt_name_item, prompt_data) in enumerate(unique_prompts.items(), 1):
        try:
            if verbose:
                console.print(f"[{i}/{len(unique_prompts)}] Syncing '{prompt_name_item}'")
            
            # Use conflict-aware pull for each prompt
            current_branch = "main"  # Default branch
            if state and state.prompt_name == prompt_name_item:
                current_branch = state.branch_name
            
            result = project_manager.handle_pull_with_conflicts(client, prompt_name_item, current_branch, force)
            
            if result['success']:
                success_count += 1
                if verbose:
                    console.print(f"✓ {result['message']}")
                
                # Set as active prompt if this is the only/first prompt
                if len(unique_prompts) == 1 or not project_manager.get_current_prompt_state():
                    project_manager.set_active_prompt(prompt_name_item, current_branch)
                
                # Sync all branches for this prompt
                branch_sync_result = project_manager.sync_remote_branches_for_prompt(
                    client, prompt_name_item, force=force
                )
                
                branches_synced = branch_sync_result['branches_synced']
                total_branches_synced += branches_synced
                
            else:
                if result.get('action') == 'conflict_created':
                    conflict_count += 1
                    console.print(f"CONFLICT: {result['message']}")
                else:
                    console.print(f"error: {result['message']}")
            
        except Exception as e:
            console.print(f"error: Failed to sync '{prompt_name_item}': {e}")
            if verbose:
                import traceback
                console.print(traceback.format_exc())
    
    # Summary
    if success_count > 0:
        if success_count == 1 and conflict_count == 0:
            console.print(f"Synced 1 prompt")
        else:
            console.print(f"Synced {success_count} prompts, {total_branches_synced} branches")
        
        # Show current context
        current_state = project_manager.get_current_prompt_state()
        if current_state:
            console.print(f"Active: {current_state.context}")
    
    if conflict_count > 0:
        console.print(f"\n{conflict_count} file(s) have merge conflicts.")
        console.print("Resolve conflicts and commit the result.")
    elif success_count == 0:
        console.print("No changes")

@app.command()
def status():
    """Show the working directory status."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        console.print("No active prompt")
        
        # Show available prompts
        prompts = project_manager.list_prompts()
        if prompts:
            console.print("Available prompts:")
            for prompt in prompts:
                console.print(f"  {prompt}")
        else:
            console.print("No prompts found. Create one with 'banyan prompt --create <name>'")
        return
    
    console.print(f"On prompt {state.prompt_name}")
    console.print(f"On branch {state.branch_name}")
    
    # Check for ongoing merge and load conflicts (always needed for status logic)
    merge_state = project_manager.load_merge_state(state.prompt_name, state.branch_name)
    conflicts = project_manager.load_prompt_conflicts(state.prompt_name, state.branch_name)
    
    if merge_state:
        console.print(f"\nYou are currently merging branch '{merge_state.source_branch}' into '{merge_state.target_branch}'")
        console.print(f"  (started {merge_state.started_at})")
        
        if conflicts:
            console.print("\n[red]All conflicts must be resolved before merge can be completed[/red]")
        else:
            console.print("\n[green]All merge conflicts have been resolved[/green]")
    
    # Ensure index is initialized for this prompt@branch
    project_manager.initialize_prompt_index_if_needed(state.prompt_name, state.branch_name)
    
    # Get staging area
    staging_area = project_manager.load_staging_area(state.prompt_name, state.branch_name)
    
    # Load all local prompts
    local_prompts = project_manager.load_local_prompts()
    
    # Get remote status if possible
    try:
        config = project_manager.load_config()
        if config.api_key:
            client = get_api_client(config)
            if client:
                remote_status = project_manager.get_prompt_working_directory_status(client, state.prompt_name, state.branch_name)
            else:
                remote_status = {}
        else:
            remote_status = {}
    except Exception:
        remote_status = {}
    
    # Categorize files
    staged_files = []
    modified_files = []
    
    # Process staged files
    for staged_file in staging_area:
        if staged_file.name == state.prompt_name:
            staged_files.append(staged_file)
    
    # Find current prompt file
    current_prompt_file = None
    for prompt in local_prompts:
        if prompt.name == state.prompt_name:
            current_prompt_file = prompt
            break
    
    # Check if current prompt is modified
    if current_prompt_file:
        staged_version = None
        for staged_file in staging_area:
            if staged_file.name == state.prompt_name:
                staged_version = staged_file
                break
        
        # During merge, don't show unstaged changes if file has conflicts
        has_conflicts = any(c.name == state.prompt_name for c in conflicts)
        
        if staged_version and not has_conflicts:
            # Check for unstaged changes on top of staged changes (only if no conflicts)
            current_hash = current_prompt_file.content_hash()
            if current_hash != staged_version.hash:
                modified_files.append({'name': state.prompt_name, 'status': 'modified'})
        elif not staged_version and not has_conflicts:
            # Check if it needs to be staged (only if no conflicts and not staged)
            index = project_manager.load_prompt_index(state.prompt_name, state.branch_name)
            if state.prompt_name in index:
                index_entry = index[state.prompt_name]
                if current_prompt_file.content_hash() != index_entry.content_hash:
                    modified_files.append({'name': state.prompt_name, 'status': 'modified'})
    
    # Display conflicts first (highest priority)
    if conflicts:
        console.print("\nYou have unmerged paths:")
        for conflict in conflicts:
            console.print(f"  [red]both modified:[/red] {conflict.name}")
        console.print("\n  (fix conflicts and run 'banyan add <file>...' to mark resolution)")
        console.print("  (use 'banyan merge --abort' to abort the merge)")
    
    # Display staged files
    if staged_files:
        console.print("\nChanges to be committed:")
        for staged_file in staged_files:
            color = "green" if staged_file.operation == "added" else "yellow"
            console.print(f"  [bold {color}]{staged_file.operation}:[/bold {color}] {staged_file.name}")
        
        # If in a merge state, show additional context
        if merge_state and not conflicts:
            console.print("\n  (merge in progress - commit to complete the merge)")
    
    # Display modified files
    if modified_files:
        console.print("\nChanges not staged for commit:")
        for modified_file in modified_files:
            console.print(f"  [red]modified:[/red] {modified_file['name']}")
        console.print(f"\n  (use 'banyan add {state.prompt_name}' to stage)")
    
    # Summary if no changes
    if not conflicts and not staged_files and not modified_files:
        if merge_state:
            console.print("\nMerge completed successfully. No additional changes.")
        else:
            console.print("\nnothing to commit, working tree clean")
    
    # Show other branches if available
    branches = project_manager.list_prompt_branches(state.prompt_name)
    other_branches = [b for b in branches if b != state.branch_name]
    
    if other_branches:
        console.print(f"\nOther branches: {', '.join(other_branches)}")

@app.command()
def add(
    prompt_name: Optional[str] = typer.Argument(None, help="Prompt to stage")
):
    """Stage changes for commit."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        error_exit("No active prompt. Use 'banyan prompt <name>' to set one")
    
    # Determine which prompt to stage
    if prompt_name is None or prompt_name == "." or prompt_name == "":
        target_prompt = state.prompt_name
    else:
        target_prompt = prompt_name.replace('.txt', '').strip()
        if target_prompt != state.prompt_name:
            error_exit(f"Cannot stage '{target_prompt}' - active prompt is '{state.prompt_name}'")
    
    # Check if prompt file exists
    if not project_manager.prompt_exists(target_prompt):
        error_exit(f"Prompt '{target_prompt}' does not exist")
    
    # Check if this file has conflicts that need to be resolved
    conflicts = project_manager.load_prompt_conflicts(state.prompt_name, state.branch_name)
    file_in_conflict = any(c.name == target_prompt for c in conflicts)
    
    if file_in_conflict:
        # Check if conflicts are resolved
        if not project_manager.is_conflict_resolved(target_prompt):
            error_exit(f"'{target_prompt}' still has conflict markers. Please resolve them before staging.")
        
        # Mark conflict as resolved
        project_manager.resolve_prompt_conflict(state.prompt_name, state.branch_name, target_prompt)
        console.print(f"Conflict resolved for '{target_prompt}'")
    
    # Load the prompt content
    prompt_file = None
    local_prompts = project_manager.load_local_prompts()
    for prompt in local_prompts:
        if prompt.name == target_prompt:
            prompt_file = prompt
            break
    
    if not prompt_file:
        error_exit(f"Could not load prompt '{target_prompt}'")
    
    # Check if already staged with same content
    staging_area = project_manager.load_staging_area(state.prompt_name, state.branch_name)
    for staged_file in staging_area:
        if staged_file.name == target_prompt:
            if staged_file.hash == prompt_file.content_hash():
                return  # Already staged, no output (like git)
            break
    
    # Stage the prompt content
    if project_manager.stage_prompt_content(target_prompt, prompt_file.content, "modified"):
        # No output on success (like git add)
        pass
    else:
        error_exit(f"Failed to stage '{target_prompt}'")

@app.command()
def commit(
    message: str = typer.Option(None, "--message", "-m", help="Commit message"),
    all: bool = typer.Option(False, "--all", "-a", help="Stage all changes and commit"),
    amend: bool = typer.Option(False, "--amend", help="Amend previous commit")
):
    """Create a new version from staged changes."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        error_exit("No active prompt. Use 'banyan prompt <name>' to set one")
    
    current_prompt = state.prompt_name
    current_branch = state.branch_name
    
    # Check if we're completing a merge
    merge_state = project_manager.load_merge_state(current_prompt, current_branch)
    if merge_state:
        # Complete the merge
        result = project_manager.complete_merge(current_prompt, current_branch, message)
        if result['success']:
            console.print(result['message'])
        else:
            error_exit(result['error'])
        return
    
    # Auto-stage if -a flag is used
    if all:
        local_prompts = project_manager.load_local_prompts()
        for prompt in local_prompts:
            if prompt.name == current_prompt:
                project_manager.stage_prompt_content(prompt.name, prompt.content, "modified")
                break
    
    # Check for conflicts first
    conflicts = project_manager.load_prompt_conflicts(current_prompt, current_branch)
    if conflicts:
        error_exit("You have unresolved merge conflicts. Please resolve them before committing.")
    
    # Check for staged files
    staging_area = project_manager.load_staging_area(current_prompt, current_branch)
    if not staging_area:
        error_exit("No changes added to commit\n  (use 'banyan add' to stage changes)")
    
    # Get commit message if not provided
    if not message:
        message = Prompt.ask("Commit message")
        if not message.strip():
            error_exit("Aborting commit due to empty commit message")
    
    # Get API client for remote version checking
    config = project_manager.load_config()
    api_client = get_api_client(config)
    
    # Update config with author info
    if api_client:
        project_manager.update_config_with_author_info(api_client)
        config = project_manager.load_config()  # Reload config with updated author info
    
    # Create versions
    new_versions = project_manager.create_prompt_commit(staging_area, message, api_client)
    
    if not new_versions:
        error_exit("Failed to create commit")
    
    # Update index and working directory
    for staged_file in staging_area:
        prompt_file = PromptFile(name=staged_file.name, content=staged_file.content)
        project_manager.update_prompt_index_entry(prompt_file, current_prompt, current_branch)
        project_manager.save_prompt_file(prompt_file)
    
    # Clear staging area
    project_manager.clear_staging_area(current_prompt, current_branch)
    
    # Show commit summary (git-style)
    version = new_versions[0] if new_versions else None
    if version:
        console.print(f"[{current_branch} {version.hash}] {message}")
        console.print(f" 1 file changed")
        
        # Show if this is a merge commit
        if version.is_merge_commit():
            console.print(f" (merge commit with {len(version.merge_parents)} parent(s))")

@app.command()
def branch(
    branch_name: Optional[str] = typer.Argument(None, help="Branch to switch to or create"),
    list_local: bool = typer.Option(False, "--list", "-l", help="List local branches"),
    list_remote: bool = typer.Option(False, "--remote", "-r", help="List remote branches"),
    list_all: bool = typer.Option(False, "--all", "-a", help="List all branches"),
    create: bool = typer.Option(False, "--create", "-b", help="Create new branch and switch to it"),
    create_only: Optional[str] = typer.Option(None, "--create-only", "-c", help="Create new branch without switching"),
    delete: Optional[str] = typer.Option(None, "--delete", "-d", help="Delete branch")
):
    """List, create, switch, or delete branches."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        error_exit("No active prompt. Use 'banyan prompt <name>' to set one")
    
    current_prompt = state.prompt_name
    current_branch = state.branch_name
    
    # Handle branch creation (without switching)
    if create_only:
        if project_manager.prompt_branch_exists(current_prompt, create_only):
            error_exit(f"Branch '{create_only}' already exists")
        
        if project_manager.create_prompt_branch(current_prompt, create_only, current_branch):
            console.print(f"Created branch '{create_only}'")
        else:
            error_exit(f"Failed to create branch '{create_only}'")
        return
    
    # Handle branch deletion
    if delete:
        if delete == current_branch:
            error_exit(f"Cannot delete current branch '{delete}'")
        
        if not project_manager.prompt_branch_exists(current_prompt, delete):
            error_exit(f"Branch '{delete}' does not exist")
        
        if not Confirm.ask(f"Delete branch '{delete}'?"):
            console.print("Aborted")
            return
        
        # Delete branch
        branch_ref_file = project_manager.refs_dir / current_prompt / 'heads' / delete
        try:
            branch_ref_file.unlink()
            branch_content_file = project_manager.banyan_dir / 'branch_content' / current_prompt / f"{delete}.txt"
            if branch_content_file.exists():
                branch_content_file.unlink()
            console.print(f"Deleted branch '{delete}'")
        except Exception as e:
            error_exit(f"Failed to delete branch '{delete}': {e}")
        return
    
    # Handle listing branches (default behavior when no branch name is provided)
    if not branch_name or list_local or list_remote or list_all:
        if list_all:
            include_remote = True
        elif list_remote:
            include_remote = True
        else:
            include_remote = False  
        
        branches_with_state = project_manager.list_prompt_branches_with_state(current_prompt, include_remote=include_remote)
        
        # Filter for remote-only if requested
        if list_remote and not list_all:
            branches_with_state = [b for b in branches_with_state if b['type'] == 'remote']
        
        if not branches_with_state:
            console.print("No branches found")
            return
        
        # Simple list view (like git branch)
        for branch_info in branches_with_state:
            branch_name_display = branch_info['name']
            
            if branch_info['type'] == 'local':
                if branch_info['is_current']:
                    console.print(f"* [green]{branch_name_display}[/green]")
                else:
                    console.print(f"  {branch_name_display}")
            else:
                console.print(f"  [blue]{branch_name_display}[/blue]")
        return
    
    # Handle branch switching/creation (when branch_name is provided)
    if branch_name:
        # Check for unresolved conflicts
        conflicts = project_manager.load_prompt_conflicts(current_prompt, current_branch)
        if conflicts:
            error_exit("You have unresolved merge conflicts. Please resolve them before switching branches.")
        
        # Check for both staged AND unstaged changes before switching (like Git)
        has_staged = project_manager.has_staged_changes(current_prompt, current_branch)
        has_unstaged = project_manager.has_unstaged_changes(current_prompt, current_branch)
        
        if has_staged or has_unstaged:
            if has_staged and has_unstaged:
                error_exit("Your local changes to the following files would be overwritten by switching branches:\n"
                          f"  {current_prompt}.txt\n"
                          "Please commit your changes or stash them before you switch branches.")
            elif has_staged:
                error_exit("Your local changes to the following files would be overwritten by switching branches:\n"
                          f"  {current_prompt}.txt\n"
                          "Please commit your changes or stash them before you switch branches.")
            elif has_unstaged:
                error_exit("Your local changes to the following files would be overwritten by switching branches:\n"
                          f"  {current_prompt}.txt\n"
                          "Please commit your changes or stash them before you switch branches.")
        
        if create:
            # Create new branch and switch to it
            if project_manager.prompt_branch_exists(current_prompt, branch_name):
                error_exit(f"Branch '{branch_name}' already exists")
            
            if project_manager.checkout_prompt_branch(current_prompt, branch_name, create_new=True):
                console.print(f"Switched to a new branch '{branch_name}'")
            else:
                error_exit(f"Failed to create branch '{branch_name}'")
        else:
            # Switch to existing branch
            if branch_name == current_branch:
                console.print(f"Already on '{branch_name}'")
                return
            
            is_remote = project_manager.is_branch_name_remote(branch_name)
            
            if is_remote:
                # Remote branch checkout
                try:
                    remote, remote_branch_name = project_manager.parse_remote_branch(branch_name)
                    if not project_manager.remote_prompt_branch_exists(current_prompt, remote_branch_name, remote):
                        error_exit(f"Remote branch '{branch_name}' does not exist")
                except ValueError as e:
                    error_exit(str(e))
            else:
                # Local branch checkout
                if not project_manager.prompt_branch_exists(current_prompt, branch_name):
                    error_exit(f"Branch '{branch_name}' does not exist")
            
            # Perform checkout
            if project_manager.checkout_prompt_branch(current_prompt, branch_name, create_new=False):
                if is_remote:
                    remote, remote_branch_name = project_manager.parse_remote_branch(branch_name)
                    console.print(f"Branch '{remote_branch_name}' set up to track remote branch '{branch_name}'")
                    console.print(f"Switched to a new branch '{remote_branch_name}'")
                else:
                    console.print(f"Switched to branch '{branch_name}'")
            else:
                error_exit(f"Failed to checkout '{branch_name}'")

@app.command()
def log(
    count: int = typer.Option(10, "--count", "-n", help="Number of versions to show"),
    oneline: bool = typer.Option(False, "--oneline", help="Compact format"),
    all_branches: bool = typer.Option(False, "--all", help="Show all branches"),
    graph: bool = typer.Option(False, "--graph", help="Show ASCII graph of commit history"),
    merge_commits: bool = typer.Option(False, "--merges", help="Show only merge commits")
):
    """Show version history with merge commit support."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        error_exit("No active prompt. Use 'banyan prompt <name>' to set one")
    
    # Load versions
    if all_branches:
        all_versions = []
        branches = project_manager.list_prompt_branches(state.prompt_name)
        for branch in branches:
            branch_versions = project_manager.load_prompt_local_versions(state.prompt_name, branch)
            all_versions.extend(branch_versions)
        versions = all_versions
    else:
        versions = project_manager.load_prompt_local_versions(state.prompt_name, state.branch_name)
    
    if not versions:
        console.print("No commit history found")
        return
    
    # Filter merge commits if requested
    if merge_commits:
        versions = [v for v in versions if v.is_merge_commit()]
        if not versions:
            console.print("No merge commits found")
            return
    
    # Sort by timestamp (newest first)
    def get_timestamp(version):
        try:
            timestamp_str = version.metadata.get('timestamp', '')
            if timestamp_str:
                from datetime import datetime
                return datetime.fromisoformat(timestamp_str)
            else:
                return datetime.min
        except:
            return datetime.min
    
    versions.sort(key=get_timestamp, reverse=True)
    
    # Limit count
    if count > 0:
        versions = versions[:count]
    
    # Display versions
    if oneline:
        # Compact format
        for version in versions:
            author_name = version.metadata.get('author_name', 'Unknown')
            timestamp_str = version.metadata.get('timestamp', '')
            if timestamp_str:
                try:
                    from datetime import datetime
                    timestamp = datetime.fromisoformat(timestamp_str)
                    date_str = timestamp.strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = timestamp_str[:16]
            else:
                date_str = "Unknown date"
            
            branch_info = f"({version.branch}) " if all_branches else ""
            merge_info = " [MERGE]" if version.is_merge_commit() else ""
            
            console.print(f"[yellow]{version.hash}[/yellow] {branch_info}{version.message}{merge_info} - {author_name}, {date_str}")
    else:
        # Detailed format
        for i, version in enumerate(versions):
            author_name = version.metadata.get('author_name', 'Unknown')
            author_email = version.metadata.get('author_email', '')
            timestamp_str = version.metadata.get('timestamp', '')
            
            if timestamp_str:
                try:
                    from datetime import datetime
                    timestamp = datetime.fromisoformat(timestamp_str)
                    date_str = timestamp.strftime('%a %b %d %H:%M:%S %Y')
                except:
                    date_str = timestamp_str
            else:
                date_str = "Unknown date"
            
            # Show graph if requested
            if graph:
                if i == 0:
                    graph_prefix = "* "
                elif version.is_merge_commit():
                    graph_prefix = "|\\ "
                else:
                    graph_prefix = "| "
                console.print(f"{graph_prefix}[yellow]commit {version.hash}[/yellow]")
            else:
                console.print(f"[yellow]commit {version.hash}[/yellow]")
            
            # Show merge information for merge commits
            if version.is_merge_commit():
                parents = [version.parent_hash] + version.merge_parents
                parents_str = " ".join(p for p in parents if p)
                console.print(f"Merge: {parents_str}")
            
            console.print(f"Author: {author_name} <{author_email}>")
            console.print(f"Date:   {date_str}")
            
            # Show branch info if showing all branches
            if all_branches:
                console.print(f"Branch: {version.branch}")
            
            console.print(f"\n    {version.message}\n")

@app.command()
def prompt(
    prompt_name: Optional[str] = typer.Argument(None, help="Prompt to switch to"),
    list_prompts: bool = typer.Option(False, "--list", "-l", help="List prompts"),
    create: Optional[str] = typer.Option(None, "--create", "-c", help="Create new prompt"),
    current: bool = typer.Option(False, "--current", help="Show current prompt")
):
    """Switch between prompts or manage prompts."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Show current prompt
    if current:
        state = project_manager.get_current_prompt_state()
        if state:
            console.print(f"On prompt {state.prompt_name}")
            console.print(f"On branch {state.branch_name}")
        else:
            console.print("No active prompt")
        return
    
    # List prompts
    if list_prompts:
        prompts = project_manager.list_prompts()
        state = project_manager.get_current_prompt_state()
        current_prompt = state.prompt_name if state else None
        
        if not prompts:
            console.print("No prompts found")
            return
        
        for prompt in prompts:
            if prompt == current_prompt:
                console.print(f"* [green]{prompt}[/green]")
            else:
                console.print(f"  {prompt}")
        return
    
    # Create new prompt
    if create:
        # Validate prompt name
        valid, error_msg = validate_prompt_name(create)
        if not valid:
            error_exit(error_msg)
        
        # Check if prompt already exists
        if project_manager.prompt_exists(create):
            error_exit(f"Prompt '{create}' already exists")
        
        # Ask for description
        description = Prompt.ask(f"Enter description for prompt '{create}'", default="")
        
        # Create prompt file
        prompt_file = PromptFile(
            name=create,
            content=f"# {create.title()} Prompt\n\nYour prompt content goes here...",
            description=description
        )
        
        # Save the description to a metadata file for later use during push
        project_manager.save_prompt_metadata(create, {"description": description})
        
        if project_manager.save_prompt_file(prompt_file):
            if project_manager.set_active_prompt(create, "main"):
                console.print(f"Switched to a new prompt '{create}'")
                console.print(f"Description: {description}")
            else:
                console.print(f"Created prompt '{create}'")
                console.print(f"Description: {description}")
        else:
            error_exit(f"Failed to create prompt '{create}'")
        return
    
    # Switch to prompt
    if not prompt_name:
        error_exit("Prompt name required")
    
    # Validate prompt exists
    if not project_manager.prompt_exists(prompt_name):
        error_exit(f"Prompt '{prompt_name}' does not exist")
    
    # Check for uncommitted changes
    current_state = project_manager.get_current_prompt_state()
    if current_state:
        staging_area = project_manager.load_staging_area(current_state.prompt_name, current_state.branch_name)
        if staging_area:
            error_exit("Please commit your changes before switching prompts")
    
    # Switch to the prompt
    if project_manager.set_active_prompt(prompt_name, "main"):
        console.print(f"Switched to prompt '{prompt_name}'")
    else:
        error_exit(f"Failed to switch to prompt '{prompt_name}'")

@app.command()
def reset(
    files: Optional[List[str]] = typer.Argument(None, help="Files to unstage"),
    hard: bool = typer.Option(False, "--hard", help="Discard working directory changes")
):
    """Unstage files or reset working directory."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        error_exit("No active prompt. Use 'banyan prompt <name>' to set one")
    
    staged_files = project_manager.load_staging_area(state.prompt_name, state.branch_name)
    
    if not staged_files:
        return  # No staged files, nothing to do (like git)
    
    if files:
        # Unstage specific files
        for file_pattern in files:
            file_name = file_pattern.replace('.txt', '')
            if project_manager.unstage_file(file_name):
                # No output on success (like git)
                pass
    else:
        # Unstage all files
        if hard and not Confirm.ask("This will discard all changes. Continue?"):
            console.print("Aborted")
            return
    
        project_manager.clear_staging_area(state.prompt_name, state.branch_name)
        
        if hard:
            # Revert working directory changes
            for staged_file in staged_files:
                try:
                    file_path = project_manager.prompts_dir / f"{staged_file.name}.txt"
                    if file_path.exists():
                        file_path.unlink()
                except Exception:
                    pass  # Ignore errors

@app.command()
def config(
    list_config: bool = typer.Option(False, "--list", "-l", help="List configuration"),
    global_config: bool = typer.Option(False, "--global", help="Use global config"),
    set_key: Optional[str] = typer.Option(None, "--set", help="Set key=value")
):
    """Manage configuration."""
    
    project_manager = BanyanProjectManager()
    
    if global_config:
        config_obj = project_manager.load_global_config()
        config_type = "global"
    else:
        if not project_manager.is_banyan_project():
            error_exit("Not in a Banyan project. Use --global or run 'banyan init'")
        config_obj = project_manager.load_config()
        config_type = "local"
    
    if set_key:
        # Set configuration value
        if '=' not in set_key:
            error_exit("Use format key=value")
        
        key, value = set_key.split('=', 1)
        if hasattr(config_obj, key):
            setattr(config_obj, key, value)
            
            if global_config:
                project_manager.save_global_config(config_obj)
            else:
                project_manager.save_config(config_obj)
            
            console.print(f"{key} = {value}")
        else:
            error_exit(f"Unknown configuration key '{key}'")
    else:
        # List configuration
        config_dict = config_obj.to_dict()
        for key, value in config_dict.items():
            # Mask API key for security
            if key == 'api_key' and value:
                display_value = value[:8] + '...' if len(value) > 8 else value
            else:
                display_value = str(value) if value is not None else ''
            
            console.print(f"{key} = {display_value}")

@app.command()
def integrity(
    check: bool = typer.Option(False, "--check", help="Check data integrity"),
    repair: bool = typer.Option(False, "--repair", help="Attempt to repair corrupted files"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Check and repair data integrity."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    results = {}
    
    if check or not repair:
        console.print("Checking project integrity...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Scanning files...", total=None)
            results = project_manager.integrity_manager.verify_project_integrity()
        
        # Display results
        console.print(f"Checked {results['checked_files']} files")
        
        if results['corrupted_files']:
            console.print(f"\n[red]Found {len(results['corrupted_files'])} corrupted files:[/red]")
            for corruption in results['corrupted_files']:
                console.print(f"  {corruption['file']}: {corruption['error']}")
        
        if results['errors']:
            console.print(f"\n[yellow]Encountered {len(results['errors'])} errors:[/yellow]")
            for error in results['errors']:
                if verbose:
                    console.print(f"  {error}")
        
        if not results['corrupted_files'] and not results['errors']:
            console.print("[green]✓ All files passed integrity checks[/green]")
    
    if repair and results.get('corrupted_files'):
        if not Confirm.ask(f"Attempt to repair {len(results['corrupted_files'])} corrupted files?"):
            console.print("Repair cancelled")
            return
        
        repaired_count = 0
        for corruption in results['corrupted_files']:
            file_path = Path(corruption['file'])
            # For now, we can't automatically repair without backups
            console.print(f"Cannot auto-repair {file_path} - no backup available")
        
        console.print(f"Repaired {repaired_count} files")

@app.command()
def maintenance(
    cleanup_days: int = typer.Option(30, "--cleanup-days", help="Remove unused objects older than N days"),
    show_stats: bool = typer.Option(False, "--stats", help="Show storage statistics"),
    clear_cache: bool = typer.Option(False, "--clear-cache", help="Clear all caches")
):
    """Perform maintenance operations."""
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    if show_stats:
        console.print("Storage Statistics:")
        stats = project_manager.storage_manager.get_comprehensive_stats()
        
        storage = stats['storage']
        console.print(f"  Objects: {storage['object_count']}")
        console.print(f"  Total size: {storage['total_size_bytes']:,} bytes")
        console.print(f"  Average size: {storage['average_size_bytes']:.1f} bytes")
        console.print(f"  Deltas: {storage['delta_count']}")
        
        if storage['delta_count'] > 0:
            efficiency = stats['total_efficiency']
            compression_percent = efficiency['compression_saving'] * 100
            console.print(f"  Compression savings: {compression_percent:.1f}%")
    
    if clear_cache:
        project_manager.clear_cache()
        console.print("Cleared all caches")
    
    if cleanup_days > 0:
        console.print(f"Cleaning up objects older than {cleanup_days} days...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Cleaning up...", total=None)
            maintenance_result = project_manager.storage_manager.maintenance(cleanup_days)
        
        removed_count = maintenance_result['objects_removed']
        if removed_count > 0:
            console.print(f"Removed {removed_count} unused objects")
        else:
            console.print("No objects needed cleanup")

@app.command()
def merge(
    source_branch: Optional[str] = typer.Argument(None, help="Branch to merge from"),
    abort: bool = typer.Option(False, "--abort", help="Abort current merge"),
    strategy: str = typer.Option("auto", "--strategy", "-s", help="Merge strategy: auto, ours, theirs, recursive"),
    no_commit: bool = typer.Option(False, "--no-commit", help="Don't auto-commit after merge"),
    squash: bool = typer.Option(False, "--squash", help="Create a single commit instead of merge commit"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="Custom merge commit message")
):
    """Merge branches with full Git-like functionality.
    
    This command performs a three-way merge between the current branch and the specified
    source branch, finding their common ancestor and automatically resolving conflicts
    where possible. 
    
    Merge strategies:
    - auto: Automatic three-way merge with conflict detection (default)
    - ours: Keep current branch content in case of conflicts
    - theirs: Take source branch content in case of conflicts
    - recursive: Advanced recursive merge strategy (future enhancement)
    
    Examples:
        banyan merge feature-branch    # Merge feature-branch into current branch
        banyan merge --abort           # Abort ongoing merge
        banyan merge --no-commit dev   # Merge dev but don't auto-commit
        banyan merge --strategy=ours feature  # Use "ours" strategy for conflicts
    """
    
    project_manager = BanyanProjectManager()
    
    if not project_manager.is_banyan_project():
        error_exit("Not in a Banyan project. Run 'banyan init' first")
    
    # Get current prompt state
    state = project_manager.get_current_prompt_state()
    if not state:
        error_exit("No active prompt. Use 'banyan prompt <name>' to set one")
    
    current_prompt = state.prompt_name
    current_branch = state.branch_name
    
    # Handle merge abort
    if abort:
        result = project_manager.abort_merge(current_prompt, current_branch)
        if result['success']:
            console.print(result['message'])
        else:
            error_exit(result['error'])
        return
    
    # Check if we're in the middle of a merge
    merge_state = project_manager.load_merge_state(current_prompt, current_branch)
    if merge_state:
        # Show merge status and instructions
        console.print("You are in the middle of a merge.")
        
        conflicts = project_manager.load_prompt_conflicts(current_prompt, current_branch)
        if conflicts:
            console.print("\nUnmerged paths:")
            for conflict in conflicts:
                console.print(f"  [red]both modified:[/red] {conflict.name}")
            console.print("\nTo resolve conflicts:")
            console.print("  1. Edit the conflicted files to resolve conflicts")
            console.print("  2. Stage resolved files: banyan add <file>")
            console.print("  3. Complete merge: banyan commit")
            console.print("  4. Or abort merge: banyan merge --abort")
        else:
            console.print("All conflicts resolved. Please commit to complete the merge:")
            console.print("  banyan commit")
        
        console.print(f"\nMerging: {merge_state.source_branch} -> {merge_state.target_branch}")
        return
    
    # Require source branch for new merge
    if not source_branch:
        error_exit("Branch name required for merge")
    
    # Validate source branch exists
    if not project_manager.prompt_branch_exists(current_prompt, source_branch):
        error_exit(f"Branch '{source_branch}' does not exist")
    
    if source_branch == current_branch:
        console.print("Already up to date.")
        return
    
    # Check for uncommitted changes
    staging_area = project_manager.load_staging_area(current_prompt, current_branch)
    if staging_area:
        error_exit("Please commit your changes or stash them before merging.\n"
                  f"You have staged changes in: {', '.join([sf.name for sf in staging_area])}")
    
    # Check for unstaged changes
    if project_manager.has_unstaged_changes(current_prompt, current_branch):
        error_exit("Please commit your changes or stash them before merging.\n"
                  f"You have unstaged changes in: {current_prompt}.txt")
    
    # Start the merge operation
    console.print(f"Merging branch '{source_branch}' into '{current_branch}'")
    
    merge_result = project_manager.start_merge(
        prompt_name=current_prompt,
        target_branch=current_branch,
        source_branch=source_branch,
        strategy=strategy,
        no_commit=no_commit or squash
    )
    
    if not merge_result['success']:
        error_message = merge_result.get('error', 'Unknown merge error')
        if merge_result.get('merge_in_progress'):
            console.print(f"error: {error_message}")
            console.print("hint: Use 'banyan merge --abort' to abort the merge")
        else:
            error_exit(error_message)
        return
    
    # Handle different merge outcomes
    merge_type = merge_result.get('merge_type')
    
    if merge_type == 'up_to_date':
        console.print(merge_result['message'])
        
    elif merge_type == 'fast_forward':
        console.print("Fast-forward")
        console.print(f"Updating {current_branch}..{merge_result['commit_hash']}")
        
    elif merge_type == 'conflict':
        # Merge conflicts occurred
        console.print(f"Auto-merging {current_prompt}")
        for conflict_file in merge_result.get('conflict_files', []):
            console.print(f"CONFLICT (content): Merge conflict in {conflict_file}")
        console.print("Automatic merge failed; fix conflicts and then commit the result.")
        
    elif merge_type == 'merge_commit':
        # Successful automatic merge with commit
        commit_hash = merge_result['commit_hash']
        console.print(merge_result['message'])
        console.print(f"Commit hash: {commit_hash}")
        
    elif merge_type == 'staged':
        # Successful automatic merge, staged for manual commit
        console.print(merge_result['message'])
        if squash:
            console.print("Squash commit prepared. You can now commit with:")
            console.print(f"  banyan commit -m \"Squashed commit from {source_branch}\"")
        else:
            console.print("You can now commit with:")
            console.print("  banyan commit")
    
    else:
        # Unexpected result
        if 'message' in merge_result:
            console.print(merge_result['message'])
        else:
            console.print("Merge completed with unknown status")

def main():
    """Main CLI entry point"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\nAborted")
        sys.exit(1)
    except Exception as e:
        console.print(f"fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 