
from python_utils_aisu import utils
logger = utils.loggingGetLogger(__name__)
logger.setLevel('INFO')

# import winsound

# def playFile(filename):
#   winsound.PlaySound(filename, winsound.SND_FILENAME)

import sounddevice as sd
import numpy as np
import wavfile

def playFile(filename, device=None):
  # Load the wav file
  # with open(filename, 'rb') as (fs1):
  with wavfile.open(filename, 'r') as f:
    sd.play(f.read_float(f.num_frames), f.sample_rate, device=device)
    sd.wait()



def playFileDelete(filepath, device=None, playFile=playFile, delete_file=True) -> bool:
    try:
        playFile(filepath, device=device)
    except Exception as e:
        logger.exception(f"While playing {filepath}")
        return False
    finally:
        if delete_file:
          try:
              if filepath and Path(filepath).exists():
                  Path(filepath).unlink()
          except Exception as e:
              logger.exception(f"While deleting {filepath}")
    return True


from typing import Any, Dict, List, Optional
from pathlib import Path

from python_utils_aisu import utils

class Tts:
  def __init__(
      self,
      url: str,
      port,
      speakers: Dict[str, str],
      synthesis_parameters: Dict[str, Any],
      soundfile_dir: str,
      soundfile_name_timestamp: bool=True,
      soundfile_name_parameters: bool=False,
  ):
    self.url = url
    self.port = port
    self.speakers = speakers
    self.synthesis_parameters = synthesis_parameters
    self.soundfile_dir = soundfile_dir
    self.soundfile_name_timestamp = soundfile_name_timestamp
    self.soundfile_name_parameters = soundfile_name_parameters

  def get_url(self, speaker_id=None):
    return self.url.format(port=self.port, speaker_id=speaker_id)
  
  def get_filepath(self, speaker_id, synthesis_parameters={}):
    fpath = f"{self.soundfile_dir}/{speaker_id}"
    if self.soundfile_name_timestamp:
      fpath = f"{fpath}-{utils.get_timestamp('milliseconds')}"
    if self.soundfile_name_parameters:
      fpath = f"{fpath} {utils.string_parameters(synthesis_parameters)[:80]}"
    return f'{fpath}.wav'

  def Synthesis(self, text, speaker_id=None, synthesis_parameters={}):
    # Should return wav data
    pass

  def get_speaker_id(self, speaker_id):
    if speaker_id is None:
      speaker_id = self.speakers['default']
    return speaker_id

  def SynthesisSaveWav(self, text, speaker_id=None, synthesis_parameters={}, filepath=None):
    speaker_id = self.get_speaker_id(speaker_id)
    if filepath is None:
      filepath = self.get_filepath(speaker_id)
    synthesis_res = self.Synthesis(
        text, speaker_id, synthesis_parameters)
    return self.SynthesisResponseSaveWav(synthesis_res, filepath)

  def SynthesisResponseSaveWav(self, wavData, filepath):
    if not wavData:
      return ""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as outfile:
      outfile.write(wavData)
    return filepath


import re

prose_type = Dict[str, Any]
"""
```python
{
  'type': 'narration' | 'dialogue' | 'speaker',
  # speaker is when a section has a defined name related to the section
  'content': related_content,
  'name': speaker_name,
  'sections': speaker_sections,
  # when type == 'speaker', this is the content parsed into 'dialogue' and 'narration' (kind of recursive, `type(speaker_sections) == prose_type`)

}
```
"""

def tts_splitter(text: str, speakers: Dict[str, str]) -> List[prose_type]:
    prose_sections = extract_prose_sections(text)
    for s in prose_sections:
        s['tts_args'] = {}
        try:
            if s['type'] == 'speaker':
                if s['name'] not in speakers:
                    s['tts_args']['speaker_id'] = speakers['speaker-default']
                else:
                    s['tts_args']['speaker_id'] = speakers[s['name']]
            else:
                if s['type'] in speakers:
                  s['tts_args']['speaker_id'] = speakers[s['type']]
                else:
                  s['tts_args']['speaker_id'] = speakers['default']
        except Exception:
            logger.exception(f"While setting tts_args for prose_section {s}")
    return prose_sections


def extract_prose_sections(input_string: str) -> List[prose_type]:
    # Define regex patterns for different section types
    speaker_pattern = r'(?:\n|^)([A-Za-z][^:\n]*[A-Za-z]|[A-Za-z]):[^\S\r\n]*([^\n]+)(?=\n|$)'
    # speaker_pattern = r'(?:\n|^)([A-Za-z][A-Za-z_ -]*[A-Za-z]|[A-Za-z]):[^\S\r\n]*([^\n]+)(?=\n|$)'
    dialogue_pattern = r'"([^"]*)"'
    narration_pattern = r'([^"\n]+)'

    # Initialize the list to store extracted sections
    sections = []

    # Initialize the starting index for the next section
    start_index = 0

    # Iterate through the input string and extract sections
    for match in re.finditer(rf'{speaker_pattern}|{dialogue_pattern}|{narration_pattern}', input_string):
        section_start = match.start()
        section_end = match.end()
        logger.info(f"extract_prose_sections: match {match.groups()}")
        # # Check if there is any text between the previous section and the current match
        # if start_index < section_start:
        #     narration_content = input_string[start_index:section_start].strip()
        #     sections.append({"type": "narration", "content": narration_content})
        
        if match.group(4):
            sections.append({'type': 'narration', 'content': match.group(4).strip()})

        # Extract speaker section
        if match.group(1):
            speaker_name = match.group(1).strip()
            related_content = match.group(2).strip()
            speaker_sections = extract_prose_sections(related_content)

            speaker_object = {
                'type': 'speaker',
                'content': related_content,
                'name': speaker_name,
                'sections': speaker_sections,
            }
            sections.append(speaker_object)
        # Extract dialogue section
        elif match.group(3):
            dialogue_content = match.group(3).strip()
            sections.append({'type': 'dialogue', 'content': dialogue_content})

        start_index = section_end

    # Check if there is any remaining text after the last section
    if start_index < len(input_string):
        narration_content = input_string[start_index:].strip()
        sections.append({'type': 'narration', 'content': narration_content})

    return sections


def prose_sections_to_text(prose_sections: List[prose_type], k_name='content') -> str:
  text = ""
  for t in prose_sections:
      text += t[k_name] + "\n"
  return text

import time
import queue
from dataclasses import dataclass

@dataclass
class SoundFile:
  filepath: str
  delay: float
  device: Optional[str]

  def __post_init__(self):
     self.file = None

  def delete_file(self):
    try:
      if self.filepath and Path(self.filepath).exists():
        Path(self.filepath).unlink()
    except Exception as e:
      logger.exception(f"While deleting {self.filepath}")
      return False
    return True

  def play(self, delete_file=False):
    self.play_()
    if delete_file:
      del self.file
      return self.delete_file()
    return True

  def play_(self):
    if not self.file:
      self.read()
    if not self.file:
      raise RuntimeError()
    sd.play(self.file['data'], self.file['sample_rate'], device=self.device)
    sd.wait()

  def read(self):
    with wavfile.open(self.filepath, 'r') as f:
      self.file = {
         'data': f.read_float(f.num_frames),
         'sample_rate': f.sample_rate,
      }
     


def play_files_from_queue(file_queue: "queue.Queue[SoundFile]"):
    while True:
        soundfile = file_queue.get()
        if soundfile.delay > 0:
            time.sleep(soundfile.delay)
        playFileDelete(soundfile.filepath, device=soundfile.device)
        file_queue.task_done()
