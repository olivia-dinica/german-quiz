import os
import argparse
import numpy as np
import pandas as pd
import glob
from google_images_download import google_images_download
from random import randint

def get_dict(df):
    list_english = list(df.english)
    response = google_images_download.googleimagesdownload()
    for i in list_english:
        print "{0}/{1} complete".format(list_english.index(i), len(list_english))
        image_paths = response.download({"keywords":"{}".format(i),"limit":1,"no_directory":"True", "no_numbering":"True"})
        image_name = image_paths[i][0].split("/")[-1]
        image_extension = image_name.split(".")[-1]
        final_image_name = 'downloads/{0}.{1}'.format(i, image_extension)
        os.rename('downloads/{}'.format(image_name), final_image_name)
        os.system('sips -Z 500 {}'.format(final_image_name))

def main(df):
    # Columns are:
    # 0 type
    # 1 category
    # 2 english
    # 3 indefinite singular OR regular translation if type = adjective
    # 4 definite singular
    # 5 definite plural
    # 6 ability level
    # 7 weight: 1/ability level (higher it is, more likely you'll be asked)
    
    df['weight'] = 1.0/(df['ability_level']+0.001)
    df['weight'] = df['weight']/sum(df['weight'])
    cols = df.columns.tolist()

    while True:
        r = np.random.choice(df.index, p=list(df['weight']))
        incr = df[['def_sing', 'indef_sing', 'def_plur']].iloc[r].isnull().sum()
        print incr, '\n\n', df[['def_sing', 'indef_sing', 'def_plur']].iloc[r]
        l
        os.system('open {}'.format(glob.glob('downloads/{}.*'.format(df.iloc[r]['english']))[0]))
        while True:
            var = raw_input("German translation (Singular Indefinite if a noun): ")
            if var==list_german[r]:
                df.iloc[r]['ability level']+=0.33
                os.system("killall -9 Preview")
                break
            if var=='s' or var=='q':
                os.system("killall -9 Preview")
                print "Correct answer was: {}".format(list_german[r])
                break

        if var=='q':
            exit()

        while True:
            var = raw_input("German translation (Singular Definite if a noun): ")
            if var==list_german_plur[r] or var=='s' or var=='q':
                df.iloc[r]['ability level']+=0.33
                os.system("killall -9 Preview")
                break
            if tries == 2:
                os.system("killall -9 Preview")
                print "Correct answer was: {}".format(list_german_plur[r])
                break

        while True:
            tries += 1
            var = raw_input("German translation (Singular Definite if a noun): ")
            if var==list_german_plur[r] or var=='s' or var=='q':
                df.iloc[r]['ability level']+=0.33
                os.system("killall -9 Preview")
                break
            if tries == 2:
                os.system("killall -9 Preview")
                print "Correct answer was: {}".format(list_german_plur[r])
                break

        if var=='q':
            exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Learn German')
    parser.add_argument('--download_new', '-dn', default=False)
    parser.add_argument('--file', '-f', default='german_words1.csv')
    args = parser.parse_args()

    df = pd.read_csv(args.file)

    if args.download_new:
        get_dict(df)
    else:
        main(df)

