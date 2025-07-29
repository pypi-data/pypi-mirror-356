#!/usr/bin/env python3
import click
import sys
import shlex
import subprocess as sp
from console import  fg, bg

import os
import glob

import srt
#  like mpv but try to get audio and subtitle based on similarity
#  also creates spectrogram
#
#
#




def combine(primary_language,  secondary_language, ide, merged_path=None):
    if merged_path is None:
        print("x... no merging")
        return
    # Read files and convert to list
    primary_path =  primary_language
    secondary_path =  secondary_language
    primary_file = open(primary_path, 'r', errors='ignore')
    primary_text = primary_file.read()
    primary_file.close()
    secondary_file = open(secondary_path, 'r', errors='ignore')
    secondary_text = secondary_file.read()
    secondary_file.close()
    subtitle_generator_primary = srt.parse(primary_text)
    subtitles_primary = list(subtitle_generator_primary)
    subtitle_generator_secondary = srt.parse(secondary_text)
    subtitles_secondary = list(subtitle_generator_secondary)

    # Make primary yellow
    for s in subtitles_primary:
        if ide == 1:
            s.content = '<font color="#ffff54">' + s.content + '</font>' # yell
        elif ide == 2:
            s.content = '<font color="#ff5454">' + s.content + '</font>' # RED
        elif ide == 3:
            s.content = '<font color="#ff54ff">' + s.content + '</font>' # magenta
        else:
            s.content = '<font color="#54ffff">' + s.content + '</font>' # cyan

    # Place secondary on top
    for s in subtitles_secondary:
        s.content = '<font color="#77ff77">' + s.content + '</font>'
        s.content = '{\\an8}' + s.content

    # Merge
    print(f"i... merging to {merged_path}")
    subtitles_merged = subtitles_primary + subtitles_secondary
    subtitles_merged = list(srt.sort_and_reindex(subtitles_merged))

    # Write merged to file
    #merged_path = f"merged_{ide}.srt" # output # "merged.srt"#primary_path.replace(primary_language, 'merged')

    merged_text = srt.compose(subtitles_merged)
    merged_file = open(merged_path, 'w')
    merged_file.write(merged_text)
    merged_file.close()




DEBUG = False
def produce_output_filename(infile, outputname, model_size):
    """
    same in fawhis and mpvsa
    """
    # ================================ OUTPUT ====================
    file_name = "x.srt"
    if DEBUG:
        print(f"> fi {infile}")
        print(f"> di {os.path.dirname(infile)}")
        print(f"> st {os.path.splitext(os.path.dirname(infile))}")
        print(f"> 00 {os.path.splitext(os.path.dirname(infile))[0]}")
        print(f"> --" )
    # --------------------   extract dirname from infile ------------
    dirname = ""
    if os.path.dirname(infile) != "":
        dirname = os.path.splitext(os.path.dirname(infile))[0]
        dirname = f"{dirname}/"
    else:
        dirname = ""
    if DEBUG: print("> dn==", dirname)

    # ----------------------------
    if outputname is not None:
        # ------ cancel my dirname idea if already defined in outputname
        if os.path.dirname(outputname) != "":
            dirname = ""
        if outputname.find(r".srt") > 0:
            file_name = f"{dirname}{outputname}"
        else:
            file_name = f"{dirname}{outputname}.srt"
    else:
        file_name = os.path.splitext(os.path.basename(infile))[0] + f"_{model_size}.srt"
        file_name = f"{dirname}{file_name}"
    return file_name






# ================================================================================
#   constructs the CMD
# --------------------------------------------------------------------------------
def mpvsub( subtitles, audios, video_file):
    opt = ""
    optau = ""
    if subtitles is not None and len(subtitles) > 0:
        for i in subtitles:
            opt = f"{opt} --sub-file={i} "
    if audios is not None and len(audios) > 0:
        for i in audios:
            optau = f"{optau} --audio-file={i} "
    CMD = f"mpv --no-sub-auto {opt} {optau} {video_file}"
    return CMD
    # mpv "${sub_options[@]}" --no-sub-auto  --sid=1 "$video_file"





# ================================================================================
# RUNS
# --------------------------------------------------------------------------------
def runcmd(CMD):
    #CMD = f"mpv {general_filename} --sub-file={another_filename}"
    args = shlex.split(CMD)
    #print(args)
    #print()
    sp.run(args)

def confirm_selection(audio, subtitle):
    print()
    SPC = ""
    print(f"Suggested    Audio:", end="")
    for i in audio:
        print(SPC, i)
        SPC = " " * 20
    if len(audio) == 0:print()
    SPC = ""
    print(f"Suggested Subtitle: ", end="")
    for i in subtitle:
        print(SPC, i)
        SPC = " " * 20
    if len(subtitle) == 0:print()
    print()
    print(f"{fg.orange}Press Enter to confirm, any other key to cancel.{fg.default}")
    choice = input()
    return choice == ''

def get_dirname(infile):
    dirname = ""
    if os.path.dirname(infile) != "":
        dirname = os.path.splitext(os.path.dirname(infile))[0]
        dirname = f"{dirname}/"
    else:
        dirname = ""
    return dirname


# def find_best_match(video_file):
#     video_base = os.path.splitext(video_file)[0].lower()
#     dirname = get_dirname(video_file)
#     print(f"i... searching @ {dirname}* ")

#     if dirname != "":
#         cwd = os.getcwd()
#         os.chdir(dirname)
#     files = glob.glob("*")
#     if dirname != "":
#         files = [f"{dirname}{x}" for x in files]
#         os.chdir(cwd)

#     print(f"i... total files: {len(files)}")
#     #print(f"i... total files: {files}")
#     audio_exts = ('.mp3', '.opus', '.m4a')
#     subtitle_ext = '.srt'

#     files = [ x for x in files if len(os.path.splitext(x)[-1]) > 3]
#     files = [ x for x in files if (os.path.splitext(x)[-1].lower() in audio_exts) or (os.path.splitext(x)[-1].lower()  in subtitle_ext) ]
#     print(f"i... Files:{files}")

#     audio_file = None
#     subtitle_file = None
#     best_audio_score = -1
#     best_subtitle_score = -1


#     def match_score(name1, name2):
#         score = 0
#         for c1, c2 in zip(name1, name2):
#             if c1 == c2:
#                 score += 1
#             else:
#                 break
#         return score


#     for f in files:
#         f_lower = f.lower()
#         base = os.path.splitext(f_lower)[0]
#         score = match_score(video_base, base)
#         if score > 0:
#             if f_lower.endswith(audio_exts) and score > best_audio_score:
#                 audio_file = f
#                 best_audio_score = score
#             elif f_lower.endswith(subtitle_ext) and score > best_subtitle_score:
#                 subtitle_file = f
#                 best_subtitle_score = score

#     return audio_file, subtitle_file





def find_top_matches(video_file, top_n=8, score_cutoff=1, threshold=50.0):
    video_base = os.path.splitext(video_file)[0].lower()
    dirname = os.path.dirname(video_file)
    if dirname != "":
        cwd = os.getcwd()
        os.chdir(dirname)
    files = glob.glob("*")
    if dirname != "":
        files = [os.path.join(dirname, x) for x in files]
        os.chdir(cwd)

    audio_exts = ('.mp3', '.opus', '.m4a')
    subtitle_ext = '.srt'

    files = [x for x in files if len(os.path.splitext(x)[-1]) > 3]
    files = [x for x in files if (os.path.splitext(x)[-1].lower() in audio_exts) or (os.path.splitext(x)[-1].lower() == subtitle_ext)]

    def match_score(name1, name2):
        score = 0
        for c1, c2 in zip(name1, name2):
            if c1 == c2:
                score += 1
            else:
                break
        return score

    audio_matches = []
    subtitle_matches = []

    for f in files:
        f_lower = f.lower()
        base = os.path.splitext(f_lower)[0]
        score = match_score(video_base, base)
        if score >= score_cutoff:
            if f_lower.endswith(audio_exts):
                audio_matches.append((score, f))
            elif f_lower.endswith(subtitle_ext):
                subtitle_matches.append((score, f))

    def renormalize(scores):
        if not scores:
            return []
        min_score = min(s for s, _ in scores)
        max_score = max(s for s, _ in scores)
        if max_score == min_score:
            return [(100, f) for _, f in scores]
        return [((s - min_score) / (max_score - min_score) * 100, f) for s, f in scores]

    audio_matches = renormalize(audio_matches)
    subtitle_matches = renormalize(subtitle_matches)

    audio_matches = [x for x in audio_matches if x[0] > threshold]
    subtitle_matches = [x for x in subtitle_matches if x[0] > threshold]

    audio_matches.sort(key=lambda x: x[0], reverse=True)
    subtitle_matches.sort(key=lambda x: x[0], reverse=True)

    print(subtitle_matches)
    print(audio_matches)

    top_audio = [f for _, f in audio_matches[:top_n]]
    top_subtitle = [f for _, f in subtitle_matches[:top_n]]

    return top_audio, top_subtitle




@click.command()
@click.argument('video_file', default=None)
@click.option('--spectrum_mp4', '-s', is_flag=True, help="create waterfall spectrum when video_file is audio")
@click.option('--merge', '-m', is_flag=True, help="merge 2 subtitles together")
def main( video_file, spectrum_mp4, merge):
    """
    joins all srt subtitles (local and remote folder too) and
    runs mpv
    """
    if video_file is None:
        print("X... give me video file")
        sys.exit(0)

    #fcomment = 6
    #fname = os.path.splitext(video_file)[0]
    # ---------------------- check if sound -----------------------
    sound_exts = {'.mp3', '.opus', '.m4a', '.wav', '.flac', '.aac'}
    exists = os.path.isfile(video_file)
    ext = os.path.splitext(video_file)[1].lower()
    is_sound = ext in sound_exts
    if is_sound:
        print(f"i... {video_file}  is  {fg.orange}SOUND{fg.default}\n")
    if is_sound and spectrum_mp4:
        base, _ = os.path.splitext(video_file)
        mp4_file = base + '.mp4'
        if os.path.isfile(mp4_file):
            print(f"X... file {mp4_file} already exists. ")
            sys.exit(1)
        CMD = f"time ffmpeg  -hide_banner  -i {video_file} -filter_complex showspectrum=mode=combined:scale=sqrt:color=plasma:slide=1:fscale=log:s=300x180:win_func=gauss -y -acodec copy {mp4_file}"
        print(CMD)
        runcmd(CMD)
        sys.exit(0)


    audio, subtitle = find_top_matches(video_file)#best_match(video_file)


    #print("Audio:", audio)
    #print("Subtitle:", subtitle)

    if confirm_selection(audio, subtitle):
        print("Confirmed.")
    else:
        print("Cancelled.")
        sys.exit(0)

    # merging
    if merge:
        subtitle = [x for x in subtitle if x.find("merged") < 0]
        if len(subtitle) > 1:
            for i in range(1, len(subtitle)):
                merged_path = produce_output_filename( subtitle[i], None, model_size=f"merged{i}")
                combine(subtitle[0], subtitle[i], i, merged_path=merged_path)
        print("i... MERGED")
        sys.exit(0)

    cmd = mpvsub(subtitle, audio, video_file)
    print(cmd)
    runcmd(cmd)


if __name__ == "__main__":
    main()
