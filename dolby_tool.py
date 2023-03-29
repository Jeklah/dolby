#!/bin/env python3

import subprocess
import click

DDP_ENC_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/DDP_Pro_Enc_v3.10.2_x86_32.exe'
SMPTE_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/smpte.exe'
STD_IO_LOCATION = '/media/sf_Shared_Folder/dolby/2023/'


def create_dolby_digital(input_file: str, output_file: str) -> None:
    """
    Command to create Dolby Digital Plus files.

    :param str: String to be used as the input file name.
    :param str: String to be used as the output file name.
    """
    command = f'wine {DDP_ENC_LOCATION} -md1 -i{input_file} -o{output_file}.ac3'
    subprocess.call(command, shell=True)


def create_dolby_digital_plus(input_file: str, output_file: str) -> None:
    """
    Command to create Dolby Digital Plus files.

    :param str: String to be used as the input file name.
    :param str: String to be used as the output file name.
    """
    command = f'wine {DDP_ENC_LOCATION} -md0 -i{input_file} -o{output_file}.ec3'
    subprocess.call(command, shell=True)


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

    :param str: String to be used as the input file.
    :param int: Number used to signify which program configuration is desired.
    """
    audio_coding_modes = [
        1,   # C
        2,   # L R
        3,   # L R C LFE
        4,   # L R   LFE Ls
        5,   # L R C LFE Ls
        6,   # L R   LFE Ls Rs
        7,   # L R C LFE Ls Rs
        21,  # L R C LFE Ls Rs Lrs Rrs
        24   # L R C LFE Ls Rs Cs
    ]
    # program_configuration, output_file_name = prog_config
    filepath_length = len(input_file.split('/'))
    filename = input_file.split('/')[filepath_length - 1].split('.')[0]
    filetype = input_file.split('/')[filepath_length - 1].split('.')[1]
    if output_file == "":
        output_file = filename
    if program_config in {1, 2}:
        command = f'wine {DDP_ENC_LOCATION} -i{input_file} -o./{output_file}.{filetype} -a{program_config} -l0'
    else:
        command = f'wine {DDP_ENC_LOCATION} -i{input_file} -o./{output_file}.{filetype} -a{program_config} -l1'
    subprocess.call(command, shell=True)


@click.command()
@click.option('--dolby_digital', '-cdd', help='Create a Dolby Digital file', type=str)
@click.option('--dolby_digital_plus', '-cddp', help='Create a Dolby Digital Plus file', type=str)
@click.option('--program_config', '-pc', help='Change the program configuration/speaker layout', type=int)
@click.option('--smpte', '-s', help='Wrap an ac3 or ec3 file up as SMPTE wav file.', is_flag=True, default=False)
@click.option('--input_file', '-i', help='String to be used as the input file', type=str)
@click.option('--output_file', '-o', help='String to be used as the output file', type=str)
def main(dolby_digital: str, dolby_digital_plus: str, program_config: int, smpte: bool, input_file: str, output_file: str):
    if dolby_digital and not program_config:
        create_dolby_digital(
            f'{STD_IO_LOCATION}/flight_audio.wav', dolby_digital)
        if smpte:
            smpte_wrapper(f'{dolby_digital}', 'ac3')
    if dolby_digital_plus and not program_config:
        create_dolby_digital_plus(
            f'{STD_IO_LOCATION}/flight_audio.wav', dolby_digital_plus)
        if smpte:
            smpte_wrapper(f'{dolby_digital_plus}', 'ec3')

    elif program_config and input_file and output_file:
        change_program_config(input_file, program_config, output_file)
        if smpte:
            smpte_wrapper(f'{output_file}', f'{input_file.split(".")[1]}')
    elif program_config and input_file:
        change_program_config(input_file, program_config)
        if smpte:
            smpte_wrapper(f'{output_file}', f'{input_file.split(".")[1]}')
    elif program_config and output_file:
        change_program_config(
            f'{STD_IO_LOCATION}/flight_audio.wav', program_config, output_file)
        if smpte:
            smpte_wrapper(f'{output_file}', 'wav')

    elif program_config and dolby_digital:
        create_dolby_digital(f'{STD_IO_LOCATION}/flight_audio.wav',
                             f'{STD_IO_LOCATION}/{dolby_digital}')
        change_program_config(
            f'{STD_IO_LOCATION}/{dolby_digital}.ac3', program_config)
        if smpte:
            smpte_wrapper(f'{dolby_digital}', 'ac3')

    elif program_config and dolby_digital_plus:
        create_dolby_digital_plus('{STD_IO_LOCATION}/flight_audio.wav',
                                  f'{STD_IO_LOCATION}/{dolby_digital_plus}')
        change_program_config(
            f'{STD_IO_LOCATION}/{dolby_digital_plus}.ec3', program_config)
        if smpte:
            smpte_wrapper(f'{dolby_digital_plus}', 'ec3')

    elif program_config:
        change_program_config(
            f'{STD_IO_LOCATION}/flight_audio.wav', program_config)
        if smpte:
            smpte_wrapper('flight_audio.wav', 'wav')


if __name__ == '__main__':
    main()
