import pandas as pd
import csv
import os

playlistCSV = 'jgs_17122023.csv'
playlistDir = 'playlistSuggestions/'
os.makedirs(playlistDir, exist_ok=True)

minPlLength = 100
playlist = []
with open(playlistCSV, mode='r', encoding='utf8') as file:
    csvFile = csv.reader(file)
    next(csvFile, None)  # skip header
    for line in csvFile:
        if line[4] == '' or line[2] == '':
            continue
        playlist += [line]


def exportToCSV(filename, pl, dir=playlistDir):
    pl.sort()
    df = pd.DataFrame(pl)
    df.to_csv(dir + filename, index=False, header=['Artist', 'Song'])


def genrePlaylists(pl=playlist, minPlaylistLength=minPlLength, dir=playlistDir):
    allGenresList = []
    for lines in pl:
        songGenres = str.split(lines[10], ',')
        for genre in songGenres:
            if genre not in allGenresList and genre != '':
                allGenresList.append(genre)

    for genre in allGenresList:
        songsInGenre = []
        for lines in pl:
            songGenres = str.split(lines[10], ',')
            if genre in songGenres:
                songsInGenre.append([lines[4], lines[2]])

        if len(songsInGenre) >= minPlaylistLength:
            exportToCSV(genre + ' playlist.csv', songsInGenre, dir)


def tempoPlaylist(tempo, window, pl=playlist, minPlaylistLength=minPlLength, dir=playlistDir):
    lowerTempoBound = tempo - window
    upperTempoBound = tempo + window
    tempoPl = []
    for lines in pl:
        if lowerTempoBound <= float(lines[-2]) <= upperTempoBound:
            tempoPl.append([lines[4], lines[2]])

    if len(tempoPl) >= minPlaylistLength:
        fileNameTempo = str(lowerTempoBound) + '_to_' + str(upperTempoBound) + '_bpm_playlist.csv'
        exportToCSV(fileNameTempo, tempoPl, dir)


def mostPopularPlaylist(pl=playlist, minPlaylistLength=minPlLength, dir=playlistDir):
    sortedByPopularity = pl
    sortedByPopularity.sort(key=lambda x: x[7], reverse=True)
    xMostPopularPlaylist = []
    for index, lines in enumerate(sortedByPopularity):
        if index + 1 > minPlaylistLength:
            break
        xMostPopularPlaylist.append([lines[4], lines[2]])

    exportToCSV(str(minPlaylistLength) + '_most_popular_playlist.csv', xMostPopularPlaylist, dir)


def xPlusPopularityPlaylist(xOrHigherPopularity, pl=playlist, minPlaylistLength=minPlLength, dir=playlistDir):
    lowerPopularityBound = xOrHigherPopularity
    popularityPlaylist = []
    for lines in pl:
        if float(lines[7]) >= lowerPopularityBound:
            popularityPlaylist.append([lines[4], lines[2]])

    if len(popularityPlaylist) >= minPlaylistLength:
        exportToCSV(str(lowerPopularityBound) + '_plus_popularity_playlist.csv', popularityPlaylist, dir)


def dancePlaylist(pl=playlist, minPlaylistLength=minPlLength, dir=playlistDir):
    sortedByDanceability = pl
    sortedByDanceability.sort(key=lambda x: x[11], reverse=True)
    xMostDanceablePlaylist = []
    for index, lines in enumerate(sortedByDanceability):
        if index + 1 > minPlaylistLength:
            break
        xMostDanceablePlaylist.append([lines[4], lines[2]])

    exportToCSV(str(minPlaylistLength) + '_most_danceable_playlist.csv', xMostDanceablePlaylist, dir)


def energyPlaylist(highEnergy, pl=playlist, minPlaylistLength=minPlLength, dir=playlistDir):
    sortedByEnergy = pl
    sortedByEnergy.sort(key=lambda x: x[12], reverse=highEnergy)
    energyPl = []
    for index, lines in enumerate(sortedByEnergy):
        if index + 1 > minPlaylistLength:
            break
        energyPl.append([lines[4], lines[2]])

    if highEnergy:
        exportToCSV(str(minPlaylistLength) + '_most_energetic_playlist.csv', energyPl, dir)
        return
    exportToCSV(str(minPlaylistLength) + '_least_energetic_playlist.csv', energyPl, dir)


genrePlaylists()
tempoPlaylist(110, 5)
tempoPlaylist(80, 10)
mostPopularPlaylist()
xPlusPopularityPlaylist(80)
dancePlaylist()
energyPlaylist(highEnergy=True)
energyPlaylist(highEnergy=False)
