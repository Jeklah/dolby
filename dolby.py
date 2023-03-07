import subprocess
import click

actions = ['Get audio from video',
           'Get Dolby from audio',
           'Decode dolby file to wav file.'
           ]


def get_audio_from_video(input_file: str, output_file: str) -> None:
    subprocess.run(
        f"ffmpeg -i {input_file} -vn -acodec copy {output_file}",
        shell=True
    )


def get_dolby_from_audio(input_file: str, output_file: str) -> None:
    subprocess.run(
        f"ffmpeg -i {input_file} -af acodec=ac3 {output_file}",
        shell=True
    )


def decode_dolby(input_file: str, output_file: str) -> None:
    subprocess.run(
        f"ffmpeg -i {input_file} -vn -acodec pcm_s16le -ar 48000 {output_file}",
        shell=True
    )


def main():
    dolby_channels = click.prompt(
        'Please enter the channels that the dolby pair you are interested in are on.', type=str)
    dolby_channels = dolby_channels.replace(' ', '')
    click.echo('It is worth remembering that this starts with an index of 0.')
    action_nums = click.IntRange(0, len(actions))
    for action in actions:
        menu = f'{action}'
        click.echo(f'{actions.index(action)} {menu}')

    click.echo('Please choose what you would like to do.')
    action_choice = click.prompt('Please choose an action', type=int)

    click.echo(f'You chose: {action_choice}: {actions[action_choice]}')
    click.echo(f'The channels you chose are: ')
    for chan in dolby_channels:
        click.echo(f'{chan}')
    click.echo(f'{len(dolby_channels)}')


if __name__ == '__main__':
    main()
