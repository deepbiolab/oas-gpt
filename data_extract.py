import os
import lzma
from tqdm import tqdm
import pandas as pd

def csv_files_in_dir(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return files

folder_path = "oas_pair/"
output_file_train = "data/train.txt"
output_file_val = "data/val.txt"
vocab_file = "vocab.txt"

files = csv_files_in_dir(folder_path)
total_files = len(files)

# Calculate the split indices
split_index = int(total_files * 0.9) # 90% for training
files_train = files[:split_index]
files_val = files[split_index:]

# Process the files for training and validation separately
vocab = set()

def load_one_file(file):
    df = pd.read_csv(file, usecols=['sequence_alignment_aa_heavy', 
                                    'sequence_alignment_aa_light'], skiprows=[0])
    df['scfv'] = df['sequence_alignment_aa_heavy'] + '#' + df['sequence_alignment_aa_light']
    return '\n'.join(df['scfv'].tolist())

# Process the training files
with open(output_file_train, "w", encoding="utf-8") as outfile:
    for filename in tqdm(files_train, total=len(files_train)):
        file_path = os.path.join(folder_path, filename)
        text = load_one_file(file_path)
        outfile.write(text)
        characters = set(text)
        vocab.update(characters)

# Process the validation files
with open(output_file_val, "w", encoding="utf-8") as outfile:
    for filename in tqdm(files_val, total=len(files_val)):
        file_path = os.path.join(folder_path, filename)
        text = load_one_file(file_path)
        outfile.write(text)
        characters = set(text)
        vocab.update(characters)

# Write the vocabulary to vocab.txt
with open(vocab_file, "w", encoding="utf-8") as vfile:
    for char in vocab:
        vfile.write(char + '\n')
print(vocab)