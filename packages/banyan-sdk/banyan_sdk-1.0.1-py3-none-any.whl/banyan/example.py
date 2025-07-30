#!/usr/bin/env python3
"""
Banyan SDK Usage Examples

This file demonstrates how to use the Banyan SDK for managing, versioning,
and A/B testing your LLM prompts in production.

Examples included:
1. Basic Configuration and Setup
2. Simple Prompt Fetching and Logging
3. Experiment-based Routing
4. Error Handling Best Practices
5. Advanced Configuration Options
6. Different Sticky Context Strategies
7. Statistics and Monitoring
"""

import os
import time
import hashlib
import logging
from typing import Optional, Dict, Any

# Import the Banyan SDK
import banyan

# Configure logging for examples
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def llm_call(prompt: str, user_input: str) -> str:
    """
    Mock LLM function for demonstration.
    In real usage, replace this with your actual LLM API calls.
    """
    # Simulate processing time
    time.sleep(0.1)
    
    # Mock response based on prompt and input
    if "welcome" in prompt.lower():
        return f"Welcome! I see you said: '{user_input}'. How can I help you get started?"
    elif "help" in prompt.lower():
        return f"I'd be happy to help! Regarding '{user_input}', here are some suggestions..."
    else:
        return f"Thank you for your message: '{user_input}'. This is a response from our AI assistant."

def basic_setup():
    """
    Example 1: Basic SDK Configuration and Setup
    
    This shows the minimal setup required to start using Banyan SDK.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Setup and Configuration")
    print("="*60)
    
    # Method 1: Configure with environment variables (recommended for production)
    # Set environment variable: export BANYAN_API_KEY=psk_your_api_key_here
    api_key = os.getenv('BANYAN_API_KEY')
    
    if not api_key:
        print("BANYAN_API_KEY not set. Using demo key for example.")
        api_key = "psk_demo_key_replace_with_real_key"
    
    try:
        # Configure the SDK
        banyan.configure(
            api_key=api_key,
            project_id="demo-project",  # Optional: for project-specific prompts
            max_retries=3,
            background_thread=True
        )
        
        stats = banyan.get_stats()
        print(f"   Initial stats: {stats}")
        
    except Exception as e:
        print(f"Configuration failed: {e}")

def basic_prompt_usage():
    """
    Example 2: Basic Prompt Fetching and Logging
    
    This demonstrates the core workflow: fetch prompt -> use with model -> log usage
    """
    
    try:
        # 1. Fetch a prompt
        print("Fetching prompt...")
        prompt_data = banyan.get_prompt(
            name="welcome-message",
            branch="main",
            use_cache=True
        )
        
        if not prompt_data:
            print("Prompt not found. Creating a demo prompt for this example.")
            # In real usage, you'd create the prompt in your Banyan dashboard
            return
        
        print(f"✅ Fetched prompt: {prompt_data.name}")
        print(f"   Version: {prompt_data.version}")
        print(f"   Branch: {prompt_data.branch}")
        print(f"   Content preview: {prompt_data.content[:100]}...")
        
        # 2. Simulate using the prompt with your model
        user_input = "Hello! I'm new to your platform."
        
        # This is where you'd call your actual model (OpenAI, Anthropic, etc.)
        start_time = time.time()
        model_output = llm_call(prompt_data.content, user_input)
        duration_ms = int((time.time() - start_time) * 1000)
        
        
        # 3. Log the prompt usage
        print("Logging prompt usage...")
        success = banyan.log_prompt(
            input=user_input,
            output=model_output,
            prompt_data=prompt_data,  # Contains all prompt metadata
            model="gpt-4",
            duration_ms=duration_ms,
            metadata={
                "user_type": "new_user",
                "feature": "welcome_flow",
                "environment": "demo"
            }
        )
        
        if success:
            print("Usage logged successfully!")
        else:
            print("Logging queued for retry")
            
    except Exception as e:
        print(f"Error in basic usage: {e}")

def experiment_routing():
    """
    Example 3: A/B Testing with Experiment Routing
    
    This shows how to use experiments for A/B testing different prompt versions.
    """

    user_id = "a_unique_user_id_for_each_of_your_users"
    
    try:
        # Set up experiment routing with sticky user context
        print(f"etting up experiment for user: {user_id}")
        
        experiment_data = banyan.experiment(
            experiment_id="your_experiment_id",  # Your experiment ID
            sticky_context={"user_id": user_id},  # Consistent routing per user
            input_text=None  # Not needed for user_id sticky type
        )
        
        print(f"Experiment active!")
        print(f"Experiment ID: {experiment_data.experiment_id}")
        print(f"Using prompt version: {experiment_data.version}")
        print(f"Sticky value: {experiment_data.sticky_value}")
        print(f"Content preview: {experiment_data.content[:100]}...")
        
        # Use the experiment prompt version
        user_input = "I need help getting started"
        start_time = time.time()
        model_output = llm_call(experiment_data.content, user_input)
        duration_ms = int((time.time() - start_time) * 1000)
        
        
        # Log with experiment context (automatically included)
        success = banyan.log_prompt(
            input=user_input,
            output=model_output,
            model="gpt-4",
            duration_ms=duration_ms,
            metadata={
                "user_id": user_id,
                "experiment_active": True,
            }
        )
        
        if success:
            print("✅ Experiment usage logged with context!")
        
    except RuntimeError as e:
        print(f"No active experiment: {e}")

def Content_based_experiments():
    """
    Example 4: Content-based Experiments
    
    This demonstrates experiments that route based on the input text.
    """
    
    print("Content-based experiments")
    input_text = "What are your business hours?"
    try:
        experiment = banyan.experiment(
            experiment_id="content-based-test",
            input_text=input_text  # Automatically hashes the input text
        )
        print(f"Content sticky: {experiment.sticky_value}")
    except Exception as e:
        print(f"Content-based experiment not available: {e}")
    

def advanced_configuration():
    """
    Example 6: Advanced Configuration Options
    
    This demonstrates advanced SDK features and custom configurations.
    """
    
    # Custom logger instance
    print("Creating custom logger instance")
    try:
        from banyan import PromptStackLogger
        
        custom_logger = PromptStackLogger(
            api_key=os.getenv('BANYAN_API_KEY', 'demo_key'),
            base_url="https://app.usebanyan.com",
            project_id="custom-project",
            max_retries=5,
            retry_delay=2.0,
            queue_size=2000,
            flush_interval=10.0,
            background_thread=True
        )
        
        print("Custom logger created")
        
        # Use custom logger
        prompt_data = custom_logger.get_prompt("test-prompt")
        if prompt_data:
            print(f"Custom logger fetched: {prompt_data.name}")
        
        # Get custom logger stats
        stats = custom_logger.get_stats()
        print(f"Custom logger stats: {stats}")
        
    except Exception as e:
        print(f"Custom logger error: {e}")
    
    # Synchronous mode
    print("Testing synchronous mode")
    try:
        # Configure for synchronous operation
        banyan.configure(
            api_key=os.getenv('BANYAN_API_KEY', 'demo_key'),
            background_thread=False  # Disable background processing
        )
        
        # All operations will be synchronous
        success = banyan.log_prompt(
            input="Sync test",
            output="Sync response",
            prompt_name="sync-test",
            blocking=True
        )
        
        if success:
            print("Synchronous logging successful")
        
    except Exception as e:
        print(f"Synchronous mode error: {e}")

def git_like_workflow_example():
    """
    Example 7: Git-like Prompt Management Workflow
    
    This demonstrates the new Git-like commands for managing prompts:
    - banyan add: Stage files for commit
    - banyan commit: Create versioned snapshots
    - banyan push: Deploy to remote environments
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: Git-like Prompt Management Workflow")
    print("="*60)
    
    print("""
This example shows how to use Banyan's Git-like workflow commands:

1. Initialize a project:
   banyan init --project my-project
   
2. Authenticate:
   banyan login
   
3. Create prompt files in prompts/:
   
   # Create welcome-prompt.txt
   Welcome! How can I help you today?
   
   # Create error-handler.txt
   I apologize for the error. Let me help you resolve this.

4. Stage files for commit (like git add):
   banyan add welcome-prompt           # Stage single prompt
   banyan add .                        # Stage all files
   
5. Check status (like git status):
   banyan status
   
   Output:
   Banyan Status
   Project ID: my-project
   API Key: Configured
   Default Branch: main
   HEAD: No commits yet
   
   Staged files (2):
   Changes to be committed:
     modified: welcome-prompt
     modified: error-handler
   
   Use 'banyan commit -m "message"' to create a commit

6. Create a commit with semantic versioning (like git commit):
   banyan commit -m "Add initial prompts"
   
   # Or with specific version control:
   banyan commit -m "Major update" --major     # Bumps to 2.0.0
   banyan commit -m "New feature" --minor      # Bumps to 1.1.0 (default)
   banyan commit -m "Bug fix" --patch          # Bumps to 1.0.1
   banyan commit -m "Custom version" --version 2.1.0
   
   Output:
   ✓ Created commit abc12345
   ✓ Version: 1.1.0
   ✓ Files: 2
   ✓ Author: John Doe <john@example.com>
   
   ┌─────────────────┬───────────┬──────────┐
   │ File            │ Operation │ Hash     │
   ├─────────────────┼───────────┼──────────┤
   │ welcome-prompt  │ modified  │ a1b2c3d4 │
   │ error-handler   │ modified  │ e5f6g7h8 │
   └─────────────────┴───────────┴──────────┘
   
   Use 'banyan push' to publish this commit to remote

7. Push commits to remote (like git push):
   banyan push                         # Push latest commit
   banyan push --all                   # Push all unpushed commits
   banyan push --commit abc12345       # Push specific commit
   
   Output:
   Pushing 1 commit...
   
   Commit abc12345 (v1.1.0)
     Message: Add initial prompts
     Author: John Doe <john@example.com>
     Files: 2
       modified welcome-prompt
       modified error-handler
   
   ✓ Pushed commit abc12345
   ✓ Successfully pushed 1 commit

8. Full workflow status check:
   banyan status
   
   Output:
   Banyan Status
   Project ID: my-project
   API Key: Configured
   Default Branch: main
   HEAD: abc12345
   
   No files staged for commit.
   Use 'banyan add <files>' to stage files
   
   No unpushed commits.
   
   Working directory (2 files):
   All files are staged
   
   Quick commands:
     banyan add .              # Stage all files
     banyan commit -m "msg"    # Create a commit
     banyan push               # Push to remote

Key Benefits of Git-like Workflow:

1. **Familiar Interface**: Uses commands developers already know
2. **Semantic Versioning**: Automatic version management with --major, --minor, --patch
3. **Staging Area**: Review changes before committing
4. **Local Commits**: Work offline and push when ready
5. **Version History**: Track all changes with commit messages
6. **Branch Support**: Work on features in isolation
7. **Rollback Capability**: Easy to revert to previous versions

Advanced Workflows:

# Feature branch workflow
banyan branch -b feature/new-tone
banyan add .
banyan commit -m "Experiment with friendlier tone"
banyan push

# Hotfix workflow  
banyan commit -m "Fix critical typo"
banyan push

# Release workflow
banyan commit -m "Major feature release"
banyan push

This workflow provides the same level of control and safety as Git,
but specifically designed for prompt management and LLM applications.
""")

def git_like_merge_example():
    """
    Example 8: Git-like Merge Functionality
    
    This demonstrates the comprehensive merge system that works just like Git merge:
    - Three-way merge with common ancestor detection
    - Fast-forward merges when possible
    - Conflict detection and resolution
    - Merge state tracking
    - Abort functionality
    """
    print("\n" + "="*60)
    print("EXAMPLE 8: Git-like Merge Functionality")
    print("="*60)
    
    print("""
This example shows how to use Banyan's Git-like merge functionality:

1. Create and switch to branches:
   banyan prompt my-prompt                    # Set active prompt
   banyan branch feature                      # Create feature branch
   banyan branch -b feature-new              # Create and switch to new branch
   
2. Make changes in different branches:
   # On feature branch
   echo "Feature content" > prompts/my-prompt.txt
   banyan add my-prompt
   banyan commit -m "Add feature"
   
   # Switch to main and make different changes
   banyan branch main
   echo "Main content" > prompts/my-prompt.txt
   banyan add my-prompt
   banyan commit -m "Update main"

3. Merge branches (various scenarios):

   A) Fast-forward merge (when target is ancestor of source):
      banyan merge feature                    # Fast-forward if possible
      
   B) Three-way merge (when both branches have changes):
      banyan merge feature                    # Creates merge commit
      
   C) Merge with conflicts:
      banyan merge feature                    # May create conflicts
      # Edit files to resolve conflicts
      banyan add my-prompt                    # Mark conflicts as resolved
      banyan commit                           # Complete the merge
      
   D) Merge strategies:
      banyan merge --strategy=ours feature   # Keep current branch content
      banyan merge --strategy=theirs feature # Take source branch content
      banyan merge --strategy=auto feature   # Automatic three-way merge
      
   E) No-commit merge (stage for manual commit):
      banyan merge --no-commit feature       # Merge but don't auto-commit
      banyan commit -m "Custom merge message"
      
   F) Squash merge (create single commit instead of merge commit):
      banyan merge --squash feature          # Squash all changes
      banyan commit -m "Squashed feature"

4. Handle merge conflicts:
   When conflicts occur, files contain Git-style conflict markers:
   
   <<<<<<< HEAD (current branch)
   Current branch content
   ||||||| base
   Original common content
   =======
   Source branch content
   >>>>>>> source branch
   
   Steps to resolve:
   1. Edit files to remove conflict markers and choose desired content
   2. Stage resolved files: banyan add <file>
   3. Complete merge: banyan commit
   4. Or abort merge: banyan merge --abort

5. Merge state tracking:
   banyan status                             # Shows merge in progress
   banyan merge --abort                      # Abort ongoing merge
   banyan log --merges                       # Show only merge commits
   banyan log --graph                        # Show commit graph

6. Advanced merge commands:
   banyan merge --abort                      # Abort current merge
   banyan merge --no-commit feature          # Merge without auto-commit
   banyan merge -m "Custom message" feature  # Custom merge message
   
Example Merge Workflow:

# Start with main branch
banyan prompt my-prompt
banyan branch main

# Create and work on feature branch
banyan branch -b feature
echo "Add new feature X" >> prompts/my-prompt.txt
banyan add my-prompt
banyan commit -m "Implement feature X"

# Switch back to main and make different changes  
banyan branch main
echo "Fix bug Y" >> prompts/my-prompt.txt
banyan add my-prompt
banyan commit -m "Fix critical bug Y"

# Merge feature into main
banyan merge feature

# Possible outcomes:
# 1. Fast-forward: Feature is simply applied to main
# 2. Automatic merge: Creates merge commit with both changes
# 3. Conflict: Shows conflict markers, requires manual resolution

# If conflicts occur:
# Edit prompts/my-prompt.txt to resolve conflicts
banyan add my-prompt
banyan commit  # Completes the merge

# View merge history
banyan log --oneline --graph

Key Features:

✓ Three-way merge algorithm finds common ancestors
✓ Fast-forward detection when no divergent changes
✓ Automatic conflict detection and resolution  
✓ Git-style conflict markers with base content
✓ Merge state persistence across CLI sessions
✓ Multiple merge strategies (auto, ours, theirs)
✓ Proper merge commits with multiple parents
✓ Abort functionality to cancel merges
✓ Full integration with existing branch/commit system

This merge system provides the same level of functionality as Git merge,
making it familiar for developers and robust for production use.
""")

def main():
    """
    Run all examples in sequence
    """
    print("This script demonstrates various features of the Banyan SDK.")
    print("For production use, make sure to set your BANYAN_API_KEY environment variable.")
    
    try:
        # Run all examples
        basic_setup()
        basic_prompt_usage()
        experiment_routing()
        Content_based_experiments()
        advanced_configuration()
        git_like_workflow_example()
        git_like_merge_example()  # Add the new merge example
        
        # Final cleanup
        print("Shutting down...")
        
        try:
            banyan.shutdown(timeout=10)
            print("Banyan shutdown completed successfully")
        except Exception as e:
            print(f"Shutdown warning: {e}")
        
        print("All examples completed!")
        print("\nNext steps:")
        print("1. Get your API key from the Banyan dashboard")
        print("2. Set BANYAN_API_KEY environment variable")
        print("3. Initialize a project with 'banyan init'")
        print("4. Create prompts in prompts/ directory")
        print("5. Use 'banyan add', 'banyan commit', 'banyan push' workflow")
        print("6. Create branches with 'banyan branch -b <name>'")
        print("7. Merge branches with 'banyan merge <branch>'")
        print("8. Set up experiments for A/B testing")
        print("9. Integrate with your production LLM calls")
        
    except KeyboardInterrupt:
        print("Examples interrupted by user")
        banyan.shutdown(timeout=5)
    except Exception as e:
        print(f"Unexpected error: {e}")
        banyan.shutdown(timeout=5)

if __name__ == "__main__":
    main()
