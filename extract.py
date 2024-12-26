import os
import shutil

# -------------------- Configuration -------------------- #

MAIN_FOLDER = "/Users/princess/Documents/RA/video-likes-prediction/Red_new"  # Replace with your main folder path
DESTINATION_FOLDER = "/Users/princess/Documents/RA/video-likes-prediction/videos_new"  # Replace with your destination folder path
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv')
# --------------------------------------------------------- #

def extract_and_rename_videos(main_folder, destination_folder, video_extensions):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    print(f"Destination folder is set to: {destination_folder}")

    for item in os.listdir(main_folder):
        item_path = os.path.join(main_folder, item)

        # Check if the item is a directory
        if os.path.isdir(item_path):
            folder_name = item  
            print(f"\nProcessing folder: {folder_name}")

            # List all files in the subfolder
            files = os.listdir(item_path)
            video_files = [f for f in files if f.lower().endswith(video_extensions)]

            if not video_files:
                print(f"  No video files found in folder: {folder_name}")
                continue

            if len(video_files) > 1:
                print(f"  Warning: Multiple video files found in folder: {folder_name}. Only the first one will be processed.")

            original_video = video_files[0]
            original_video_path = os.path.join(item_path, original_video)

            _, ext = os.path.splitext(original_video)
            ext = ext.lower()

            # Define the new video name
            new_video_name = f"{folder_name}{ext}"  

            destination_path = os.path.join(destination_folder, new_video_name)

            try:
                # Copy the file to the destination folder with the new name
                shutil.copy2(original_video_path, destination_path)
                print(f"  Copied and renamed to: {destination_path}")
            except Exception as e:
                print(f"  Error copying file from {original_video_path} to {destination_path}: {e}")

if __name__ == "__main__":
    extract_and_rename_videos(MAIN_FOLDER, DESTINATION_FOLDER, VIDEO_EXTENSIONS)
    print("\nAll videos have been processed.")
