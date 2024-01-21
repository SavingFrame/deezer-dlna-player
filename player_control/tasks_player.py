from dlna.services.dlna_device import DlnaDevice
from library.album import Album
from library.track import Track
from player_control.utils import get_dlna_device
from utils.task_worker.task_registry import task


@task(queue_key='player.play_song')
@get_dlna_device
async def player_play_song(dlna_device: DlnaDevice, data):
    track_id = data.get('message')
    track = await Track.from_deezer_by_id(track_id, dlna_device)
    await track.play()


@task(queue_key='player.play_album')
@get_dlna_device
async def player_play_album(dlna_device: DlnaDevice, data):
    album_id = data.get('message')
    album = await Album.from_deezer_by_id(album_id, dlna_device)
    await album.play()


@task(queue_key='player.pause')
@get_dlna_device
async def player_pause(dlna_device: DlnaDevice, data):
    await dlna_device.pause()


@task(queue_key='player.play')
@get_dlna_device
async def player_play(dlna_device: DlnaDevice, data):
    await dlna_device.play()


@task(queue_key='device.set_volume')
@get_dlna_device
async def player_set_volume(dlna_device: DlnaDevice, data):
    volume = data.get('message')
    await dlna_device.set_volume(volume)


@task(queue_key='internal.set_next_track', skip_logging=True)
@get_dlna_device
async def player_set_next_track(dlna_device: DlnaDevice, data):
    print('data', data)
    player_queue = await dlna_device.get_player_queue()
    await player_queue.set_next_song()


@task(queue_key='internal.upnp_event', skip_logging=True)
@get_dlna_device
async def player_upnp_event(dlna_device: DlnaDevice, data):
    message = data.get('message')
    service_id = message.get('service_id')
    state_variables = message.get('state_variables')
    dlna_device.dmr_device.on_queue_event(service_id, state_variables)
