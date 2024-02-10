
export type DeviceType = {
    friendly_name: string;
    manufacturer: string;
    model_name: string;
    icon?: string | null;
    udn: string;
    url: string
}

export type PlayerType = {
    media_title: string;
    media_album: string;
    media_artist: string;
    media_position: number;
    media_duration: number;
    media_image_url?: string | null;
    volume_level: number;
    is_playing: boolean;
};

export type WebSocketValues = {
    playerData: PlayerType;
    deviceData: DeviceType[];
    currentDevice: DeviceType | null;
    isConnected: boolean;
    sendData: (data: any) => void; // Adjust the type of 'data' if needed
    actionSetDevice: (device: DeviceType) => void;
    actionPause: () => void;
    actionPlay: () => void;
    actionPlayTrack: (songId: number) => void;
    actionPlayAlbum: (albumId: number, startFrom: number | null) => void;
    actionPlayPlaylist: (playlistId: number, startFrom: number | null) => void;
    actionPlayArtistTopTracks: (artistId: number, startFrom: number | null) => void;
    actionPlayFlow: () => void;
    actionPlayNext: () => void;
    actionPlayPrevious: () => void;
    reconnect: () => void;
};
