# transform_audio.py usage

 1. Install pocketsphinx.
 2. Inside the pocketsphinx models directory (usually `%PYTHON%\Lib\site-packages\pocketsphinx\models`) extract the [models.7z](https://drive.google.com/open?id=1TiEisEbHlTAcHM82iDVCF9qFKlj9yOQ1) archive. The file structure should be similar to this:
 
    ![file_structure](https://i.imgur.com/VGe6N4P.png)
    
 3. Use transform_audio.py as imported module or from the comamnd line.

*Command line usage example:*

    `python transform_audio.py -w samples1.wav -model=en-us -d`
