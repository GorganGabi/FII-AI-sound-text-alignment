import httpDownloader as httpd
import constants
import wikiParse
import mkvocab as mvc

archiveName = httpd.downloadHTTP(constants.roWikiArchiveUrl)

# output file is always wiki.txt
wikiParse.buildPlainTextArchive(archiveName)

mvc.createVocabulary ('wiki.txt', 'wikiVocab.txt')
