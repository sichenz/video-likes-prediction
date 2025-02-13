# video-likes-prediction

This is a video embedding/features extraction and prediction model framework. This guide provides step-by-step instructions to help you set up and run the file on your local machine.


## Requirements

- Python 3.8+
- Conda environment

## Steps

### Step 1: Compile Webscraped Post Data 
1. Retain only the `.csv` file containing video likes information.
2. Name it `video_sheet.csv`.

### Step 2: Extract Videos (Do this step only if your data folder has mixed files in it)
1. Run `extract.py`.
2. Extract all videos from the organized folders into `videos` folder.

### Step 3: Generate Physical Features and Embeddings
1. Run `embeddings_and_features.ipynb`.
2. Generate and save all features into a combined `video_info.csv` file.

### Step 4: Deploy the Prediction Model
1. Run `prediction_using_embeddings.ipynb`.
2. Run `prediction_using_features.ipynb`.

### Step 5: Run Prediction Model Using Features
1. Run `App.py` using Streamlit.
```bash
streamlit run app.py
```
2. Interact with the prediction model through the application.
