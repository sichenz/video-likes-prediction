# video-likes-prediction

This is a video embedding/features extraction and prediction model framework designed for Professor Xiao Liu's class. This guide provides step-by-step instructions to help you set up and run the file on your local machine.


## Requirements

- Python 3.8+
- Conda environment

## Steps

### Step 1: Sort Competing Programs
1. Organize the `Competing Programs` directory.
2. Retain only the `.csv` file containing video likes information.

### Step 2: Extract Videos
1. Download the Red folder (or any video folder with .mov, .mp4, etc)
2. Run `extract.py`.
2. Extract all videos from the organized folders into `videos` folder.

### Step 3: Generate Physical Feature Embeddings
1. Run `embedding.ipynb`.
2. Generate and save the physical features to a `video_features.csv` file.

### Step 4: Create Prediction Model Using Physical Features
1. Open `features.ipynb`.
2. Load the `video_features.csv` file of physical features.
3. Train a prediction model.

### Step 5: Deploy the Prediction Model
1. Run `App.py` using Streamlit.
```bash
streamlit run app.py
```
2. Interact with the prediction model through the application.

### Step 6: Generate Numerical Embeddings
1. Run `embed2.ipynb`.
2. Process the extracted videos.
3. Generate and save numerical embeddings to a `video_embeddings.csv` file.

### Step 7: Create Prediction Model Using Numerical Embeddings
1. Open `predict.ipynb`.
2. Load the `video_embeddings.csv` file of numerical embeddings.
3. Train a prediction model using the extracted features.
