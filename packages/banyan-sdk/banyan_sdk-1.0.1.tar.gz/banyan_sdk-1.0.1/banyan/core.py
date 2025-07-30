"""
Banyan Core API Client

Low-level REST API methods used by both the SDK and CLI tools.
This module provides the foundational HTTP client functionality.
"""

import requests
import json
import time
import hashlib
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class APIResponse:
    """Standardized API response wrapper"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None

class BanyanAPIClient:
    """
    Core API client for Banyan platform
    
    Handles authentication, request/response, retries, and error handling.
    Used by both SDK and CLI components.
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.usebanyan.com",
        project_id: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 10
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.project_id = project_id
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'banyan-sdk/1.0.0'
        })
        
        if self.project_id:
            self.session.headers['X-Project-Id'] = self.project_id
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> APIResponse:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Merge headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=request_headers,
                    timeout=self.timeout
                )
                
                # Handle different response types
                if response.status_code == 200 or response.status_code == 201:
                    try:
                        return APIResponse(
                            success=True,
                            data=response.json(),
                            status_code=response.status_code
                        )
                    except json.JSONDecodeError:
                        return APIResponse(
                            success=True,
                            data={"message": response.text},
                            status_code=response.status_code
                        )
                
                elif response.status_code == 404:
                    return APIResponse(
                        success=False,
                        error="Resource not found",
                        status_code=404
                    )
                
                elif response.status_code == 401:
                    return APIResponse(
                        success=False,
                        error="Invalid API key",
                        status_code=401
                    )
                
                else:
                    error_msg = f"HTTP {response.status_code}"
                    try:
                        # Check if response is HTML (like error pages)
                        if response.headers.get('content-type', '').startswith('text/html'):
                            error_msg = f"Server error (HTTP {response.status_code}) - received HTML error page instead of JSON response. Server may be down or misconfigured."
                        else:
                            error_data = response.json()
                            if 'error' in error_data:
                                error_msg = error_data['error']
                            elif 'message' in error_data:
                                error_msg = error_data['message']
                    except:
                        error_msg = response.text[:200] if response.text else error_msg
                    
                    return APIResponse(
                        success=False,
                        error=error_msg,
                        status_code=response.status_code
                    )
                        
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue
                else:
                    return APIResponse(
                        success=False,
                        error=f"Network error: {str(e)}"
                    )
        
        return APIResponse(
            success=False,
            error="Max retries exceeded"
        )
    
    # Prompt-related API methods
    def get_prompt(
        self,
        name: str,
        version: Optional[str] = None,
        branch: str = "main",
        project_id: Optional[str] = None
    ) -> APIResponse:
        """Fetch a prompt by name"""
        endpoint = f"api/logs/prompt/{name}"
        params = {'branch': branch}
        if version:
            params['version'] = version
        
        headers = {}
        if project_id:
            headers['X-Project-Id'] = project_id
        
        return self._make_request('GET', endpoint, params=params, headers=headers)
    
    def create_prompt(
        self,
        name: str,
        content: str,
        branch: str = "main",
        metadata: Optional[Dict] = None,
        project_id: Optional[str] = None
    ) -> APIResponse:
        """Create a new prompt"""
        endpoint = "api/logs/cli/prompts"
        data = {
            'name': name,
            'content': content,
            'branch': branch,
            'metadata': metadata or {},
            'project_id': project_id
        }
        
        return self._make_request('POST', endpoint, data=data)
    
    def create_prompt_version(
        self,
        name: str,
        content: str,
        version: str,
        change_message: str,
        branch: str = "main",
        project_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> APIResponse:
        """Create a new version of a prompt"""
        endpoint = "api/logs/cli/prompts/version"
        data = {
            'name': name,
            'content': content,
            'version': version,
            'change_message': change_message,
            'branch': branch,
            'project_id': project_id,
            'metadata': metadata or {}
        }
        
        return self._make_request('POST', endpoint, data=data)
    
    def _get_prompt_id_by_name(self, name: str, project_id: str) -> Optional[str]:
        """Get prompt ID by name from a project"""
        endpoint = "api/logs/cli/prompts"
        params = {'project_id': project_id} if project_id else {}
        response = self._make_request('GET', endpoint, params=params)
        
        if response.success and response.data:
            prompts = response.data.get('prompts', [])
            for prompt in prompts:
                if prompt.get('name') == name:
                    return prompt.get('id')
        
        return None
    
    def update_prompt(
        self,
        prompt_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict] = None,
        branch: Optional[str] = None
    ) -> APIResponse:
        """Update an existing prompt"""
        endpoint = f"api/logs/cli/prompts/{prompt_id}"
        data = {}
        
        if content is not None:
            data['content'] = content
        if metadata is not None:
            data['metadata'] = metadata
        if branch is not None:
            data['branch'] = branch
        
        return self._make_request('PUT', endpoint, data=data)
    
    def list_prompts(
        self,
        project_id: Optional[str] = None,
        branch: Optional[str] = None
    ) -> APIResponse:
        """List all prompts in a project"""
        endpoint = "api/logs/cli/prompts"
        params = {}
        if branch:
            params['branch'] = branch
        if project_id:
            params['project_id'] = project_id
        
        return self._make_request('GET', endpoint, params=params)
    
    def delete_prompt(self, prompt_id: str) -> APIResponse:
        """Delete a prompt"""
        endpoint = f"api/logs/cli/prompts/{prompt_id}"
        return self._make_request('DELETE', endpoint)
    
    # Logging API methods
    def log_prompt_usage(
        self,
        prompt_id: Optional[str] = None,
        prompt_name: Optional[str] = None,
        version: Optional[str] = None,
        branch_name: Optional[str] = None,
        input_text: str = "",
        output_text: str = "",
        model: Optional[str] = None,
        metadata: Optional[Dict] = None,
        duration_ms: Optional[int] = None,
        experiment_id: Optional[str] = None,
        experiment_version_id: Optional[str] = None,
        sticky_key: Optional[str] = None,
        sticky_value: Optional[str] = None
    ) -> APIResponse:
        """Log prompt usage"""
        endpoint = "api/logs/prompt-usage"
        
        data = {
            'input': input_text,
            'output': output_text,
            'metadata': metadata or {}
        }
        
        # Add optional fields
        if prompt_id:
            data['prompt_id'] = prompt_id
        if prompt_name:
            data['prompt_name'] = prompt_name
        if version:
            data['version'] = version
        if branch_name:
            data['branch_name'] = branch_name
        if model:
            data['model'] = model
        if duration_ms:
            data['duration_ms'] = duration_ms
        if experiment_id:
            data['experiment_id'] = experiment_id
        if experiment_version_id:
            data['experiment_version_id'] = experiment_version_id
        if sticky_key:
            data['sticky_key'] = sticky_key
        if sticky_value:
            data['sticky_value'] = sticky_value
        
        return self._make_request('POST', endpoint, data=data)
    
    # Experiment API methods
    def get_experiment(self, experiment_id: str) -> APIResponse:
        """Get experiment details"""
        endpoint = f"api/experiments/{experiment_id}"
        return self._make_request('GET', endpoint)
    
    def route_experiment(
        self,
        experiment_id: str,
        sticky_key: str,
        sticky_value: str
    ) -> APIResponse:
        """Route experiment to get appropriate prompt version"""
        endpoint = "api/experiments/route"
        data = {
            'experimentId': experiment_id,
            'stickyKey': sticky_key,
            'stickyValue': sticky_value,
            'apiKey': self.api_key
        }
        return self._make_request('POST', endpoint, data=data)
    
    # Project API methods
    def get_project(self, project_id: Optional[str] = None) -> APIResponse:
        """Get project details"""
        pid = project_id or self.project_id
        if not pid:
            return APIResponse(success=False, error="No project ID specified")
        
        endpoint = f"api/projects/{pid}"
        return self._make_request('GET', endpoint)
    
    def list_projects(self) -> APIResponse:
        """List available projects"""
        endpoint = "api/projects"
        return self._make_request('GET', endpoint)
    
    # Authentication methods
    def validate_api_key(self) -> APIResponse:
        """Validate the current API key"""
        endpoint = "api/auth/validate"
        return self._make_request('GET', endpoint)
    
    def close(self):
        """Close the session"""
        self.session.close() 