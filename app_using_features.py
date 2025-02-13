# app.py

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ===========================
# 1. Download NLTK Data
# ===========================
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# ===========================
# 2. Load Preprocessing Objects and Model
# ===========================
@st.cache_resource
def load_models():
    try:
        model = joblib.load(f'models/video_feature_model.pkl')
        scaler = joblib.load(f'models/scaler.pkl')
        tfidf_vectorizer = joblib.load(f'models/tfidf_vectorizer.pkl')
        le_codec = joblib.load(f'models/label_encoder_codec.pkl')
        feature_names = joblib.load(f'models/feature_names.pkl')
        return model, scaler, tfidf_vectorizer, le_codec, feature_names
    except FileNotFoundError as e:
        st.error(f"Error loading model or preprocessing files: {e}")
        st.stop()

model, scaler, tfidf_vectorizer, le_codec, feature_names = load_models()

# ===========================
# 3. Prediction Function
# ===========================
def predict_likes(model, scaler, tfidf_vectorizer, le_codec, feature_names,
                 duration_seconds, fps, width, height, num_frames, file_size_MB,
                 audio_fps, audio_channels, publish_time,
                 codec, has_audio, title):
    """
    Predict the number of likes for a video based on its features.
    """
    # Handle publish_time
    try:
        publish_datetime = pd.to_datetime(publish_time, format='%m/%d/%Y')
    except:
        publish_datetime = pd.to_datetime('2000-01-01')
    
    publish_year = publish_datetime.year
    publish_month = publish_datetime.month
    publish_day = publish_datetime.day
    publish_dayofweek = publish_datetime.dayofweek
    publish_hour = 12  # Default value as time is not provided
    
    # Encode 'codec'
    if codec in le_codec.classes_:
        codec_encoded = le_codec.transform([codec])[0]
    else:
        # Assign the mode or a default value if codec is unknown
        codec_encoded = le_codec.transform([le_codec.classes_[0]])[0]
        st.warning(f"Codec '{codec}' not recognized. Assigning default codec encoding.")
    
    # Clean and process title
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    title_clean = clean_text(title)
    
    # Remove stopwords and lemmatize
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    def preprocess_text(text):
        tokens = text.split()
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    
    title_processed = preprocess_text(title_clean)
    
    # TF-IDF Vectorization
    tfidf_vector = tfidf_vectorizer.transform([title_processed])
    tfidf_features = pd.DataFrame(tfidf_vector.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    
    # Combine all features into a single DataFrame
    input_data = pd.DataFrame({
        'duration_seconds': [duration_seconds],
        'fps': [fps],
        'width': [width],
        'height': [height],
        'num_frames': [num_frames],
        'file_size_MB': [file_size_MB],
        'audio_fps': [audio_fps],
        'audio_channels': [audio_channels],
        'publish_year': [publish_year],
        'publish_month': [publish_month],
        'publish_day': [publish_day],
        'publish_dayofweek': [publish_dayofweek],
        'publish_hour': [publish_hour],
        'codec_encoded': [codec_encoded],
        'has_audio': [has_audio],
        'title_processed': [title_processed]
    })
    
    # Scale numerical features
    numerical_features = ['duration_seconds', 'fps', 'width', 'height', 'num_frames',
                          'file_size_MB', 'audio_fps', 'audio_channels',
                          'publish_year', 'publish_month', 'publish_day',
                          'publish_dayofweek', 'publish_hour']
    input_data[numerical_features] = scaler.transform(input_data[numerical_features])
    
    # TF-IDF features are already in tfidf_features
    # Concatenate TF-IDF features
    input_data = pd.concat([input_data, tfidf_features], axis=1)
    
    # Drop 'title_processed' as it's already vectorized
    input_data = input_data.drop(['title_processed'], axis=1)
    
    # Reorder columns to match training
    input_data = input_data.reindex(columns=feature_names, fill_value=0)
    
    # Check for any missing features
    missing_features = set(feature_names) - set(input_data.columns)
    if missing_features:
        st.warning(f"Missing features {missing_features}. Filling with zeros.")
        for feature in missing_features:
            input_data[feature] = 0
    
    # Ensure the order matches
    input_data = input_data[feature_names]
    
    # Predict
    predicted_likes = model.predict(input_data)[0]
    
    return predicted_likes

# ===========================
# 4. Streamlit User Interface
# ===========================
st.title("🎥 Video Like Prediction App")

st.write("""
### Predict the Number of Likes Your Video Might Receive
Fill in the details below to get an estimated like count for your video.
""")

# Input Fields within a Form
with st.form("video_features_form"):
    st.header("Video Features")
    
    duration_seconds = st.number_input("Duration (seconds)", min_value=0.0, value=150.0, step=0.1)
    fps = st.number_input("Frames Per Second (FPS)", min_value=0.0, value=25.0, step=0.1)
    width = st.number_input("Video Width (pixels)", min_value=0, value=1280, step=10)
    height = st.number_input("Video Height (pixels)", min_value=0, value=720, step=10)
    num_frames = st.number_input("Number of Frames", min_value=0, value=3750, step=1)
    file_size_MB = st.number_input("File Size (MB)", min_value=0.0, value=10.0, step=0.1)
    audio_fps = st.number_input("Audio Sampling Rate (Hz)", min_value=0.0, value=48000.0, step=100.0)
    audio_channels = st.number_input("Number of Audio Channels", min_value=1, value=2, step=1)
    publish_time = st.text_input("Publish Time (MM/DD/YYYY)", value="10/19/2023")
    codec = st.selectbox("Codec", options=le_codec.classes_)
    has_audio = st.selectbox("Has Audio", options=[0, 1])
    title = st.text_input("Video Title", value="新学期欢迎活动🎉📚")
    
    submit_button = st.form_submit_button(label='Predict Likes')

if submit_button:
    try:
        predicted_likes = predict_likes(
            model=model,
            scaler=scaler,
            tfidf_vectorizer=tfidf_vectorizer,
            le_codec=le_codec,
            feature_names=feature_names,
            duration_seconds=duration_seconds,
            fps=fps,
            width=width,
            height=height,
            num_frames=num_frames,
            file_size_MB=file_size_MB,
            audio_fps=audio_fps,
            audio_channels=audio_channels,
            publish_time=publish_time,
            codec=codec,
            has_audio=has_audio,
            title=title
        )
        
        st.success(f"**Predicted Likes:** {predicted_likes:.2f}")
    except Exception as e:
        st.error(f"Error in prediction: {e}")
