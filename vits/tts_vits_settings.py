
port = 7860
url = "http://127.0.0.1:{port}/run/tts-{speaker_id}"

soundfile_dir = "soundfiles"

speaker_id = "Tendou Alice"
# Tendou Alice
# Misono Mika
# Shiromi Iori
speakers = {
    'narration': "Shiromi Iori",
    'dialogue': "Tendou Alice",
    'speaker-default': "Misono Mika",
    'default': "Misono Mika",
}

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

# "Tendou Alice",
# "Natsume Iroha",
# "Hayase Yuuka",
# "Misono Mika",
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