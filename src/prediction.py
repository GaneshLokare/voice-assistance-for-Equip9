import os
from gtts import gTTS
import librosa
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences



LABELS = {'jcb' : 0 , 'bulldozer' : 1, 'crane': 2, 'excavator' : 3, 'roller' : 4}
INV_LABELS = {0 : 'jcb', 1 : 'bulldozer', 2 : 'crane', 3 : 'excavator', 4 : 'roller'}


    
langs=['en']
loaded_model = load_model('model.h5')
sample_rate = 22050
max_length = 45000


def predict(final_words,not_spoken_well):
    # create a gTTS object for each language and save the audio as a file
    for text in not_spoken_well:
        for lang in langs:
            try:
                tts = gTTS(text=text, lang=lang)
                filename = f"{text} {lang}.mp3"
                file_path = os.path.join(os.getcwd(), "pred", filename)
                tts.save(file_path)
                    
            except:
                pass
        
        all_files = os.listdir('pred')
        all_files = ['pred\\' + ele for ele in all_files]

    def load_wav(x, get_duration=True):
            '''This will return the array values of audio with sampling rate of 22050 and Duration'''
            #loading the wav file with sampling rate of 22050
            samples, sample_rate = librosa.load(x, sr=22050)
            if get_duration:
                duration = librosa.get_duration(y = samples, sr = sample_rate)
                return [samples, duration]
            else:
                return samples

    samples_train, durations_train, = [],[]


    for ele in all_files:
        try:
            samples, duration = load_wav(ele)
            samples_train.append(samples)
            durations_train.append(duration)
        except:
            print(ele)

    X_train_processed = pd.DataFrame({'raw_data' : samples_train, 'duration' : durations_train})
        
    max_length  = 50000
    X_train_pad_seq = pad_sequences(X_train_processed.raw_data, 
                                        maxlen = max_length, 
                                        padding = 'post',
                                        dtype = 'float32',
                                        truncating = 'post')

    X_train_mask = X_train_pad_seq != 0
        
    def convert_to_spectrogram(raw_data):
        '''converting to spectrogram'''
        spectrum = librosa.feature.melspectrogram(y=raw_data, sr=2250, n_mels=64)
        logmel_spectrum = librosa.power_to_db(S=spectrum, ref=np.max)
        return logmel_spectrum

        ##using convert_to_spectrogram and convert every raw sequence in X_train_pad_seq and X_test_pad_seq.
        ## saving those all in the X_train_spectrogram and X_test_spectrogram ( These two arrays must be numpy arrays)
    X_train_spectrogram = []
    for ele in X_train_pad_seq:
        logmel = convert_to_spectrogram(ele)
        X_train_spectrogram.append(logmel)
    X_train_spectrogram = np.array(X_train_spectrogram)

    for i in range(len(X_train_spectrogram)):
        y_pred = loaded_model.predict(X_train_spectrogram[i].reshape((1, 64, 88)))
        word = INV_LABELS[np.argmax(y_pred)]
        final_words.append(word)

    return final_words
        
     