
## Description

FasterWhisper fine tuned models by [Xabier de Zuazo](https://huggingface.co/zuazo) for all the iberian peninsula languages, `pt`, `es`, `gl`, `ca`, `eu`

> NOTE: this is intended to use only these specific finetuned models, if you want to use your own models use the main [ovos-stt-plugin-fasterwhisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper) instead

## Install

`pip install ovos-stt-plugin-fasterwhisper-zuazo`

## Configuration

to use small model locally

```json
  "stt": {
    "module": "ovos-stt-plugin-fasterwhisper-zuazo",
    "ovos-stt-plugin-fasterwhisper-zuazo": {
        "model": "small"
    }
  }
```

to use Large model with GPU

```json
  "stt": {
    "module": "ovos-stt-plugin-fasterwhisper-zuazo",
    "ovos-stt-plugin-fasterwhisper-zuazo": {
        "model": "large",
        "use_cuda": true,
        "compute_type": "float16",
        "beam_size": 5,
        "cpu_threads": 4
    }
  }
```

best model is automatically selected based on language unless specified, valid config options are `tiny`,`base`,`small`,`medium`,`large`

> you can also select `large-v1`, `large-v2` or `large-v3` explicitly, but `v3` is only available for `pt`,`ca`,`eu`

### Models


#### Portuguese

self reported WER score from model pages

| Model                             | CV13   |  
|-----------------------------------|--------| 
| `zuazo/whisper-large-v3-pt`       | 4.6003 |  
| `zuazo/whisper-large-v2-pt`       | 5.875  |  
| `zuazo/whisper-large-pt`          | 6.399  |  
| `zuazo/whisper-medium-pt`         | 6.332  |  
| `zuazo/whisper-small-pt`          | 10.252 |  
| `zuazo/whisper-base-pt`           | 19.290 |  
| `zuazo/whisper-tiny-pt`           | 28.965 |  

#### Galician

self reported WER score from model pages

| Model                       | CV13    |
|-----------------------------|---------|
| `zuazo/whisper-large-v2-gl` | 5.9879  |
| `zuazo/whisper-large-gl`    | 6.9398  |
| `zuazo/whisper-medium-gl`   | 7.1227  |
| `zuazo/whisper-small-gl`    | 10.9875 |
| `zuazo/whisper-base-gl`     | 18.6879 |
| `zuazo/whisper-tiny-gl`     | 26.3504 |

#### Catalan

self reported WER score from model pages

| Model                                                | CV13    |  
|------------------------------------------------------|---------| 
| `zuazo/whisper-large-v2-ca`                          | 4.6716  | 
| `zuazo/whisper-large-ca`                             | 5.0700  | 
| `zuazo/whisper-large-v3-ca`                          | 5.9714  | 
| `zuazo/whisper-medium-ca`                            | 5.9954  | 
| `zuazo/whisper-small-ca`                             | 10.0252 | 
| `zuazo/whisper-base-ca`                              | 13.7897 | 
| `zuazo/whisper-tiny-ca`                              | 16.9043 | 

#### Spanish

self reported WER score from model pages

| Model                       | CV13    |
|-----------------------------|---------|
| `zuazo/whisper-large-v2-es` | 4.8949  |
| `zuazo/whisper-large-es`    | 5.1265  |
| `zuazo/whisper-medium-es`   | 5.4088  |
| `zuazo/whisper-small-es`    | 8.2668  |
| `zuazo/whisper-base-es`     | 13.5312 |
| `zuazo/whisper-tiny-es`     | 19.5904 |

#### Basque

self reported WER score from model pages

| Model                              | CV13    |
|------------------------------------|---------|
| `zuazo/whisper-large-v3-eu-cv16_1` | 6.8880  |
| `zuazo/whisper-large-v2-eu-cv16_1` | 7.7204  |
| `zuazo/whisper-large-eu-cv16_1`    | 8.1444  |
| `zuazo/whisper-medium-eu-cv16_1`   | 9.2006  |
| `zuazo/whisper-small-eu-cv16_1`    | 12.7374 |
| `zuazo/whisper-base-eu-cv16_1`     | 16.1765 |
| `zuazo/whisper-tiny-eu-cv16_1`     | 19.0949 |




## Credits

<img src="img.png" width="128"/>

> This plugin was funded by the Ministerio para la Transformación Digital y de la Función Pública and Plan de Recuperación, Transformación y Resiliencia - Funded by EU – NextGenerationEU within the framework of the project ILENIA with reference 2022/TL22/00215337
