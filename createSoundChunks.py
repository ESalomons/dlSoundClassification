import glob
import os
import shutil

from scipy.io import wavfile


def doMain():
    createChunks20180419()


def createChunks20180419():
    # maak brokken van train en testdata voor gebruik tensorflow voorbeeldprogramma

    # parameters
    baseSrcDir = '/Volumes/SAA_DATA/datasets/localizationFiles/20171025AllExtractionsMic4'
    baseTargetDir = '/Users/etto/tmp/tensorChunks'
    chunkTime = 2.0  # seconds

    orgWavDirs1 = ['G428_0.0_1.4',
                   'G527_0.5_1.4',
                   'Studio_2.0_4.2'
                   ]

    orgWavDirs2 = ['G428_2.1_2.4',
                   'G527_1.2_5.8',
                   'Studio_3.0_2.0'
                   ]

    if not os.path.isdir(baseTargetDir):
        os.mkdir(baseTargetDir)

    targetTrainDir = baseTargetDir + '/train'
    if not os.path.isdir(targetTrainDir):
        os.mkdir(targetTrainDir)

    for room in orgWavDirs1:
        srcDir = baseSrcDir + '/' + room
        targetDir = targetTrainDir + '/' + room
        if os.path.isdir(targetDir):
            shutil.rmtree(targetDir)
        os.mkdir(targetDir)

        # iterate over each category
        for catDirLong in glob.glob(srcDir + '/*'):
            catDir = catDirLong.replace(srcDir + '/', '')
            targetCatDir = targetDir + '/' + catDir
            os.mkdir(targetCatDir)

            for longFilename in glob.glob(catDirLong + '/*'):
                filename = longFilename.replace(catDirLong + '/', '')

                # simple: copy file
                targetFileStr = targetCatDir + '/' + filename[:-4] + '_{:d}.wav'

                fr, data = wavfile.read(longFilename)

                stepsize = int(chunkTime * fr)
                filenr = 1
                while filenr * stepsize < len(data):
                    wavfile.write(targetFileStr.format(filenr), fr, data[(filenr - 1) * stepsize: filenr * stepsize])
                    print('written: ' + targetFileStr.format(filenr))
                    filenr += 1


if __name__ == '__main__':
    doMain()
    print('Ready')
