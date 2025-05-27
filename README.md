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
2. Extract all videos from the organized folders into the `videos` folder.

### Step 3: Generate Physical Features, Embeddings, and ASR
1. Run `video_likes.ipynb`.
2. Generate and save all features into a combined `combined.csv` file.
3. Deploy a prediction model that will use all three of these video characteristics.

**NOTE**: `video_likes.ipynb` was computed on the NYU Greene Cluster. Please see `JUPYTER.md` for details.

### Step 4: Deploy Specific Prediction Models
1. Run `prediction_using_embeddings.ipynb` to deploy a prediction model based on embeddings.
2. Run `prediction_using_features.ipynb` to deploy a prediction model based on features.

### Step 5: Run Prediction Model Using Features
1. Run `app_using_features.py` using Streamlit.
```bash
streamlit run app_using_features.py
```
2. Interact with the prediction model through the application.
