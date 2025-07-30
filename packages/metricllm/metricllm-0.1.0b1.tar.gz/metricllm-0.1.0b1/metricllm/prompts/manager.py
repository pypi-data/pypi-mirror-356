"""
Prompt management system with versioning.
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

from metricllm.utils.logging import get_logger
from metricllm.storage.file_store import FileStore


class PromptManager:
    """Manages prompts with versioning and template support."""

    def __init__(self, storage_path: str = "data/prompts"):
        self.storage_path = storage_path
        self.file_store = FileStore()
        self.logger = get_logger(__name__)
        self.prompts = {}
        self._ensure_storage_directory()
        self._load_prompts()

    def _ensure_storage_directory(self):
        """Ensure the storage directory exists."""
        os.makedirs(self.storage_path, exist_ok=True)

    def _load_prompts(self):
        """Load existing prompts from storage."""
        try:
            prompts_file = os.path.join(self.storage_path, "prompts.json")
            if os.path.exists(prompts_file):
                with open(prompts_file, 'r', encoding='utf-8') as f:
                    self.prompts = json.load(f)
                self.logger.info(f"Loaded {len(self.prompts)} prompts from storage")
        except Exception as e:
            self.logger.error(f"Failed to load prompts: {str(e)}")
            self.prompts = {}

    def _save_prompts(self):
        """Save prompts to storage."""
        try:
            prompts_file = os.path.join(self.storage_path, "prompts.json")
            with open(prompts_file, 'w', encoding='utf-8') as f:
                json.dump(self.prompts, f, indent=2, ensure_ascii=False)
            self.logger.info("Prompts saved to storage")
        except Exception as e:
            self.logger.error(f"Failed to save prompts: {str(e)}")

    def create_prompt(self,
                      name: str,
                      template: str,
                      description: str = "",
                      tags: List[str] = None,
                      variables: List[str] = None,
                      metadata: Dict[str, Any] = None) -> str:
        """
        Create a new prompt template.
        
        Args:
            name: Prompt name
            template: Prompt template with variables
            description: Prompt description
            tags: List of tags for categorization
            variables: List of variable names in the template
            metadata: Additional metadata
        
        Returns:
            Version ID of the created prompt
        """
        if not name or not template:
            raise ValueError("Name and template are required")

        # Generate version ID
        version_id = self._generate_version_id(template)

        # Extract variables from template if not provided
        if variables is None:
            variables = self._extract_variables(template)

        prompt_data = {
            "name": name,
            "template": template,
            "description": description,
            "tags": tags or [],
            "variables": variables,
            "metadata": metadata or {},
            "version_id": version_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "usage_count": 0,
            "versions": [version_id]
        }

        # If prompt exists, create new version
        if name in self.prompts:
            existing_prompt = self.prompts[name]
            prompt_data["versions"] = existing_prompt["versions"] + [version_id]
            prompt_data["usage_count"] = existing_prompt["usage_count"]
            prompt_data["created_at"] = existing_prompt["created_at"]

        self.prompts[name] = prompt_data
        self._save_prompts()

        self.logger.info(f"Created prompt '{name}' with version {version_id}")
        return version_id

    def get_prompt(self, name: str, version_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get a prompt by name and optional version.
        
        Args:
            name: Prompt name
            version_id: Specific version ID (latest if not provided)
        
        Returns:
            Prompt data or None if not found
        """
        if name not in self.prompts:
            return None

        prompt_data = self.prompts[name].copy()

        # If specific version requested, check if it exists
        if version_id and version_id not in prompt_data["versions"]:
            return None

        return prompt_data

    def render_prompt(self, name: str, variables: Dict[str, str], version_id: Optional[str] = None) -> Optional[str]:
        """
        Render a prompt template with provided variables.
        
        Args:
            name: Prompt name
            variables: Dictionary of variable values
            version_id: Specific version ID
        
        Returns:
            Rendered prompt or None if not found
        """
        prompt_data = self.get_prompt(name, version_id)
        if not prompt_data:
            return None

        template = prompt_data["template"]

        try:
            # Simple string replacement for variables
            rendered = template
            for var_name, var_value in variables.items():
                placeholder = f"{{{var_name}}}"
                rendered = rendered.replace(placeholder, str(var_value))

            # Increment usage count
            self.prompts[name]["usage_count"] += 1
            self._save_prompts()

            self.logger.info(f"Rendered prompt '{name}' with variables: {list(variables.keys())}")
            return rendered

        except Exception as e:
            self.logger.error(f"Failed to render prompt '{name}': {str(e)}")
            return None

    def list_prompts(self, tags: List[str] = None) -> List[Dict[str, Any]]:
        """
        List all prompts, optionally filtered by tags.
        
        Args:
            tags: Filter by tags
        
        Returns:
            List of prompt summaries
        """
        prompts_list = []

        for name, prompt_data in self.prompts.items():
            # Filter by tags if provided
            if tags and not any(tag in prompt_data.get("tags", []) for tag in tags):
                continue

            summary = {
                "name": name,
                "description": prompt_data.get("description", ""),
                "tags": prompt_data.get("tags", []),
                "variables": prompt_data.get("variables", []),
                "version_count": len(prompt_data.get("versions", [])),
                "current_version": prompt_data.get("version_id", ""),
                "usage_count": prompt_data.get("usage_count", 0),
                "created_at": prompt_data.get("created_at", ""),
                "updated_at": prompt_data.get("updated_at", "")
            }
            prompts_list.append(summary)

        return sorted(prompts_list, key=lambda x: x["updated_at"], reverse=True)

    def update_prompt(self,
                      name: str,
                      template: str = None,
                      description: str = None,
                      tags: List[str] = None,
                      variables: List[str] = None,
                      metadata: Dict[str, Any] = None) -> Optional[str]:
        """
        Update an existing prompt.
        
        Args:
            name: Prompt name
            template: New template (creates new version if changed)
            description: New description
            tags: New tags
            variables: New variables list
            metadata: New metadata
        
        Returns:
            New version ID if template changed, current version ID otherwise
        """
        if name not in self.prompts:
            return None

        prompt_data = self.prompts[name]
        current_template = prompt_data["template"]

        # Update non-template fields
        if description is not None:
            prompt_data["description"] = description
        if tags is not None:
            prompt_data["tags"] = tags
        if metadata is not None:
            prompt_data["metadata"] = metadata

        # If template changed, create new version
        if template is not None and template != current_template:
            new_version_id = self._generate_version_id(template)
            prompt_data["template"] = template
            prompt_data["version_id"] = new_version_id
            prompt_data["versions"].append(new_version_id)

            # Update variables if not provided
            if variables is None:
                variables = self._extract_variables(template)
            prompt_data["variables"] = variables

            version_id = new_version_id
        else:
            if variables is not None:
                prompt_data["variables"] = variables
            version_id = prompt_data["version_id"]

        prompt_data["updated_at"] = datetime.now().isoformat()
        self._save_prompts()

        self.logger.info(f"Updated prompt '{name}' - version: {version_id}")
        return version_id

    def delete_prompt(self, name: str) -> bool:
        """
        Delete a prompt.
        
        Args:
            name: Prompt name
        
        Returns:
            True if deleted, False if not found
        """
        if name not in self.prompts:
            return False

        del self.prompts[name]
        self._save_prompts()

        self.logger.info(f"Deleted prompt '{name}'")
        return True

    def get_prompt_versions(self, name: str) -> List[str]:
        """
        Get all versions of a prompt.
        
        Args:
            name: Prompt name
        
        Returns:
            List of version IDs
        """
        if name not in self.prompts:
            return []

        return self.prompts[name].get("versions", [])

    def get_prompt_analytics(self, name: str = None) -> Dict[str, Any]:
        """
        Get analytics for prompts.
        
        Args:
            name: Specific prompt name (all prompts if None)
        
        Returns:
            Analytics data
        """
        if name:
            if name not in self.prompts:
                return {}

            prompt_data = self.prompts[name]
            return {
                "name": name,
                "total_usage": prompt_data.get("usage_count", 0),
                "version_count": len(prompt_data.get("versions", [])),
                "created_at": prompt_data.get("created_at", ""),
                "last_used": prompt_data.get("updated_at", ""),
                "variables": prompt_data.get("variables", []),
                "tags": prompt_data.get("tags", [])
            }
        else:
            # Overall analytics
            total_prompts = len(self.prompts)
            total_usage = sum(p.get("usage_count", 0) for p in self.prompts.values())
            total_versions = sum(len(p.get("versions", [])) for p in self.prompts.values())

            # Most used prompts
            most_used = sorted(
                [(name, data.get("usage_count", 0)) for name, data in self.prompts.items()],
                key=lambda x: x[1],
                reverse=True
            )[:5]

            # Tag distribution
            all_tags = []
            for prompt_data in self.prompts.values():
                all_tags.extend(prompt_data.get("tags", []))

            tag_counts = {}
            for tag in all_tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            return {
                "total_prompts": total_prompts,
                "total_usage": total_usage,
                "total_versions": total_versions,
                "average_usage_per_prompt": round(total_usage / max(total_prompts, 1), 2),
                "most_used_prompts": most_used,
                "tag_distribution": tag_counts,
                "prompts_with_multiple_versions": sum(
                    1 for p in self.prompts.values() if len(p.get("versions", [])) > 1)
            }

    def _generate_version_id(self, template: str) -> str:
        """Generate a version ID based on template content."""
        return hashlib.md5(template.encode('utf-8')).hexdigest()[:8]

    def _extract_variables(self, template: str) -> List[str]:
        """Extract variable names from template."""
        import re
        # Find all {variable_name} patterns
        variables = re.findall(r'\{([^}]+)\}', template)
        return list(set(variables))  # Remove duplicates
