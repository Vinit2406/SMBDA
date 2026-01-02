!pip install streamlit wordcloud matplotlib pandas

import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Set page configuration
st.set_page_config(page_title="Word Cloud Generator", layout="wide")

# Title
st.title("📊 Word Cloud Analysis Dashboard")

# User input for topic name
topic_name = st.text_input("Enter Topic Name:", placeholder="e.g., Technology Trends, Marketing Analysis")

# Create 3 tabs
tab1, tab2, tab3 = st.tabs(["📝 Text Input", "☁️ Word Cloud", "📈 Word Frequency"])

# Tab 1: Text Input
with tab1:
    st.header("Enter Your Text Data")
    
    # Text area for user input
    user_text = st.text_area(
        "Paste your text here (minimum 500 words recommended):",
        height=300,
        placeholder="Enter or paste your text content here..."
    )
    
    # Display word count
    if user_text:
        word_count = len(user_text.split())
        st.info(f"Current word count: **{word_count}** words")
        
        if word_count < 500:
            st.warning("⚠️ You have less than 500 words. Add more text for better word cloud visualization.")
    
    # Optional: File upload
    uploaded_file = st.file_uploader("Or upload a text file:", type=['txt'])
    if uploaded_file:
        user_text = uploaded_file.read().decode('utf-8')
        st.success(f"File uploaded! Word count: {len(user_text.split())}")

# Tab 2: Word Cloud
with tab2:
    st.header(f"Word Cloud Visualization{': ' + topic_name if topic_name else ''}")
    
    if user_text:
        # Limit to 500 words if more
        words_list = user_text.split()[:500]
        text_500 = ' '.join(words_list)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5
        ).generate(text_500)
        
        # Display word cloud
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(f'Word Cloud - {topic_name}' if topic_name else 'Word Cloud', 
                     fontsize=20, fontweight='bold')
        st.pyplot(fig)
        
        st.success(f"✅ Word cloud generated from {len(words_list)} words")
        
        # Download option
        if st.button("💾 Save Word Cloud"):
            wordcloud.to_file(f"wordcloud_{topic_name.replace(' ', '_') if topic_name else 'output'}.png")
            st.success("Word cloud saved successfully!")
    else:
        st.info("👈 Please enter text in the 'Text Input' tab to generate word cloud")

# Tab 3: Word Frequency Analysis
with tab3:
    st.header(f"Word Frequency Analysis{': ' + topic_name if topic_name else ''}")
    
    if user_text:
        # Get first 500 words
        words_list = user_text.lower().split()[:500]
        
        # Count word frequency
        word_freq = Counter(words_list)
        top_words = word_freq.most_common(20)
        
        # Create DataFrame
        df_freq = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        
        # Display as table
        st.subheader("Top 20 Most Frequent Words")
        st.dataframe(df_freq, use_container_width=True)
        
        # Bar chart
        st.subheader("Frequency Distribution")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(df_freq['Word'][:15], df_freq['Frequency'][:15], color='steelblue')
        ax.set_xlabel('Frequency', fontsize=12)
        ax.set_ylabel('Words', fontsize=12)
        ax.set_title('Top 15 Words by Frequency', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        st.pyplot(fig)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Words Analyzed", len(words_list))
        with col2:
            st.metric("Unique Words", len(set(words_list)))
        with col3:
            st.metric("Most Common Word", top_words[0][0] if top_words else "N/A")
    else:
        st.info("👈 Please enter text in the 'Text Input' tab to see analysis")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ Instructions")
    st.markdown("""
    1. **Enter Topic Name** at the top
    2. **Tab 1**: Paste your text (500+ words)
    3. **Tab 2**: View word cloud visualization
    4. **Tab 3**: Analyze word frequency
    
    **Tips:**
    - More words = Better visualization
    - Upload .txt files for convenience
    - Word cloud uses first 500 words
    """)
    
    if topic_name:
        st.success(f"Current Topic: **{topic_name}**")
