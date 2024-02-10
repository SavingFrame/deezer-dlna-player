from deezer_integration.services.deezer import deezer_integration
from dlna.services.dlna_device import DlnaDevice
from library.album import Album
from library.playlist import Playlist
from library.track import Track
from player_worker.utils import get_dlna_device
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
    message = data.get('message')
    album_id = message.get('album_id')
    start_from = message.get('start_from')
    album = await Album.from_deezer_by_id(album_id, dlna_device)
    await album.play(start_from)


@task(queue_key='player.pause')
@get_dlna_device
async def player_pause(dlna_device: DlnaDevice, data):
    await dlna_device.pause()


@task(queue_key='player.play')
@get_dlna_device
async def player_play(dlna_device: DlnaDevice, data):
    await dlna_device.play()


@task(queue_key='player.play_artist_top_tracks')
@get_dlna_device
async def player_play_artist_top(dlna_device: DlnaDevice, data):
    message = data.get('message')
    artist_id = message.get('artist_id')
    start_from = message.get('start_from')
    client = deezer_integration
    tracks_info = await client.get_artist_top(artist_id)
    tracks = [
        await Track.from_deezer_api_track_info(
            track_info,
            dlna_device=dlna_device,
            _deezer_client=client.async_client
        )
        for track_info in tracks_info
    ]
    player_queue = await dlna_device.get_player_queue()
    await player_queue.set_queue(tracks, start_from=start_from)
    await player_queue.play()


@task(queue_key='player.next')
@get_dlna_device
async def player_next(dlna_device: DlnaDevice, data):
    queue = await dlna_device.get_player_queue()
    await queue.play_next()


@task(queue_key='player.previous')
@get_dlna_device
async def player_previous(dlna_device: DlnaDevice, data):
    queue = await dlna_device.get_player_queue()
    await queue.play_previous()


@task(queue_key='player.play_playlist')
@get_dlna_device
async def player_play_playlist(dlna_device: DlnaDevice, data):
    message = data.get('message')
    playlist_id = message.get('playlist_id')
    start_from = message.get('start_from')
    playlist = await Playlist.from_deezer_by_id(playlist_id, dlna_device)
    await playlist.play(start_from=start_from)


@task(queue_key='player.play_flow')
@get_dlna_device
async def player_play_flow(dlna_device: DlnaDevice, data):
    client = deezer_integration
    tracks_info = await client.get_flow_tracks()
    tracks = [
        await Track.from_deezer_api_track_info(
            track_info,
            dlna_device=dlna_device,
            _deezer_client=client.async_client
        )
        for track_info in tracks_info
    ]
    player_queue = await dlna_device.get_player_queue()
    await player_queue.set_queue(tracks)
    await player_queue.play()
