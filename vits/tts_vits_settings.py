
port = 7860
url = "http://127.0.0.1:{port}/run/tts-{speaker_id}"

soundfile_dir = "soundfiles"

speakers = {
    # 'narration': "Shiromi Iori",
    # 'narration': "Tendou Alice",
    'narration': "Misono Mika",
    'dialogue': "Tendou Alice",
    'speaker-default': "Misono Mika",
    'default': "Misono Mika",
}
# "Tendou Alice",
# "Misono Mika",
# "Shiromi Iori",
# "Natsume Iroha",
# "Hayase Yuuka",
# "Saiba Momoi",
# "Ameth",
# "Kyoka",
# "Yuni",
# "Hatsune",
# "Pecorine",
# "Kokoro",
# "Kyaru",
# "Herrscher of Reason",
# "Theresa",

synthesis_parameters = {
	#   "content": "",
	#   # : string
	'Language': "Japanese",
	#  : string
	'noise_scale': 0.6,
	#  : number
	'noise_scale_w': 0.668,
	#  : number
	'length_scale': 1,
	#  : number
	'Symbol input': False,
	#  : boolean
}
