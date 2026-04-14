import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
import json


# Full-width page with custom theme
st.set_page_config(
    page_title="RAG Application", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 10px;
        color: White;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-title h1 {
        margin: 0;
        font-size: 2.5em;
    }
    
    /* Info card styling */
    .info-card {
        background: Blackrmdir /s /q .git;
        padding: 20px;
        border-left: 5px solid #667eea;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Success message styling */
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* File details container */
    .file-details {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-top: 20px;
    }
    
    /* Metadata section */
    .metadata-section {
        background: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        border: 1px solid #e8e8e8;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.markdown("### 📖 About RAG")
    st.info(
        "**Retrieval-Augmented Generation (RAG)** combines retrieval and generation "
        "to provide AI responses grounded in real documents and data sources. "
        "Upload files to extract metadata and enhance your RAG pipeline!"
    )
    st.markdown("---")
    st.markdown("### 📁 Supported Formats")
    st.markdown("""
    - **Images**: PNG, JPG, JPEG
    - **Documents**: PDF, DOCX, TXT
    """)

# Main header with gradient
st.markdown('<div class="main-title"><h1>📚 RAG Application</h1></div>', unsafe_allow_html=True)

# Info section
st.markdown('<div class="info-card"><h4>What is RAG?</h4>'
            '<p>Retrieval-Augmented Generation (RAG) is an AI framework that improves '
            'Large Language Model (LLM) accuracy by retrieving data from external, trusted '
            'sources—like company documents or databases—before generating a response.</p></div>', 
            unsafe_allow_html=True)


# Upload section with better styling
st.markdown("---")
st.markdown("### 📤 Upload Your File")
st.markdown("Upload any file below to extract metadata and use in your RAG application.")

# Upload file in centered layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=None,
        help="Supports images (PNG, JPG), PDFs, DOCX files, and text files"
    )

image_types = ["image/png", "image/jpeg", "image/jpg"]

doc_types = [
    "text/plain",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

# Show file details
if uploaded_file is not None:
    st.markdown('<div class="success-message">✅ <strong>File uploaded successfully!</strong></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 📋 File Details")
        
        # File metrics in columns
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="📄 File Name", value=uploaded_file.name)
        with metric_col2:
            st.metric(label="🏷️ File Type", value=uploaded_file.type or "Unknown")
        with metric_col3:
            st.metric(label="💾 File Size", value=f"{uploaded_file.size / 1024:.2f} KB")
    
    st.markdown("---")
    
    # Image metadata
    if uploaded_file.type.startswith("image"):
        with st.container():
            st.markdown("### 🖼️ Image Metadata")
            
            image = Image.open(uploaded_file)
            
            # Display image
            col1, col2 = st.columns([2, 1])
            with col1:
                st.image(image, use_column_width=True)
            
            # Image properties
            with col2:
                st.markdown('<div class="metadata-section">', unsafe_allow_html=True)
                st.write(f"**Format:** {image.format}")
                st.write(f"**Mode:** {image.mode}")
                st.write(f"**Dimensions:** {image.size[0]}×{image.size[1]} px")
                
                # EXIF data
                exif_data = image.getexif()
                if exif_data:
                    with st.expander("📸 EXIF Data"):
                        for key, value in exif_data.items():
                            st.write(f"**{key}:** {value}")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # DOCX metadata
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        st.markdown("### 📝 Document Metadata")
        with st.container():
            st.markdown('<div class="metadata-section">', unsafe_allow_html=True)
            
            doc = Document(uploaded_file)
            core_props = doc.core_properties
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Author:** {core_props.author or 'Not specified'}")
                st.write(f"**Created:** {core_props.created or 'Not specified'}")
            with col2:
                st.write(f"**Last Modified By:** {core_props.last_modified_by or 'Not specified'}")
                st.write(f"**Subject:** {core_props.subject or 'Not specified'}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # PDF metadata
    elif uploaded_file.type == "application/pdf":
        st.markdown("### 📕 PDF Metadata")
        with st.container():
            st.markdown('<div class="metadata-section">', unsafe_allow_html=True)
            
            reader = PdfReader(uploaded_file)
            metadata = reader.metadata
            
            if metadata:
                for key, value in metadata.items():
                    st.write(f"**{key}:** {value}")
            else:
                st.info("No metadata found in this PDF.")
            
            st.write(f"**Total Pages:** {len(reader.pages)}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Save file data to JSON
    st.markdown("---")
    data = {
        "file_name": uploaded_file.name,
        "file_type": uploaded_file.type,
        "file_size": round(uploaded_file.size / 1024, 2),
    }
    
    with open("data_store.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
    
    st.success("✅ File information saved to database!")
else:
    # Empty state
    st.markdown("---")
    st.info("👆 Upload a file to see its metadata and details")

