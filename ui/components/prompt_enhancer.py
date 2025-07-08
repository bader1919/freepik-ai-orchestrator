"""Prompt enhancement component for the Freepik AI Orchestrator"""

import streamlit as st
from typing import Dict, Any, List

class PromptEnhancer:
    """Component for interactive prompt enhancement"""
    
    @staticmethod
    def display_enhancement_interface(initial_prompt: str = "") -> Dict[str, Any]:
        """Display interactive prompt enhancement interface"""
        
        st.subheader("✨ Prompt Enhancement Studio")
        
        # Main prompt input
        prompt = st.text_area(
            "Base Prompt",
            value=initial_prompt,
            placeholder="Describe your image...",
            height=100
        )
        
        # Enhancement options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎨 Style Modifiers**")
            
            style_categories = {
                "Photography": ["professional photography", "portrait photography", "commercial photography", "street photography"],
                "Artistic": ["digital art", "concept art", "illustration", "painting style"],
                "Cinematic": ["cinematic lighting", "movie still", "dramatic composition", "film noir"],
                "Technical": ["architectural visualization", "technical illustration", "blueprint style", "isometric view"]
            }
            
            selected_styles = []
            for category, styles in style_categories.items():
                with st.expander(category):
                    for style in styles:
                        if st.checkbox(style, key=f"style_{style}"):
                            selected_styles.append(style)
        
        with col2:
            st.markdown("**🔧 Technical Modifiers**")
            
            technical_options = {
                "Quality": ["ultra-detailed", "high resolution", "sharp focus", "professional quality"],
                "Lighting": ["natural lighting", "studio lighting", "golden hour", "dramatic lighting"],
                "Composition": ["rule of thirds", "shallow depth of field", "wide angle", "close-up"],
                "Camera": ["shot on Canon 5D", "85mm lens", "macro photography", "telephoto lens"]
            }
            
            selected_technical = []
            for category, options in technical_options.items():
                with st.expander(category):
                    for option in options:
                        if st.checkbox(option, key=f"tech_{option}"):
                            selected_technical.append(option)
        
        # Advanced settings
        with st.expander("🔬 Advanced Settings"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                creativity_level = st.slider("Creativity Level", 0.0, 1.0, 0.5, 0.1)
                detail_level = st.slider("Detail Level", 0.0, 1.0, 0.7, 0.1)
            
            with col_adv2:
                realism_level = st.slider("Realism Level", 0.0, 1.0, 0.8, 0.1)
                artistic_freedom = st.slider("Artistic Freedom", 0.0, 1.0, 0.6, 0.1)
        
        # Generate enhanced prompt
        if st.button("🚀 Generate Enhanced Prompt"):
            enhanced_prompt = PromptEnhancer._generate_enhanced_prompt(
                prompt, selected_styles, selected_technical, {
                    "creativity": creativity_level,
                    "detail": detail_level,
                    "realism": realism_level,
                    "artistic_freedom": artistic_freedom
                }
            )
            
            st.markdown("**✨ Enhanced Prompt:**")
            st.code(enhanced_prompt, language=None)
            
            return {
                "original_prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "modifiers": {
                    "styles": selected_styles,
                    "technical": selected_technical
                },
                "settings": {
                    "creativity": creativity_level,
                    "detail": detail_level,
                    "realism": realism_level,
                    "artistic_freedom": artistic_freedom
                }
            }
        
        return {
            "original_prompt": prompt,
            "enhanced_prompt": prompt,
            "modifiers": {"styles": selected_styles, "technical": selected_technical}
        }
    
    @staticmethod
    def _generate_enhanced_prompt(base_prompt: str, styles: List[str], 
                                technical: List[str], settings: Dict[str, float]) -> str:
        """Generate enhanced prompt from components"""
        
        enhanced_parts = [base_prompt]
        
        # Add style modifiers
        if styles:
            style_text = ", ".join(styles)
            enhanced_parts.append(style_text)
        
        # Add technical modifiers
        if technical:
            tech_text = ", ".join(technical)
            enhanced_parts.append(tech_text)
        
        # Add quality modifiers based on settings
        quality_terms = []
        
        if settings.get("detail", 0) > 0.7:
            quality_terms.extend(["highly detailed", "intricate details"])
        elif settings.get("detail", 0) > 0.4:
            quality_terms.append("detailed")
        
        if settings.get("realism", 0) > 0.8:
            quality_terms.extend(["photorealistic", "lifelike"])
        elif settings.get("realism", 0) > 0.5:
            quality_terms.append("realistic")
        
        if settings.get("creativity", 0) > 0.7:
            quality_terms.extend(["creative", "imaginative", "unique"])
        
        if quality_terms:
            enhanced_parts.append(", ".join(quality_terms))
        
        return ", ".join(enhanced_parts)
    
    @staticmethod
    def display_prompt_templates():
        """Display prompt template library"""
        
        st.subheader("📚 Prompt Template Library")
        
        templates = {
            "Professional Headshots": {
                "template": "Professional headshot of {subject}, {attire}, {background}, natural lighting, shot with Canon 5D Mark IV, 85mm lens, shallow depth of field, high resolution, sharp focus",
                "variables": ["subject", "attire", "background"],
                "example": "Professional headshot of confident businesswoman, dark business suit, modern office background, natural lighting, shot with Canon 5D Mark IV, 85mm lens, shallow depth of field, high resolution, sharp focus"
            },
            
            "Product Photography": {
                "template": "{product} product photography, {background}, {lighting}, commercial style, high quality, detailed, professional advertising photo, {camera_settings}",
                "variables": ["product", "background", "lighting", "camera_settings"],
                "example": "Luxury watch product photography, clean white background, studio lighting, commercial style, high quality, detailed, professional advertising photo, macro lens"
            },
            
            "Artistic Concepts": {
                "template": "{style} artwork of {subject}, {mood}, {color_palette}, {artistic_technique}, creative composition, detailed illustration, high resolution digital art",
                "variables": ["style", "subject", "mood", "color_palette", "artistic_technique"],
                "example": "Digital art artwork of futuristic cityscape, moody atmosphere, neon color palette, concept art technique, creative composition, detailed illustration, high resolution digital art"
            }
        }
        
        selected_template = st.selectbox("Choose a template", list(templates.keys()))
        
        if selected_template:
            template_data = templates[selected_template]
            
            st.markdown("**Template Structure:**")
            st.code(template_data["template"], language=None)
            
            st.markdown("**Variables to customize:**")
            for var in template_data["variables"]:
                st.write(f"• `{{{var}}}`")
            
            st.markdown("**Example:**")
            st.info(template_data["example"])
            
            if st.button(f"Use {selected_template} Template"):
                return template_data["template"]
        
        return None
