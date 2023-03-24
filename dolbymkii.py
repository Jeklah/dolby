import subprocess
import os
import click


DDP_ENC_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/DDP_Pro_Enc_v3.10.2_x86_32.exe'
SMPTE_LOCATION = '/media/sf_Shared_Folder/dolby/2023/dolby_legacy_ref_encoder/Dolby_Digital_Plus_Pro_System_Implementation_Kit_v7.6/Test_Tools/smpte.exe'


def create_dolby_digital(input_file: str, output_file: str) -> None:
    """
    Command to create Dolby Digital Plus files.

    :param str: String to be used as the input file name.
    :param str: String to be used as the output file name.
    """
    command = f'wine "{DDP_ENC_LOCATION}" -md1 -i"{input_file}" -o"{output_file}.ac3"'
    print('about to run wine')
    subprocess.call(command, shell=True)
    print('wine has been run')
    print('wrapping in smpte')
    smpte_wrap = f'wine "{SMPTE_LOCATION}" -i"{output_file}.ac3" -o"{output_file}.wav"'
    subprocess.call(smpte_wrap, shell=True)
    print('smpte wrapping complete')


def create_dolby_digital_plus(input_file: str, output_file: str) -> None:
    """
    Command to create Dolby Digital Plus files.

    :param str: String to be used as the input file name.
    :param str: String to be used as the output file name.
    """
    print('about to run Dolby ')
    command = f'wine "{DDP_ENC_LOCATION}" -md0 -i"{input_file}" -o"{output_file}.ec3"'
    subprocess.call(command, shell=True)
    print('wine has been run')
    print('wrapping in smpte')
    smpte_wrap = f'wine "{SMPTE_LOCATION}" -i"{output_file}.ec3" -o"{output_file}.wav"'
    subprocess.call(smpte_wrap, shell=True)
    print('smpte wrapping complete')


def change_program_config(input_file: str, prog_config: int) -> None:
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
    filepath_length = len(input_file.split('/'))
    filename = input_file.split('/')[filepath_length - 1].split('.')[0]
    print(f'{filename}')
    print('starting changing program config')
    print(f'{input_file}')
    if prog_config in {1, 2}:
        command = f'wine "{DDP_ENC_LOCATION}" -md0 -i"{input_file}" -o./"{filename}.ec3" -a"{prog_config}" -l0'
    else:
        command = f'wine "{DDP_ENC_LOCATION}" -i"{input_file}" -o./"{filename}" -a"{prog_config}" -l1'
    subprocess.call(command, shell=True)


@click.command()
@click.option('--dolby_digital', '-cdd', help='Create a Dolby Digital file', type=str)
@click.option('--dolby_digital_plus', '-cddp', help='Create a Dolby Digital Plus file', type=str)
@click.option('--program_config', '-pc', help='Change the program configuration/speaker layout', type=int)
def main(dolby_digital: str, dolby_digital_plus: str, program_config: int):
    if dolby_digital:
        create_dolby_digital(
            '/media/sf_Shared_Folder/dolby/2023/flight_audio.wav', dolby_digital)
    if dolby_digital_plus:
        create_dolby_digital_plus(
            '/media/sf_Shared_Folder/dolby/2023/flight_audio.wav', dolby_digital_plus)
    if program_config:
        change_program_config(
            '/media/sf_Shared_Folder/dolby/2023/flight_audio.wav', program_config)


if __name__ == '__main__':
    main()
