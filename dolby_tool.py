#!/bin/env python3

import subprocess
import sys
import os
import click

DDP_ENC_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/DDP_Pro_Enc_v3.10.2_x86_32.exe'
SMPTE_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/smpte.exe'
STD_IO_LOCATION = '/media/sf_Shared_Folder/dolby/2023'
FFPROBE = '/usr/bin/ffprobe -v error -select_streams a:0 -show_entries stream=channels -of default=noprint_wrappers=1:nokey=1'
PROG_CONF_CHAN_NUM = {1: 1, 2: 2, 3: 4, 4: 4, 5: 5, 6: 5, 7: 6, 21: 8, 24: 7}


def channel_check(input_file: str, program_config: int) -> None:
    """
    Function to check how many audio channels a file has, to make sure there
    are enough channels to do a change of program configuration.
    If there are not enough channels, a message will be printed out and the
    tool will exit.

    :param str: String to be used for the input file.
    :param int: Integer to be used as the program config index to be checked.
    """
    input_file_channel_number = int(os.popen(
        f'{FFPROBE} {input_file}').read())
    if input_file_channel_number < PROG_CONF_CHAN_NUM[program_config]:
        print('The input file does not have enough audio channels to do this program configuration change.')
        sys.exit()


def create_dolby_digital(input_file: str, output_file: str) -> None:
    """
    cmd to create Dolby Digital Plus files.

    :param str: String to be used as the input file name.
    :param str: String to be used as the output file name.
    """
    cmd = f'wine {DDP_ENC_LOCATION} -md1 -i{input_file} -o{output_file}.ac3'
    subprocess.call(cmd, shell=True)


def create_dolby_digital_plus(input_file: str, output_file: str) -> None:
    """
    cmd to create Dolby Digital Plus files.

    :param str: String to be used as the input file name.
    :param str: String to be used as the output file name.
    """
    cmd = f'wine {DDP_ENC_LOCATION} -md0 -i{input_file} -o{output_file}.ec3'
    subprocess.call(cmd, shell=True)


def smpte_wrapper(input_file: str, filetype: str) -> None:
    """
    Wrap .ac3 or .ec3 file as SMPTE .wav file.

    :param str: String to be used as the input file.
    :param str: String to be used as the filetype of the input file.
    """
    smpte_wrap = f'wine {SMPTE_LOCATION} -i{input_file}.{filetype} -o{input_file}.wav'
    subprocess.call(smpte_wrap, shell=True)


def change_program_config(input_file: str, program_config: int, output_file="") -> None:
    """
    Change the program configuration/speaker layout of a Dolby file.

    NOTE: Modes -a0, -a1 and -a2 require -l0 (LFE disabled).

    Program Configuration Modes:
        1,   #     C
        2,   # L R
        3,   # L R C LFE
        4,   # L R   LFE Ls
        5,   # L R C LFE Ls
        6,   # L R   LFE Ls Rs
        7,   # L R C LFE Ls Rs
        21,  # L R C LFE Ls Rs Lrs Rrs
        24   # L R C LFE Ls Rs Cs

    :param str: String to be used as the input file.
    :param int: Number used to signify which program configuration is desired.
    :param str: String to be used as the output file name.
    """
    filepath_length = len(input_file.split('/'))
    filename = input_file.split('/')[filepath_length - 1].split('.')[0]
    filetype = input_file.split('/')[filepath_length - 1].split('.')[1]
    if output_file == "":
        output_file = filename
    lfe_flag = ' -l0' if program_config in {1, 2} else ' -l1'
    cmd = f'wine {DDP_ENC_LOCATION} -i{input_file} -o./{output_file}.{filetype} -a{program_config}'
    cmd += lfe_flag
    subprocess.call(cmd, shell=True)


@click.command()
@click.option('--dolby_digital', '-cdd', help='Create a Dolby Digital file', type=str)
@click.option('--dolby_digital_plus', '-cddp', help='Create a Dolby Digital Plus file', type=str)
@click.option('--program_config', '-pc', help='Change the program configuration/speaker layout', type=int)
@click.option('--smpte', '-s', help='Wrap an ac3 or ec3 file up as SMPTE wav file.', is_flag=True, default=False)
@click.option('--input_file', '-i', help='String to be used as the input file', type=str)
@click.option('--output_file', '-o', help='String to be used as the output file', type=str)
def main(dolby_digital: str, dolby_digital_plus: str, program_config: int, smpte: bool, input_file: str, output_file: str) -> None:
    """
    This is a tool that allows creation of Dolby Digital and Dolby Digital Plus
    files as well as changing the program configuration and SMPTE wrapping.
    Input file and output file can be specified, if they are not, the output
    file name will be the same as the input file.
    If the input file is not provided, this will use the file flight_audio.wav
    as an example.

    :param str: String to be used as the Dolby Digital file name on creation.
    :param str: String to be used as the Dolby Digital Plus file name on creation.
    :param int: Integer to be used to identify the desired program configuration to be used.
    :param bool: Flag for whether the output file is to be SMPTE wrapped.
    :param str: String to be used as the input file.
    :param str: String to be used as the output file.
    """
    # Handling the creation of dolby digital files and whether the program
    # configuration is to be changed as well as SMPTE wrapping.
    if dolby_digital:
        create_dolby_digital(
            f'{STD_IO_LOCATION}/flight_audio.wav', dolby_digital)
        if program_config:
            channel_check(
                f'{STD_IO_LOCATION}/flight_audio.wav', program_config)
            change_program_config(
                f'{STD_IO_LOCATION}/{dolby_digital}.ac3', program_config)
        if smpte:
            smpte_wrapper(f'{dolby_digital}', 'ac3')

    # Handling creation of dolby digital plus files and whether the program
    # configuration is to be changed as well as SMPTE wrapping.
    if dolby_digital_plus:
        create_dolby_digital_plus(
            f'{STD_IO_LOCATION}/flight_audio.wav', dolby_digital_plus)
        if program_config:
            channel_check(
                f'{STD_IO_LOCATION}/flight_audio.wav', program_config)
            change_program_config(
                f'{STD_IO_LOCATION}/{dolby_digital_plus}.ec3', program_config)
        if smpte:
            smpte_wrapper(f'{dolby_digital_plus}', 'ec3')

    # Changing program configuration with no input or output and without
    # creating a dolby file. (Not a likely use case).
    if program_config and not dolby_digital and not dolby_digital_plus and not input_file and not output_file:
        channel_check(f'{STD_IO_LOCATION}/flight_audio.wav', program_config)
        change_program_config(
            f'{STD_IO_LOCATION}/flight_audio.wav', program_config)

    # Handling changing program configuration when input_file and output_file
    # are provided.
    elif program_config and input_file and output_file:
        channel_check(input_file, program_config)
        change_program_config(input_file, program_config, output_file)
        if smpte:
            smpte_wrapper(f'{output_file}', f'{input_file.split(".")[1]}')
    elif program_config and input_file:
        channel_check(input_file, program_config)
        change_program_config(input_file, program_config)
        if smpte:
            smpte_wrapper(f'{input_file}', f'{input_file.split(".")[1]}')
    elif program_config and output_file:
        channel_check(f'{STD_IO_LOCATION}/flight_audio.wav', program_config)
        change_program_config(
            f'{STD_IO_LOCATION}/flight_audio.wav', program_config, output_file)
        if smpte:
            smpte_wrapper(f'{output_file}', 'wav')


if __name__ == '__main__':
    main()
