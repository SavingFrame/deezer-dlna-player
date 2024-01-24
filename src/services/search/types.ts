// Track search types
type TrackArtistData = {
    id: number;
    name: string;
}

type TrackAlbumData = {
    id: number;
    title: string;
    cover_medium: string;
}

export type TrackData = {
    id: number;
    title: string;
    duration: number;
    artist: TrackArtistData;
    album: TrackAlbumData;
}

// Album search types

export type AlbumData = {
    id: number;
    title: string;
    cover_medium: string;
    nb_tracks: number;
    record_type: string;
    artist: TrackArtistData;
}

// Artist search types

export type ArtistData = {
    id: number;
    name: string;
    picture_medium: string;
    nb_album: number;
    nb_fan: number;
}
