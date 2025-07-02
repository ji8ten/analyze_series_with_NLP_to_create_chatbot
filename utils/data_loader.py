from glob import glob
import pandas as pd
import os


def load_subtitles_dataset(dataset_path):
    dataset_path = os.path.abspath(dataset_path)
    print(f"Loading subtitles from: {dataset_path}")

    if not os.path.exists(dataset_path):
        print("❌ ERROR: Path does not exist.")
        return pd.DataFrame()
    
    subtitles_paths = glob(dataset_path + '/*.ass')
    print(f"Found {len(subtitles_paths)} .ass files")

    if not subtitles_paths:
        print("❌ No subtitle files found.")
        return pd.DataFrame()
    
    scripts = []
    episode_num = []

    for path in subtitles_paths:
        # Read Lines
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            lines = lines[27:]
            lines = [",".join(line.split(',')[9:]) for line in lines]

        lines = [line.replace('\\N', ' ') for line in lines]
        script = " ".join(lines)
        episode = int(path.split('-')[-1].split('.')[0].strip())

        scripts.append(script)
        episode_num.append(episode)

    df = pd.DataFrame.from_dict({"episode": episode_num, "script": scripts})
    return df