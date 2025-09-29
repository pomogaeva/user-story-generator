#!/usr/bin/env python3
"""
Prompt Enhancer for Design-Informed User Story Generation

This module enhances user story generation prompts with design context
extracted from Figma designs using the FigmaDesignAnalyzer.
"""

import re
from typing import Dict, List, Optional, Any
from figma_design_analyzer import FigmaDesignAnalyzer, DesignRequirements


class PromptEnhancer:
    """Enhances user story generation prompts with design context"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.design_analyzer = FigmaDesignAnalyzer(config)

    def extract_feature_description(self, user_prompt: str) -> str:
        """Extract the core feature description from user prompt"""
        # Remove metadata like fix versions, severity, etc.
        clean_prompt = re.sub(r'Fix versions:[\s\S]*?(\n\n|\Z)', '', user_prompt)
        clean_prompt = re.sub(r'QC Severity:[\s\S]*?(\n\n|\Z)', '', clean_prompt)
        clean_prompt = re.sub(r'Issue type:[\s\S]*?(\n\n|\Z)', '', clean_prompt)

        return clean_prompt.strip()

    def build_design_context_prompt(self, design_requirements: DesignRequirements) -> str:
        """Build design context section for the prompt"""
        context_parts = []

        if design_requirements.components:
            context_parts.append("## Available Design Components")
            for component in design_requirements.components[:10]:  # Limit to avoid token limits
                props = []
                if 'width' in component.properties:
                    props.append(f"width: {component.properties['width']}")
                if 'height' in component.properties:
                    props.append(f"height: {component.properties['height']}")
                if component.properties.get('backgroundColor'):
                    props.append(f"background: {component.properties['backgroundColor']}")

                props_str = f" ({', '.join(props)})" if props else ""
                context_parts.append(f"- **{component.name}** ({component.type}){props_str}")

        if design_requirements.interaction_patterns:
            context_parts.append("\n## Interaction Patterns from Design")
            for pattern in design_requirements.interaction_patterns[:5]:
                context_parts.append(f"- {pattern}")

        if design_requirements.constraints:
            context_parts.append("\n## Design Constraints")
            for constraint in design_requirements.constraints[:5]:
                context_parts.append(f"- {constraint}")

        if design_requirements.accessibility_notes:
            context_parts.append("\n## Accessibility Requirements from Design")
            for note in design_requirements.accessibility_notes[:3]:
                context_parts.append(f"- {note}")

        return "\n".join(context_parts)

    def enhance_user_story_prompt(self, user_prompt: str, design_context: Optional[str] = None) -> str:
        """Enhance the user story generation prompt with design context"""

        base_prompt = f"""
You are creating a comprehensive user story following ShortPoint's template structure.

USER REQUEST: {user_prompt}

IMPORTANT REQUIREMENTS:
1. **Title Format**: Use `[Feature]` tag format (e.g., `[Dashboard] Implement New Layout`)
2. **Template Structure**: Follow the exact template format with all sections
3. **Design Integration**: If design information is provided, incorporate it into appropriate sections
4. **Specificity**: Be specific about components, interactions, and visual requirements
5. **Testing**: Include design-specific testing requirements

"""

        if design_context:
            base_prompt += f"""
DESIGN CONTEXT AVAILABLE:
{design_context}

INSTRUCTIONS FOR DESIGN INTEGRATION:
- Reference specific components from the design context in the DESIGN section
- Include design patterns and interaction requirements in FUNCTIONAL DETAILS
- Add design system validation to TESTING & VALIDATION
- Ensure all design constraints are documented in SPECIAL CASES/EDGE CASES
- Make accessibility requirements from design explicit in ERROR HANDLING and TESTING

"""

        base_prompt += """
GENERATE A COMPLETE USER STORY:
Include all template sections with detailed, actionable content.
Focus on user value, clear acceptance criteria, and comprehensive testing requirements.
If design context is available, ensure the story reflects the design specifications accurately.
"""

        return base_prompt.strip()

    def create_refinement_prompt(self, current_story: str, refinement_request: str, design_context: Optional[str] = None) -> str:
        """Create a prompt for refining an existing story with design context"""

        prompt = f"""
You need to refine the following user story based on new requirements.

CURRENT STORY:
{current_story}

REFINEMENT REQUEST: {refinement_request}
"""

        if design_context:
            prompt += f"""

ADDITIONAL DESIGN CONTEXT:
{design_context}

When refining:
- Update DESIGN section to reflect any new design components or patterns
- Modify FUNCTIONAL DETAILS to align with design specifications
- Update TESTING & VALIDATION with design-specific testing requirements
- Ensure design constraints are properly documented

"""

        prompt += """
Provide the complete updated user story following the ShortPoint template structure.
Maintain consistency with existing content while incorporating the requested changes and design context.
"""

        return prompt.strip()

    async def process_user_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """Process a user prompt and return enhanced prompt with design context"""

        # Extract feature description
        feature_description = self.extract_feature_description(user_prompt)

        # Analyze designs from the prompt
        design_context = await self.design_analyzer.analyze_design_from_urls(user_prompt)

        # Build enhanced prompt
        enhanced_prompt = self.enhance_user_story_prompt(feature_description, design_context)

        return {
            'original_prompt': user_prompt,
            'feature_description': feature_description,
            'design_context': design_context,
            'enhanced_prompt': enhanced_prompt
        }

    def get_design_system_context(self) -> str:
        """Get design system context for prompt enhancement"""
        design_system = self.design_analyzer.get_design_system_info()

        if not design_system:
            return ""

        context_parts = ["## Design System Context"]

        for category, items in design_system.items():
            context_parts.append(f"**{category.title()}:** {', '.join(items)}")

        return "\n".join(context_parts)


def create_enhanced_user_story_prompt(user_prompt: str, config: Dict[str, Any]) -> str:
    """Convenience function to create enhanced prompt"""
    enhancer = PromptEnhancer(config)
    import asyncio

    async def _create_prompt():
        result = await enhancer.process_user_prompt(user_prompt)
        return result['enhanced_prompt']

    # For synchronous usage, return a basic prompt if no design context
    try:
        return asyncio.run(_create_prompt())
    except:
        # Fallback for environments without async support
        return PromptEnhancer(config).enhance_user_story_prompt(
            PromptEnhancer(config).extract_feature_description(user_prompt)
        )


# Example usage
if __name__ == "__main__":
    config = {
        'figma': {
            'enabled': True,
            'default_file_key': 'example-key'
        }
    }

    user_prompt = """
    Create a user story for implementing a new dashboard with improved navigation.
    Please check the Figma design at https://www.figma.com/design/ABC123/Dashboard-Design
    and use the component library from https://www.figma.com/design/DEF456/Component-Library.
    Fix versions: 8.9.0, QC Severity: Medium
    """

    enhanced_prompt = create_enhanced_user_story_prompt(user_prompt, config)
    print("Enhanced Prompt:")
    print(enhanced_prompt)
