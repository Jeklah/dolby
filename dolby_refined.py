#!/bin/env python3

import subprocess
import click

DDP_ENC_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/DDP_Pro_Enc_v3.10.2_x86_32.exe'
SMPTE_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/smpte.exe'
STD_IO_LOCATION = '/media/sf_Shared_Folder/dolby/2023'


def create_dolby(input_file: str, output_file: str, mode: int) -> None:
    """
    Command to create Dolby Digital or Dolby Digital Plus files.

    :param input_file: String to be used as the input file name.
    :param output_file: String to be used as the output file name.
    :param mode: Integer to be used as the Dolby Digital mode.
    """
    extension = 'ac3' if mode == 1 else 'ec3'
    command = f'wine {DDP_ENC_LOCATION} -md{mode} -i{input_file} -o{output_file}.{extension}'
    subprocess.call(command, shell=True)


def smpte_wrapper(input_file: str, filetype: str) -> None:
    """
    Wrap .ac3 or .ec3 file as SMPTE .wav file.

    :param input_file: String to be used as the input file.
    :param filetype: String to be used as the filtype of the input file.
    """
    smpte_wrap = f'wine {SMPTE_LOCATION} -i{input_file}.{filetype} -o{input_file}.wav'
    subprocess.call(smpte_wrap, shell=True)


def change_program_config(input_file: str, program_config: int, output_file="") -> None:
    """
    Change the program configuration/speaker layout of a Dolby file.

    NOTE: Modes -a0, -a1 and -a2 require -l0 (LFE disabled).

    :param input_file: String to be used as the input file.
    :param program_config: Number used to signify which program configuration is desired.
    :param output_file: String to be used as the output file.
    """
    filepath_length = len(input_file.split('/'))
    filename = input_file.split('/')[filepath_length - 1].split('.')[0]
    filetype = input_file.split('/')[filepath_length - 1].split('.')[1]
    if output_file == "":
        output_file = filename
    lfe_flag = '-l0' if program_config in {1, 2} else '-l1'
    command = f'wine {DDP_ENC_LOCATION} -i{input_file} -o./{output_file}.{filetype} -a{program_config} {lfe_flag}'
    subprocess.call(command, shell=True)


@click.command()
@click.option('--codec', '-c', help='Create a Dolby Digital (ac3) or Dolby Digital Plus (ec3) file', type=click.Choice(['ac3', 'ec3']))
@click.option('--program_config', '-pc', help='Change the program configuration/speaker layout', type=int)
@click.option('--smpte', '-s', help='Wrap an ac3 or ec3 file up as SMPTE wav file.', is_fla=True, default=False)
@click.option('--input_file', '-i', help='String to be used as the input file', type=str)
@click.option('--output_file', '-o', help='String to be used as the output file', type=str)
@click.option('--mode', '-m', help='Integer to select whether to create Dolby Digital or Dolby Digital Plus', type=int)
def main(codec: str, program_config: int, smpte: bool, input_file: str, output_file: str, mode: int) -> None:
    input_file = input_file or f'{STD_IO_LOCATION}/flight_audio.wav'
    output_file = output_file or f'{STD_IO_LOCATION}/{input_file.split("/")[len(input_file.split("/")) -1].split(".")[0]}'

    if codec == 'ac3':
        create_dolby(input_file, output_file, mode=0)
    elif codec == 'ec3':
        create_dolby(input_file, output_file, mode=1)

    if program_config:
        change_program_config(f'{output_file}.{codec}', program_config)

    if smpte:
        smpte_wrapper(f'{output_file}', codec)


if __name__ == '__main__':
    main()
