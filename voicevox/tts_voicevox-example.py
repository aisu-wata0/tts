
from python_utils_aisu import utils
from tts.voicevox import tts_voicevox_utils
from tts import tts_utils
from translation_utils import tr_google

def main():
  texts = [
  #   {
  #     'id': "really",
  #     'text': """
  # Really, reaally interesting!
  # So, soo exciting!
  # Quite, quiite fun!
  # Hurry hurry, we'll be late laate!
  # Study study all day, my brain is mush muush...
  # Walking walking endlessly... when will we arrive, I wonder woonder?""",
  #   },
  #   {'id': "chuuni-0", 'text': "To fret over what you cannot change is as pointless as trying to illuminate the night sky by blowing out the sun.",},
  #   {'id': "chuuni-1", 'text': "The day shall come when all we know and all we are has faded into dusk. The ultimate riddle I have to solve before that light runs out.",},
  #   {'id': "chuuni-2", 'text': "The light of truth pierces even the veil of belief - when knowledge awakens, illusion perishes. The dawn of understanding cannot be dimmed.",},
  # 	{
  # 		'id': "really ro b",
  # 		'text': """
  # リアリー・リーオーリー・イントラステング・ソー・スー・エクサイティング・クァイト・クィアイト・ファン""",
  # 	},
  # 	{
  #           'id': "really ro s",
  #           'text': """
  # リアリー リーオーリー イントラステング ソー スー エクサイティング クァイト クィアイト ファン""",
  # 	},
  # 	{
  #           'id': "really ro nos",
  #           'text': """
  # リアリーリーオーリーイントラステングソースーエクサイティングクァイトクィアイトファン""",
  # 	},
  ]

  synthesis_parameters = [
    {
      
      "speedScale": 1,
      # "pitchScale": 2,
      "intonationScale": 1,
      # "volumeScale": 0,
      # "prePhonemeLength": 0,
      # "postPhonemeLength": 0,
    },
  ]

  for speaker_id in [
    0,
    # 2,
    # 4,
    # 6,
    # 8,
    # 14,
    # 19,
    # 20,
    # 22,
    # 24,
    # 25,
    # 31,
    # 44,
    # 46,
    # 47,
    # 48,
    # 59,
  ]:
    for t in texts:
      for sp in synthesis_parameters:
        text = t['text']
        id = t['id']

        Voicevox_args = {
            # 'url': tts_voicevox_settings.url,
            # 'port': tts_voicevox_settings.port,
            'speaker_id': speaker_id,
            'synthesis_parameters': sp,
        }
        
        voicevox = tts_voicevox_utils.TtsVoicevox(
             **Voicevox_args,
        )
        print(text)
        text = tr_google.translate(text, src='en', dest='ja')
        print(text)
        filename = f"{speaker_id}-{id} {utils.string_parameters(sp)}.wav"
        filepath = voicevox.SynthesisSaveWav(text)

        print(filename)
        tts_utils.playFile(filename)


if __name__ == "__main__":
  main()
