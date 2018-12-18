import requests

def downloadHTTP(url):
    try:
        localFilename = url.split('/')[-1]

        r = requests.get(url, stream = True)
        with open(localFilename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        return localFilename
    except Exception as e:
        print(e)
        return ''
