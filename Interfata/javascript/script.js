function upload() {
    var data
    $.getJSON('../vers.json', function (json) {
        data = json // this will show the info it in firebug console
        var audioPlayer = document.getElementById('audiofile')
        audioPlayer.muted = true
        var subtitles = document.getElementById('subtitles')
        var syncData = data

        createSubtitle()

        function createSubtitle() {
            var element

            for (var i = 0; i < syncData.length; i++) {
                element = document.createElement('span');
                element.setAttribute('id', 'c_' + i);
                element.innerText = syncData[i].word + ' ';
                subtitles.appendChild(element)
            }
        }

        audioPlayer.addEventListener('timeupdate', function (e) {
            syncData.forEach(function (element, index, array) {
                    if (audioPlayer.currentTime >= element.start && audioPlayer.currentTime <= element.end)
                        if (element.matched === 0) {
                            console.log('-----------')
                            subtitles.children[index].style.background = 'red';
                        } else {
                            subtitles.children[index].style.background = 'yellow';
                        }

                }
            )

        })
    })
}

window.onload = function () {
    upload()
};