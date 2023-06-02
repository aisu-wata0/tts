import requests
import tts.vits.tts_vits_settings as tts_vits_settings

url = "http://127.0.0.1:7860/run/tts-Tendou Alice"

synthesis_parameters = {**tts_vits_settings.synthesis_parameters}
synthesis_parameters['content'] = "Hello"

print(synthesis_parameters)

response = requests.post(url, json={
	"data": [
	synthesis_parameters['content'],
	synthesis_parameters['Language'],
	synthesis_parameters['noise_scale'],
	synthesis_parameters['noise_scale_w'],
	synthesis_parameters['length_scale'],
	synthesis_parameters['Symbol input'],
	]
}).json()

for k,v in response.items():
    print(f'"{k}":', v)
