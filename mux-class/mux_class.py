#!/usr/bin/env python

import argparse, treat_nfo

def transform_and_mux(folder):
    for file in os.listdir(folder):
        if file.endswith(".nfo.clean"):
            name_file = file.split(".nfo.clean")

            # Build names of files to treat
            in_audio ="rec-" + name_file[0] + "-audio.mjr"
            out_audio = "rec-" + name_file[0] + "-audio.opus"
            in_video = "rec" + name_file[0] + "-video.mjr"
            out_video = "rec" + name_file[0] + "-video.webm"

            # Convert audio and video files
            os.system("janus-pp-rec " + folder + "/" + in_audio + " " + out_audio)
            os.system("janus-pp-rec " + folder + "/" + in_video + " " + out_video)

            # Mux audio and video
            mux_name = name_file[0] + "-mux.webm"
            os.system("ffmpeg -i " + folder + "/" + out_video + " -i " + folder + "/" + out_audio +
                      " -acodec copy -vcodec copy " + folder + "/" + mux_name)

            # Nfo.muxed creation + add opus, webm and mux.webm fields to it
            nfo = treat_nfo.TreatNfo(file, file_name[0], "mux")
            nfo.CreateMuxedNfo(out_audio, out_video, mux_name)

            # Files classification

            day = nfo.GetDay()
            os.system("mkdir " + folder + "/archive-records/" + day)
            hour = nfo.GetHour()
            folder_hour = folder + "/archive-records/" + day + "/" + hour + "-hour"

            folder_muxed = folder + "/archive-records/" + day + "/" + hour + "-hour/muxed"
            folder_opus_webm = folder + "/archive-records/" + day + "/" + hour + "-hour/opus-webm"
            folder_mjr = folder + "/archive-records/" + day + "/" + hour + "-hour/mjr"

            os.system("mkdir " + folder_hour)
            os.system("mkdir " + folder_muxed)
            os.system("mkdir " + folder_audio_video)
            os.system("mkdir " + folder_mjr)

            os.system("mv " + folder + "/" + in_audio + " " + folder_mjr)
            os.system("mv " + folder + "/" + in_video + " " + folder_mjr)
            os.system("mv " + folder + "/" + out_audio + " " + folder_opus_webm)
            os.system("mv " + folder + "/" + out_video + " " + folder_opus_webm)
            os.system("mv " + folder + "/" + mux_name + " " + folder_muxed)

            # Todo : Move archives to S3 and delete all archives from Disk

def pars_argument():
    parser = argparse.ArgumentParser()

    parser.add_argument("folder", help = "Folder with .mjr to be treat (required absolute path)")
    parser.add_argument("--dny_run", help = "display the execution of the program")

    args = parser.parse_args()

    if args.dny_run:
        print """execution :
        -Transform .mjr to .opus and .webm
        -Mux .opus and .webm to -mux.webm
        -Class files by date and hour
        -Format .nfo.clean to .nfo.muxed adding fields audio.opus, video.webm and mux.webm"""
    return args.folder

if __name__ == "__main__":
    folder = pars_argument()

    transform_and_mux(folder)
