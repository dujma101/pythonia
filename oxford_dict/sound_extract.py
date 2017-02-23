words = ['illici01.wav','conjur03.wav','cram0001.wav']


#
# podije = s_file.split()
#
#
# one = []
# rest = []
# for sve in podije:
#     rest.append(sve[5:])
#     one.append(sve[5:6])
#
# # print(one)
# print(rest)
#
# result = zip(one, rest)
# resultList = list(result)
# #print(resultList)
#
import urllib.request

baseURL= "http://media.merriam-webster.com/soundc11/"

for word in words:
#
    print(baseURL + word[:1] + '/' + word )
    urllib.request.urlretrieve(baseURL + word[:1] + '/' + word, word)
#     # testfile.retrieve( baseURL + , "file.gz")
#

# import urllib.request
# ...
# # Download the file from `url` and save it locally under `file_name`:
# urllib.request.urlretrieve(url, file_name)