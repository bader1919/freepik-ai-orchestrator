"""UI components for the Freepik AI Orchestrator"""

import streamlit as st
from typing import List, Dict, Any

class ImageGallery:
    """Streamlit component for displaying image galleries"""
    
    @staticmethod
    def display_image_grid(images: List[Dict[str, Any]], columns: int = 3):
        """Display images in a responsive grid"""
        
        if not images:
            st.info("No images to display")
            return
        
        # Create columns
        cols = st.columns(columns)
        
        for i, image_data in enumerate(images):
            col_idx = i % columns
            
            with cols[col_idx]:
                ImageGallery._display_single_image(image_data, i)
    
    @staticmethod
    def _display_single_image(image_data: Dict[str, Any], index: int):
        """Display a single image with metadata"""
        
        # Image display
        if image_data.get("image_url"):
            st.image(
                image_data["image_url"],
                caption=f"Image {index + 1} - {image_data.get('model_used', 'Unknown')}",
                use_column_width=True
            )
        else:
            st.info(f"Image {index + 1} - Processing...")
        
        # Metadata
        with st.expander("Details", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.caption(f"**Model:** {image_data.get('model_used', 'N/A')}")
                st.caption(f"**Status:** {image_data.get('status', 'Unknown')}")
            
            with col2:
                st.caption(f"**Time:** {image_data.get('timestamp', 'N/A')}")
                st.caption(f"**Task ID:** {image_data.get('task_id', 'N/A')[:8]}...")
        
        # Action buttons
        button_cols = st.columns(3)
        
        with button_cols[0]:
            if st.button("💾", key=f"save_{index}", help="Save image"):
                ImageGallery._save_image(image_data)
        
        with button_cols[1]:
            if st.button("🔄", key=f"regenerate_{index}", help="Regenerate"):
                ImageGallery._regenerate_image(image_data)
        
        with button_cols[2]:
            if st.button("✨", key=f"enhance_{index}", help="Enhance"):
                ImageGallery._enhance_image(image_data)
    
    @staticmethod
    def _save_image(image_data: Dict[str, Any]):
        """Handle image saving"""
        if image_data.get("image_url"):
            st.success("Image saved! (Implement actual saving logic)")
        else:
            st.error("No image URL available")
    
    @staticmethod
    def _regenerate_image(image_data: Dict[str, Any]):
        """Handle image regeneration"""
        st.info("Regenerating image... (Implement regeneration logic)")
    
    @staticmethod
    def _enhance_image(image_data: Dict[str, Any]):
        """Handle image enhancement"""
        st.info("Enhancing image... (Implement enhancement logic)")
    
    @staticmethod
    def display_comparison_view(images: List[Dict[str, Any]]):
        """Display images in comparison view"""
        
        if len(images) < 2:
            st.warning("Need at least 2 images for comparison")
            return
        
        st.subheader("🔍 Image Comparison")
        
        # Image selection
        col1, col2 = st.columns(2)
        
        image_options = [f"Image {i+1} - {img.get('model_used', 'Unknown')}" 
                        for i, img in enumerate(images)]
        
        with col1:
            selected_1 = st.selectbox("Select first image", image_options, key="compare_1")
            idx_1 = image_options.index(selected_1)
            if images[idx_1].get("image_url"):
                st.image(images[idx_1]["image_url"], caption="Image 1")
            
        with col2:
            selected_2 = st.selectbox("Select second image", image_options, key="compare_2")
            idx_2 = image_options.index(selected_2)
            if images[idx_2].get("image_url"):
                st.image(images[idx_2]["image_url"], caption="Image 2")
        
        # Comparison metrics
        st.subheader("📊 Comparison Metrics")
        
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.markdown("**Image 1 Details:**")
            st.write(f"Model: {images[idx_1].get('model_used', 'N/A')}")
            st.write(f"Prompt: {images[idx_1].get('user_input', 'N/A')[:50]}...")
            
        with metrics_col2:
            st.markdown("**Image 2 Details:**")
            st.write(f"Model: {images[idx_2].get('model_used', 'N/A')}")
            st.write(f"Prompt: {images[idx_2].get('user_input', 'N/A')[:50]}...")
