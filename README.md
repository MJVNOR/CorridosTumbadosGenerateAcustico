# DatasetMidiCorridosTumbadosAcustico


## Why we decided to do this project
We decided to do this project due to a task assigned to us in the neural networks class of Professor Julio Waissman Vilanova, this task was about generating music with the use of recurrent neural networks (RNN) and we decided to take this opportunity to create "corridos tumbados", which are very popular mainly in northern Mexico.

## Dataset
To generate the midi dataset we used "Onset and Frames" colab made by Google to generate around 241 "corridos tumbados" in the MIDI format. It was the best midi generator we could find.

## Music Generation

#### GeneratorMusicLstm.ipynb
This is our first aproach using an LSTM model to generate some music files (you can check medium for music results), you can find the generated durations, notes and offsets thar were used for the neuronal network in the "data" folder in this repository.

#### nsynth.ipynb
This is the n-synth that we used to generate music by interpolating our music from the dataset contained in "Midis" folder (you can check medium for music results).

#### AutoMusicGen.ipynb
This is our last aproach using a WaveNet using raw music files wich can be found in the "RawAudio" folder from this repository (you can check medium for music results).

[medium link (spanish)](https://mjvnor.medium.com/como-fallar-en-generar-corridos-tumbados-mediante-ia-28c74a0b23db)

[medium link (english) (under construction)](https://github.com/MJVNOR/CorridosTumbadosGenerateAcustico)
