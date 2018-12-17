var wavesurfer = WaveSurfer.create({
  container: '#waveform',
  scrollParent: true,
  waveColor: 'green',
  progressColor: 'white'
})

wavesurfer.on('pause', function () {
  wavesurfer.pause()
  wavesurfer.params.container.style.opacity = 0.9
})
wavesurfer.on('play', function () {
  wavesurfer.play()
})

wavesurfer.load('file4.mp3')