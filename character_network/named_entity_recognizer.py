import spacy
from nltk.tokenize import sent_tokenize
import pandas as pd
from ast import literal_eval
import os 
import sys
import pathlib
folder_path = pathlib.Path().parent.resolve()
sys.path.append(os.path.join(folder_path, '../'))
from utils.data_loader import load_subtitles_dataset

class NamedEntityRecognizer:
    def __init__(self):
        try:
            spacy.require_gpu()
            print("✅ spaCy is using GPU 🚀")
        except Exception as e:
            print("⚠️ spaCy GPU not available, falling back to CPU 🧠")
            print(f"Error: {e}")
        
        self.nlp_model = self.load_model()
        pass

    def load_model(self):
        nlp = spacy.load("en_core_web_trf")
        return nlp

    def get_ners_inference(self,script):
        script_sentences = sent_tokenize(script)
        ner_output = []

        for sentence in script_sentences:
            doc = self.nlp_model(sentence)
            ners = set()
            for entity in doc.ents:
                if entity.label_ =="PERSON":
                    print(f"Found PERSON: {entity.text}")
                    full_name = entity.text
                    first_name = full_name.split(" ")[0]
                    first_name = first_name.strip()
                    ners.add(first_name)
            print(f"Sentence: {sentence}\nNERs: {ners}\n")        
            ner_output.append(ners)
        
        print("NERs for this script:", ner_output[:5])
        return ner_output

    def get_ners(self,dataset_path,save_path=None):
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            df['ners'] = df['ners'].apply(lambda x: literal_eval(x) if isinstance(x,str) else x)
            return df

        # load dataset 
        df = load_subtitles_dataset(dataset_path)

        # Run Inference
        df['ners'] = df['script'].apply(self.get_ners_inference)

        if save_path is not None:
            df.to_csv(save_path,index=False)
        
        return df