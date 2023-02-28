# This is a tool to and modify Dolby Digitial and Dolby Digital Plus files.
# The creation of the files will be handled by DDP_Pro_Enc_v3.10.2_x86_32.exe,
# run using Wine.
# Modifying the program configuration/speaker layout will be handled by ffmpeg.
# It is worth noting Dolby Digital is only capable up to 5.1.
#
# This will be a command line tool, the command line side of things (arguments,
# sub-commands etc) will be handled by Click.

import subprocess
import click
import os


# This is the main command. It is the base command for all sub-commands.
@click.group()
def dolby_cli():
    """
    Main command that covers the sub commands.
    """
    pass


# This is the sub-command to create the Dolby Digital Plus file.
# It takes the input file and the output file as arguments.
@dolby_cli.command()
@click.argument('input_file')
@click.argument('output_file')
def create_dolby_digital_plus(input_file: str, output_file: str) -> None:
    command = f'wine DDP_Pro_Enc_v3.10.2_x86_32.exe -md0 -i"{input_file}" -o"{output_file}" -ac21'
    subprocess.call(command, shell=True)


# This is the sub-command to create the Dolby Digital file.
# It takes the input file and the output file as arguments.
@dolby_cli.command()
@click.argument('input_file')
@click.argument('output_file')
def create_dolby_digitial(input_file: str, output_file: str) -> None:
    command = f'wine DDP_Pro_Enc_v3.10.2_x86_32.exe -md1 -i"{input_file}" -o"{output_file}"'
    subprocess.call(command, shell=True)


# This is the sub-command to modify the program configuration.
# It takes the input file, the output file and the speaker layout as arguments.
@dolby_cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.argument('speaker_layout')
def program_configuration(input_file: str, output_file: str, speaker_layout: str) -> None:
    command = f'ffmpeg -i"{input_file}" -c copy -metadata:s:a:0 "acmod={speaker_layout}" -o"{output_file}"'
    subprocess.call(command, shell=True)


# This is the sub-command to modify the speaker layout.
# It takes the input file, the output file and the speaker layout as arguments.
@dolby_cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.argument('speaker_layout')
def speaker_layout(input_file: str, output_file: str, speaker_layout: str) -> None:
    command = f'ffmpeg -i"{input_file}" -c copy -metadata:s:a:0 "channel_layout={speaker_layout}" -o"{output_file}"'
    subprocess.call(command, shell=True)


# This is the sub-command to extract audio from a video file (starting with
# .mov extension)
# It takes an input video file and outputs a .wav audio file.
@dolby_cli.command()
@click.argument('input_file')
@click.argument('output_file')
def extract_audio(input_file: str, output_file: str) -> None:
    """
    Sub-command that extracts the audio from a video file and outputs it as a
    .wav file.

    :param str: Name of the input file
    :param str: Name of the output file
    """
    command = f'ffmpeg -i {input_file}.mov -vn -acodec pcm_s16le {output_file}.wav'
    subprocess.call(command, shell=True)


# This sub-command extracts the Dolby from the audio file.
@dolby_cli.command()
@click.argument('input_file')
@click.command('output_file')
def extract_dolby(input_file: str, output_file: str) -> None:
    """
    Sub-command that extracts the Dolby audio from an audio file
    and outputs it as a .wav file.

    :param str: Name of the input_file.
    :param str: Name of the output_file
    """
    command = f'ffmpeg -i {input_file}.wav -af "pan=quad|c0=c12|c1=c13|c2=c12|c3=c13" {output_file}.wav'
    subprocess.call(command, shell=True)
