#if plexapi doesn't exist, install it
try:
    from plexapi.server import PlexServer
except ImportError:
    print('plexapi is not installed, installing now, if this is failling, install PlexAPI into pip')
    import pip
    pip.main(['install', 'PlexAPI'])
    from plexapi.server import PlexServer
import sys
import os
import time
import datetime
import argparse
import logging
import logging.handlers

def connect_to_plex(server_name, token):
    plex = PlexServer('http://' + server_name + ':32400', token)
    return plex

#function to find content with 4k and 1080p and print them
def find_content(server, section):
    dict = {}
    for item in server.library.section(section).all():
        #get all media files
        if item.type == 'movie':
            dict[item] = {}
            dict[item]['title'] = []
            dict[item]['res'] = []
            dict[item]['bitrate'] = []
            dict[item]['path'] = []
            for media in item.media:
                #check if media is 4k or 1080p
                dict[item]['title'].append(media.title)
                dict[item]['res'].append(media.videoResolution)
                dict[item]['bitrate'].append(media.bitrate)
                dict[item]['path'].append(media.parts[0].file)
        if item.type == 'show':
            dict[item] = {}
            for episode in item.episodes():
                dict[item][episode] = {}
                dict[item][episode]['title'] = []
                dict[item][episode]['res'] = []
                dict[item][episode]['bitrate'] = []
                dict[item][episode]['path'] = []
                dict[item][episode][episode] = []
                for media in episode.media:
                    #check if media is 4k or 1080p
                    if media.videoResolution != 'sd':
                        dict[item][episode]['res'].append(media.videoResolution)
                    if media.videoResolution == 'sd':
                        dict[item][episode]['res'].append('320')
                    dict[item][episode]['bitrate'].append(media.bitrate)
                    dict[item][episode]['path'].append(media.parts[0].file)
    for key in dict.keys():
        resAvailable = ['4k', '1080','720','sd',]
        if item.type == 'movie':
            
            title = key
            resList = dict[key]['res']
            bitrateList = dict[key]['bitrate']
            pathList = dict[key]['path']
            #get highest bitrate in list
            bitrate = max(bitrateList)
            #get index of highest bitrate
            index = bitrateList.index(bitrate)
            bestVersion = resList[index]
            bestBitrate = bitrateList[index]
            bestPath = pathList[index]
            #remove best version from list
            bitrateList.remove(bestBitrate)
            pathList.remove(bestPath)
            #delete all of the files in the pathList
            for path in pathList:
                if os.path.isfile(path.replace(plexPath,localPath)):
                    #check if path.replace(plexPath,localPath) was made 30 days ago
                    if datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(path.replace(plexPath,localPath))) > datetime.timedelta(days=30):
                        print ('removing' + path +'. keeping  ' + str(bestVersion) + ' ' + str(bestBitrate) + ' ' + bestPath)
                        os.remove(path.replace(plexPath,localPath))
        if item.type == 'show':
            for episode in dict[key].keys():
                if None not in dict[key][episode]['res']:
                    title = key
                    resList = dict[key][episode]['res']
                    bitrateList = dict[key][episode]['bitrate']
                    pathList = dict[key][episode]['path']
                    #get highest bitrate in list
                    bitrate = max(bitrateList)
                    #get index of highest bitrate
                    index = bitrateList.index(bitrate)
                    bestVersion = resList[index]
                    bestBitrate = bitrateList[index]
                    bestPath = pathList[index]
                    #remove best version from list
                    bitrateList.remove(bestBitrate)
                    pathList.remove(bestPath)
                    #delete all of the files in the pathList
                    for path in pathList:
                        if os.path.isfile(path.replace(plexPath,localPath)):
                            if datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(path.replace(plexPath,localPath))) > datetime.timedelta(days=30):
                                print ('removing' + path +'. keeping  ' + str(bestVersion) + ' ' + str(bestBitrate) + ' ' + bestPath)
                                os.remove(path.replace(plexPath,localPath))
                                  
#connect to plex server
plexPath = '/media/'
localPath = 'F:/My Drive/'
plexIP = '192.168.1.78'
plexToken = 'ZUzMV_5BNYcfUf5zUM-A'
LibrariesToScan = ['Movies', 'TV Shows']

plex = connect_to_plex(plexIP,plexToken)
for section in LibrariesToScan:
    find_content(plex, section)
