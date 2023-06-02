
port = 7860
url = "http://127.0.0.1:{port}/run/tts-{speaker_id}"

soundfile_dir = "soundfiles"

speaker_id = "Tendou Alice"

speakers = {
    'narration': "Misono Mika",
    'dialogue': "Tendou Alice",
    'speaker-default': "Misono Mika",
    'default': "Misono Mika",
}

synthesis_parameters = {
	#   "content": "",
	#   # : string, // represents text string of 'Text' Textbox component
	'Language': "Japanese",
	#  : string, // represents selected choice of 'Language' Dropdown component
	'noise_scale': 0.6,
	#  : number, // represents selected value of 'noise_scale' Slider component
	'noise_scale_w': 0.668,
	#  : number, // represents selected value of 'noise_scale_w' Slider component
	'length_scale': 1,
	#  : number, // represents selected value of 'length_scale' Slider component
	'Symbol input': False,
	#  : boolean, // represents checked status of 'Symbol input' Checkbox component
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