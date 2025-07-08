import streamlit as st
import asyncio
import os
import json
from datetime import datetime
from typing import Dict, Any

# Import our core modules
from core.freepik_client import FreepikClient
from core.llm_orchestrator import LLMOrchestrator
from core.workflow_engine import WorkflowEngine
from config.settings import get_config
from ui.components.image_gallery import ImageGallery
from ui.components.prompt_enhancer import PromptEnhancer

# Page configuration
st.set_page_config(
    page_title="🎨 Freepik AI Orchestrator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/freepik-ai-orchestrator',
        'Report a bug': 'https://github.com/yourusername/freepik-ai-orchestrator/issues',
        'About': """
        # Freepik AI Orchestrator
        
        Professional AI-powered image generation with LLM optimization.
        Built for consultancies and businesses requiring high-quality AI imagery.
        """
    }
)

# Load custom CSS
def load_css():
    css_path = os.path.join("ui", "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = LLMOrchestrator()
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'user_tier' not in st.session_state:
        st.session_state.user_tier = 'free'  # free, professional, enterprise
    if 'generations_today' not in st.session_state:
        st.session_state.generations_today = 0
    if 'current_workflow' not in st.session_state:
        st.session_state.current_workflow = None

# Main application
def main():
    load_css()
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 Freepik AI Orchestrator</h1>
        <p>Professional AI-powered image generation with LLM optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    setup_sidebar()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 Generate", 
        "📊 Analytics", 
        "🔄 Workflows", 
        "⚙️ Settings"
    ])
    
    with tab1:
        generation_tab()
    
    with tab2:
        analytics_tab()
    
    with tab3:
        workflows_tab()
    
    with tab4:
        settings_tab()

def setup_sidebar():
    """Configure the sidebar with user preferences and settings"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # User tier display
        tier_color = {"free": "🆓", "professional": "💎", "enterprise": "🏢"}
        st.markdown(f"""
        **User Tier:** {tier_color.get(st.session_state.user_tier, '❓')} 
        {st.session_state.user_tier.title()}
        """)
        
        # Usage display for free tier
        if st.session_state.user_tier == 'free':
            progress = min(st.session_state.generations_today / 10, 1.0)
            st.progress(progress)
            st.caption(f"Daily usage: {st.session_state.generations_today}/10")
            
            if st.session_state.generations_today >= 10:
                st.error("🚫 Daily limit reached!")
                if st.button("💳 Upgrade to Professional"):
                    st.info("Redirecting to billing... (Demo)")
        
        st.divider()
        
        # Model preferences
        st.subheader("🤖 Model Preferences")
        model_preference = st.selectbox(
            "Preferred Model",
            ["Auto-Select (Recommended)", "Mystic", "Imagen3", "Flux Dev", "Classic Fast"],
            help="Auto-Select uses LLM to choose the optimal model for your request"
        )
        
        style_preference = st.selectbox(
            "Style Preference",
            ["Auto-Detect", "Photorealistic", "Artistic", "Cinematic", "Technical", "Abstract"]
        )
        
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["Auto", "16:9 (Landscape)", "1:1 (Square)", "9:16 (Portrait)", "4:3", "3:2"]
        )
        
        st.divider()
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            enable_post_processing = st.checkbox("Enable Post-Processing", value=True)
            auto_upscale = st.checkbox("Auto Upscale Results", value=False)
            enable_variations = st.checkbox("Generate Variations", value=False)
            
            st.subheader("Quality Settings")
            quality_level = st.slider("Quality Level", 1, 10, 8)
            creativity_level = st.slider("Creativity Level", 1, 10, 5)
        
        st.divider()
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        if st.button("🔄 Clear Session", help="Clear all generated images"):
            st.session_state.generated_images = []
            st.rerun()
        
        if st.button("📥 Export Results", help="Export generation history"):
            export_results()

def generation_tab():
    """Main image generation interface"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✍️ Describe Your Image")
        
        # Main input area
        user_input = st.text_area(
            "What would you like to create?",
            placeholder="A professional headshot of a confident businesswoman in a modern office setting with natural lighting...",
            height=120,
            help="Be as descriptive as possible. The LLM will optimize your prompt automatically."
        )
        
        # Quick templates
        st.markdown("📝 **Quick Templates:**")
        template_cols = st.columns(4)
        
        templates = {
            "👔 Professional": "Professional headshot of a confident business person, modern office background, natural lighting, sharp focus",
            "📦 Product": "High-quality product photography, clean white background, studio lighting, commercial style",
            "🎨 Artistic": "Digital art masterpiece, creative composition, vibrant colors, artistic style, detailed illustration",
            "📢 Marketing": "Eye-catching marketing banner design, modern layout, professional branding, clean typography"
        }
        
        for i, (name, template) in enumerate(templates.items()):
            with template_cols[i]:
                if st.button(name, key=f"template_{i}", help=template):
                    user_input = template
                    st.rerun()
        
        # Generation controls
        col_gen1, col_gen2 = st.columns([3, 1])
        
        with col_gen1:
            # Check limits for free users
            can_generate = True
            if st.session_state.user_tier == 'free' and st.session_state.generations_today >= 10:
                can_generate = False
            
            generate_button = st.button(
                "🚀 Generate Image", 
                type="primary", 
                disabled=not user_input or not can_generate,
                help="Generate optimized image using AI"
            )
        
        with col_gen2:
            if st.button("🎲 Surprise Me!", disabled=not can_generate):
                surprise_prompts = [
                    "A futuristic cityscape at sunset with flying cars",
                    "A cozy coffee shop interior with warm lighting",
                    "An abstract geometric pattern in vibrant colors",
                    "A minimalist workspace with modern design"
                ]
                user_input = st.selectbox("Choose a surprise:", surprise_prompts)
                st.rerun()
        
        # Process generation
        if generate_button and user_input:
            process_generation(user_input)
    
    with col2:
        st.subheader("🎯 AI Optimization")
        
        if user_input:
            with st.spinner("🤖 Analyzing prompt..."):
                try:
                    # Mock optimization preview for demo
                    optimization = {
                        'enhanced_prompt': f"{user_input}, high quality, professional, detailed",
                        'model': 'mystic',
                        'style': 'balanced',
                        'aspect_ratio': '16:9',
                        'reasoning': 'Balanced approach with enhanced quality descriptors'
                    }
                    
                    st.markdown("**✨ Enhanced Prompt:**")
                    st.code(optimization.get('enhanced_prompt', user_input)[:200] + "...", language=None)
                    
                    st.markdown("**📊 AI Recommendations:**")
                    st.write(f"🤖 **Model:** `{optimization.get('model', 'mystic')}`")
                    st.write(f"🎨 **Style:** `{optimization.get('style', 'auto')}`")
                    st.write(f"📐 **Aspect:** `{optimization.get('aspect_ratio', 'auto')}`")
                    
                    if optimization.get('reasoning'):
                        with st.expander("🧠 AI Reasoning"):
                            st.write(optimization['reasoning'])
                            
                except Exception as e:
                    st.error(f"LLM optimization failed: {str(e)}")
                    st.info("Will proceed with basic optimization")
    
    # Results section
    display_results()

def process_generation(user_input: str):
    """Process the image generation request"""
    try:
        with st.spinner("🎨 Creating your image..."):
            # Mock generation for demo
            result = {
                "task_id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "model_used": "mystic",
                "synchronous": False,
                "image_url": None,
                "status": "pending"
            }
            
            # Update session state
            st.session_state.generated_images.append({
                **result,
                "timestamp": datetime.now(),
                "user_input": user_input
            })
            st.session_state.generations_today += 1
            
            # Show success message
            st.success(f"✅ Generation started! Using {result.get('model_used', 'unknown')} model")
            
            if result.get('synchronous'):
                st.image(result.get('image_url'), caption="Generated Image")
            else:
                st.info("🔄 Your image is being generated. Results will appear below shortly.")
                
    except Exception as e:
        st.error(f"Generation failed: {str(e)}")
        st.info("Please check your API configuration and try again.")

def display_results():
    """Display generated images and their details"""
    if not st.session_state.generated_images:
        st.info("👆 Generate your first image to see results here!")
        return
    
    st.divider()
    st.subheader("🖼️ Your Generated Images")
    
    # Show recent generations
    for i, result in enumerate(reversed(st.session_state.generated_images[-5:])):
        with st.expander(
            f"🎨 Image {len(st.session_state.generated_images) - i} - {result.get('model_used', 'Unknown')}", 
            expanded=i == 0
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if result.get('image_url'):
                    st.image(
                        result['image_url'], 
                        caption=f"Generated with {result.get('model_used', 'Unknown')}",
                        use_column_width=True
                    )
                    
                    # Download button
                    if st.button(f"📥 Download", key=f"download_{i}"):
                        st.info("Download functionality - implement based on your needs")
                else:
                    # Show status for async generations
                    st.info("🔄 Generation in progress...")
                    if st.button(f"🔄 Check Status", key=f"status_{i}"):
                        # Implement status checking
                        st.info("Status checking - implement webhook handling")
            
            with col2:
                st.markdown("**📋 Details:**")
                st.code(f"Task ID: {result.get('task_id', 'N/A')}")
                st.code(f"Model: {result.get('model_used', 'Unknown')}")
                st.code(f"Time: {result.get('timestamp', 'Unknown').strftime('%H:%M:%S') if result.get('timestamp') else 'N/A'}")
                
                # Post-processing options
                if result.get('image_url'):
                    st.markdown("**🔧 Post-Process:**")
                    
                    post_cols = st.columns(2)
                    with post_cols[0]:
                        if st.button("⬆️ Upscale", key=f"upscale_{i}"):
                            st.info("Upscaling feature - implement based on Freepik API")
                    
                    with post_cols[1]:
                        if st.button("💡 Relight", key=f"relight_{i}"):
                            st.info("Relighting feature - implement based on Freepik API")

def analytics_tab():
    """Analytics and usage dashboard"""
    st.subheader("📊 Usage Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Generations", 
            len(st.session_state.generated_images),
            delta=f"+{st.session_state.generations_today} today"
        )
    
    with col2:
        success_rate = 94.2  # Calculate from actual data
        st.metric("Success Rate", f"{success_rate}%", delta="↗️ 2.1%")
    
    with col3:
        avg_time = "45s"  # Calculate from actual data
        st.metric("Avg. Processing Time", avg_time, delta="↘️ 12s")
    
    with col4:
        cost_per_image = "$0.23"  # Calculate from actual usage
        st.metric("Est. Cost/Image", cost_per_image, delta="↘️ $0.05")
    
    # Usage over time chart (placeholder)
    st.subheader("📈 Usage Over Time")
    chart_data = {"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                  "Generations": [5, 8, 12, 6, 15, 20, 10]}
    st.bar_chart(chart_data, x="Day", y="Generations")
    
    # Model usage breakdown
    st.subheader("🤖 Model Usage")
    model_cols = st.columns(4)
    
    models = ["Mystic", "Imagen3", "Flux Dev", "Classic Fast"]
    usage = [45, 30, 20, 5]  # Calculate from actual data
    
    for i, (model, pct) in enumerate(zip(models, usage)):
        with model_cols[i]:
            st.metric(model, f"{pct}%")

def workflows_tab():
    """Workflow templates and automation"""
    st.subheader("🔄 Workflow Templates")
    
    workflows = {
        "👔 Professional Headshots": {
            "description": "Complete pipeline for professional headshots with optimal lighting",
            "steps": ["Generate with Imagen3", "Auto-relight", "Upscale 4x", "Background variants"],
            "estimated_time": "2-3 minutes",
            "cost_estimate": "$1.20"
        },
        "📦 Product Photography": {
            "description": "E-commerce product images with multiple angles and backgrounds",
            "steps": ["Generate with Imagen3", "Remove background", "Multiple lighting", "Angle variants"],
            "estimated_time": "3-4 minutes", 
            "cost_estimate": "$2.50"
        },
        "🎨 Marketing Materials": {
            "description": "Social media and marketing content with brand consistency",
            "steps": ["Generate with Mystic", "Style variations", "Aspect ratio variants", "Brand overlay"],
            "estimated_time": "2-3 minutes",
            "cost_estimate": "$1.80"
        }
    }
    
    for name, workflow in workflows.items():
        with st.expander(name):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(workflow["description"])
                st.markdown("**🔄 Workflow Steps:**")
                for i, step in enumerate(workflow["steps"], 1):
                    st.write(f"{i}. {step}")
            
            with col2:
                st.markdown("**📊 Estimates:**")
                st.write(f"⏱️ Time: {workflow['estimated_time']}")
                st.write(f"💰 Cost: {workflow['cost_estimate']}")
                
                if st.button(f"🚀 Start Workflow", key=f"workflow_{name}"):
                    st.session_state.current_workflow = name
                    st.success(f"Started {name} workflow!")

def settings_tab():
    """Application settings and configuration"""
    st.subheader("⚙️ System Settings")
    
    # API Configuration
    st.markdown("### 🔑 API Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Freepik API**")
        freepik_status = "🟢 Connected" if os.getenv("FREEPIK_API_KEY") else "🔴 Not configured"
        st.write(freepik_status)
        
        st.markdown("**LLM API**")
        llm_status = "🟢 Connected" if (os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")) else "🔴 Not configured"
        st.write(llm_status)
    
    with col2:
        st.markdown("**Webhook**")
        webhook_status = "🟢 Active" if os.getenv("FREEPIK_WEBHOOK_URL") else "🔴 Not configured"
        st.write(webhook_status)
        
        st.markdown("**Database**")
        db_status = "🟢 Connected" if os.getenv("DATABASE_URL") else "🔴 Not configured"
        st.write(db_status)

def export_results():
    """Export generation results"""
    if st.session_state.generated_images:
        # Create export data
        export_data = []
        for img in st.session_state.generated_images:
            export_data.append({
                "timestamp": img.get("timestamp", "").isoformat() if img.get("timestamp") else "",
                "user_input": img.get("user_input", ""),
                "model_used": img.get("model_used", ""),
                "task_id": img.get("task_id", ""),
                "image_url": img.get("image_url", "")
            })
        
        # Convert to JSON for download
        json_str = json.dumps(export_data, indent=2, default=str)
        
        st.download_button(
            label="📥 Download Generation History",
            data=json_str,
            file_name=f"freepik_generations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
