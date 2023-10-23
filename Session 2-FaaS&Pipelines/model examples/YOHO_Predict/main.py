import os

import librosa
import numpy as np
import tensorflow as tf
import math
import dtlpy as dl
"""
Code from helper functions has been removed due to code privacy
"""

class ServiceRunner:
    # loading the model and the weights here in the init, so it'll be loaded once, no need to consume resources and
    # load it with every execution since we're not saving weights, and it's only predictions
    def __init__(self, weights_h5file: str):
        print("[INFO] defining YOHO ...")
        self.model = self.define_YOHO()
        print("[INFO] loading weights to the model...")
        self.model.load_weights(os.path.join(os.getcwd(), weights_h5file))
        print("[INFO] Loaded ")

    def define_YOHO(self):
        '''
        Manual definition of YOHO model.

        '''
        # TODO
        model = None

        return model

    @staticmethod
    def smoothe_events(events, max_speech_silence=0.8, max_music_silence=0.8,
                       min_dur_speech=0.8, min_dur_music=3.4):
        smooth_events=None
        return smooth_events

    @staticmethod
    def get_log_melspectrogram(audio, sr=16000, hop_length=160,
                               win_length=400, n_fft=512, n_mels=64, fmin=125, fmax=7500):

        """
        Return the log-scaled Mel bands of an audio signal.
        """

        bands = None

        return librosa.core.power_to_db(bands, amin=1e-7)

    def mk_preds_vector(self, audio_path, model, hop_size=6.0, discard=1.0,
                        win_length=8.0, sampling_rate=22050):
        '''
        This function takes an audio file and returns the predictions vector.
        '''

        smooth_events=None

        return smooth_events

    def YOHO_predect(self, item: dl.Item):

        audio_path = item.download()

        see = self.mk_preds_vector(audio_path=audio_path, model=self.model)

        # here we upload the predictions to the Audio item as an annotation
        builder = item.annotations.builder()
        for ann in see:
            builder.add(annotation_definition=dl.Subtitle(label=ann[2],
                                                          text=''),
                        start_time=ann[0],
                        end_time=ann[1],
                        model_info={
                            'name': 'YOHO',
                            'confidence': 0.6
                        })
        builder.upload()
        item.update()

        return item

# if __name__ == "__main__":
#     sr = ServiceRunner(weights_h5file='YOHO-music-speech.h5')
#     # pass one of the original items' id from the platform
#     sr.YOHO_predect(dl.items.get(item_id=''))
