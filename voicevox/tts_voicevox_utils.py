
import logging
import urllib.request
import urllib.parse
import urllib
import requests

import tts.tts_utils as tts_utils

import tts.voicevox.tts_voicevox_settings as tts_voicevox_settings

class TtsVoicevox(tts_utils.Tts):
  def __init__(
      self,
      url=tts_voicevox_settings.url,
      port=tts_voicevox_settings.port,
      speakers=tts_voicevox_settings.speakers,
      synthesis_parameters=tts_voicevox_settings.synthesis_parameters,
      soundfile_dir=tts_voicevox_settings.soundfile_dir,
      *args,
      **kwargs,
  ):
    super().__init__(
      url,
      port,
      speakers,
      synthesis_parameters,
      soundfile_dir,
      *args,
      **kwargs,
    )

  def Synthesis(self, text, speaker_id=None, synthesis_parameters={}):
    speaker_id = self.get_speaker_id(speaker_id)
    synthesis_parameters = {**self.synthesis_parameters, **synthesis_parameters}
    params_encoded = urllib.parse.urlencode({'text': text, 'speaker': speaker_id})
    response = requests.post(f'{self.get_url()}/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': speaker_id, 'enable_interrogative_upspeak': True})
    synthesis_request = response.json()
    for k in synthesis_parameters.keys():
      synthesis_request[k] = synthesis_parameters[k]

    synthesis_res = requests.post(f'{self.get_url()}/synthesis?{params_encoded}', json=synthesis_request)
    return synthesis_res.content
