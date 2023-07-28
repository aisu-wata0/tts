
import logging
import urllib.request
import urllib.parse
import urllib
import requests

import tts.tts_utils as tts_utils

import tts.vits.tts_vits_settings as tts_vits_settings

import base64

class TtsVits(tts_utils.Tts):
  def __init__(
      self,
      url=tts_vits_settings.url,
      port=tts_vits_settings.port,
      speakers=tts_vits_settings.speakers,
      synthesis_parameters=tts_vits_settings.synthesis_parameters,
      soundfile_dir=tts_vits_settings.soundfile_dir,
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
    if not speaker_id:
      return None
    synthesis_parameters = {**self.synthesis_parameters, **synthesis_parameters}

    synthesis_parameters['content'] = text

    request_json = {
      "data": [
        synthesis_parameters['content'],
        synthesis_parameters['Language'],
        synthesis_parameters['noise_scale'],
        synthesis_parameters['noise_scale_w'],
        synthesis_parameters['length_scale'],
        synthesis_parameters['Symbol input'],
      ]
    }
    url = self.get_url(speaker_id)
    response = requests.post(url, json=request_json).json()

    data = response["data"]
    if data[0] != "Success":
      raise RuntimeError(f'On Synthesis {speaker_id} content: """{text}"""' + data[0])
    
    data_prefix = "data:audio/wav;base64,"
    base64_data = data[1][len(data_prefix):]
    # Decode the base64 data
    decoded_data = base64.b64decode(base64_data)
    return decoded_data
