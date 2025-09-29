#!/usr/bin/env python3
"""
Figma Design Analyzer for User Story Generation

This module provides utilities to extract design information from Figma
and integrate it into user story requirements using Figma MCP tools.
"""

import json
import re
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DesignComponent:
    """Represents a design component with its properties"""
    id: str
    name: str
    type: str
    properties: Dict[str, Any]
    children: List['DesignComponent']

    def to_dict(self):
        return asdict(self)

@dataclass
class DesignRequirements:
    """Extracted design requirements for user story enhancement"""
    components: List[DesignComponent]
    patterns: List[str]
    constraints: List[str]
    accessibility_notes: List[str]
    interaction_patterns: List[str]

    def to_dict(self):
        return asdict(self)

class FigmaDesignAnalyzer:
    """Main class for analyzing Figma designs and extracting requirements"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.figma_enabled = config.get('figma', {}).get('enabled', False)
        self.default_file_key = config.get('figma', {}).get('default_file_key', '')
        self.design_system_file = config.get('figma', {}).get('design_system_file', '')

    def extract_figma_urls(self, text: str) -> List[str]:
        """Extract Figma URLs from text input"""
        figma_pattern = r'https://www\.figma\.com/design/([a-zA-Z0-9]+)/[a-zA-Z0-9-]+'
        return re.findall(figma_pattern, text)

    def parse_figma_url(self, url: str) -> Dict[str, str]:
        """Parse Figma URL to extract file key and node ID"""
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip('/').split('/')

            if len(path_parts) >= 2:
                file_key = path_parts[1]

                # Look for node-id parameter
                node_id = None
                if parsed.query:
                    query_params = dict(param.split('=') for param in parsed.query.split('&') if '=' in param)
                    node_id = query_params.get('node-id')

                return {
                    'file_key': file_key,
                    'node_id': node_id,
                    'file_name': path_parts[2] if len(path_parts) > 2 else 'Unknown'
                }
        except Exception as e:
            logger.error(f"Error parsing Figma URL {url}: {e}")

        return {}

    async def get_design_metadata(self, file_key: str, node_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get design metadata using Figma MCP"""
        if not self.figma_enabled:
            logger.warning("Figma integration is disabled")
            return None

        try:
            # Use Figma MCP get_metadata tool
            # This would need to be implemented with actual MCP calls
            metadata = await self._call_figma_mcp('get_metadata', {
                'fileKey': file_key,
                'nodeId': node_id or ''
            })

            return metadata
        except Exception as e:
            logger.error(f"Error getting design metadata for {file_key}: {e}")
            return None

    async def get_design_code(self, file_key: str, node_id: str) -> Optional[Dict[str, Any]]:
        """Get design code representation using Figma MCP"""
        if not self.figma_enabled:
            return None

        try:
            # Use Figma MCP get_code tool
            code_data = await self._call_figma_mcp('get_code', {
                'fileKey': file_key,
                'nodeId': node_id
            })

            return code_data
        except Exception as e:
            logger.error(f"Error getting design code for {file_key}/{node_id}: {e}")
            return None

    async def get_design_screenshot(self, file_key: str, node_id: str) -> Optional[str]:
        """Get design screenshot using Figma MCP"""
        if not self.figma_enabled:
            return None

        try:
            # Use Figma MCP get_screenshot tool
            screenshot_data = await self._call_figma_mcp('get_screenshot', {
                'fileKey': file_key,
                'nodeId': node_id
            })

            return screenshot_data
        except Exception as e:
            logger.error(f"Error getting design screenshot for {file_key}/{node_id}: {e}")
            return None

    async def _call_figma_mcp(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Make MCP tool calls to Figma (placeholder implementation)"""
        # This is a placeholder - actual implementation would use MCP SDK
        # For now, return mock data structure
        logger.info(f"Calling Figma MCP {tool_name} with params: {params}")

        # Mock response structure
        if tool_name == 'get_metadata':
            return {
                'name': 'Mock Component',
                'type': 'FRAME',
                'children': [
                    {
                        'id': '1:2',
                        'name': 'Button',
                        'type': 'COMPONENT',
                        'properties': {
                            'width': 120,
                            'height': 40,
                            'backgroundColor': '#007BFF'
                        }
                    }
                ]
            }
        elif tool_name == 'get_code':
            return {
                'code': '<button className="btn btn-primary">Click me</button>',
                'assets': {}
            }
        elif tool_name == 'get_screenshot':
            return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='

        return None

    def parse_design_hierarchy(self, metadata: Dict[str, Any]) -> List[DesignComponent]:
        """Parse Figma metadata into component hierarchy"""
        components = []

        def parse_node(node_data: Dict[str, Any]) -> DesignComponent:
            return DesignComponent(
                id=node_data.get('id', ''),
                name=node_data.get('name', ''),
                type=node_data.get('type', ''),
                properties=node_data.get('properties', {}),
                children=[parse_node(child) for child in node_data.get('children', [])]
            )

        if 'children' in metadata:
            for child in metadata['children']:
                components.append(parse_node(child))

        return components

    def extract_design_requirements(self, components: List[DesignComponent]) -> DesignRequirements:
        """Extract design requirements from component hierarchy"""
        requirements = DesignRequirements(
            components=components,
            patterns=[],
            constraints=[],
            accessibility_notes=[],
            interaction_patterns=[]
        )

        for component in components:
            self._analyze_component(component, requirements)

        return requirements

    def _analyze_component(self, component: DesignComponent, requirements: DesignRequirements):
        """Analyze individual component for requirements"""
        # Extract component types and patterns
        if component.type == 'COMPONENT':
            requirements.patterns.append(f"Reusable {component.name} component")

        # Extract interaction patterns
        if 'onClick' in component.properties:
            requirements.interaction_patterns.append(f"{component.name} has click interaction")

        # Extract accessibility information
        if 'accessibility' in component.properties:
            requirements.accessibility_notes.append(f"{component.name}: {component.properties['accessibility']}")

        # Extract constraints
        if 'constraints' in component.properties:
            requirements.constraints.append(f"{component.name} layout constraints: {component.properties['constraints']}")

        # Recursively analyze children
        for child in component.children:
            self._analyze_component(child, requirements)

    def format_design_context(self, requirements: DesignRequirements) -> str:
        """Format design requirements for inclusion in user story"""
        context_parts = []

        if requirements.components:
            context_parts.append("## Design Components")
            for component in requirements.components[:5]:  # Limit to top 5 components
                context_parts.append(f"- **{component.name}** ({component.type}): {component.properties.get('description', 'No description')}")

        if requirements.patterns:
            context_parts.append("\n## Design Patterns")
            for pattern in requirements.patterns[:3]:
                context_parts.append(f"- {pattern}")

        if requirements.interaction_patterns:
            context_parts.append("\n## Interaction Patterns")
            for pattern in requirements.interaction_patterns[:3]:
                context_parts.append(f"- {pattern}")

        if requirements.constraints:
            context_parts.append("\n## Design Constraints")
            for constraint in requirements.constraints[:3]:
                context_parts.append(f"- {constraint}")

        if requirements.accessibility_notes:
            context_parts.append("\n## Accessibility Requirements")
            for note in requirements.accessibility_notes[:3]:
                context_parts.append(f"- {note}")

        return "\n".join(context_parts)

    async def analyze_design_from_urls(self, text: str) -> Optional[str]:
        """Main method to analyze designs from text containing Figma URLs"""
        if not self.figma_enabled:
            return None

        figma_urls = self.extract_figma_urls(text)

        if not figma_urls:
            logger.info("No Figma URLs found in text")
            return None

        all_requirements = []

        for url in figma_urls:
            url_info = self.parse_figma_url(url)

            if url_info.get('file_key'):
                metadata = await self.get_design_metadata(url_info['file_key'], url_info.get('node_id'))

                if metadata:
                    components = self.parse_design_hierarchy(metadata)
                    requirements = self.extract_design_requirements(components)
                    all_requirements.append(requirements)

        if not all_requirements:
            return None

        # Combine all design requirements
        combined_requirements = DesignRequirements(
            components=[comp for req in all_requirements for comp in req.components],
            patterns=[pattern for req in all_requirements for pattern in req.patterns],
            constraints=[constraint for req in all_requirements for constraint in req.constraints],
            accessibility_notes=[note for req in all_requirements for note in req.accessibility_notes],
            interaction_patterns=[pattern for req in all_requirements for pattern in req.interaction_patterns]
        )

        return self.format_design_context(combined_requirements)

    def get_design_system_info(self) -> Dict[str, Any]:
        """Get design system information from configured design system file"""
        if not self.design_system_file:
            return {}

        # This would query the design system file for tokens, patterns, etc.
        return {
            'colors': ['primary', 'secondary', 'success', 'warning', 'danger'],
            'typography': ['heading1', 'heading2', 'body', 'caption'],
            'spacing': ['xs', 'sm', 'md', 'lg', 'xl'],
            'components': ['button', 'input', 'card', 'modal']
        }

# Example usage function
async def analyze_design_for_user_story(text: str, config: Dict[str, Any]) -> Optional[str]:
    """Convenience function to analyze designs for user story enhancement"""
    analyzer = FigmaDesignAnalyzer(config)
    return await analyzer.analyze_design_from_urls(text)

if __name__ == "__main__":
    # Example usage
    config = {
        'figma': {
            'enabled': True,
            'default_file_key': 'example-key'
        }
    }

    text = """
    Create a user story for implementing the new dashboard layout.
    Please check the Figma design at https://www.figma.com/design/ABC123/Dashboard-Design
    and the component library at https://www.figma.com/design/DEF456/Component-Library
    """

    async def main():
        design_context = await analyze_design_for_user_story(text, config)
        if design_context:
            print("Design Context Found:")
            print(design_context)
        else:
            print("No design context found")

    # Note: This would need to be run in an async context
    # asyncio.run(main())
