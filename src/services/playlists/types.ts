import exp from "node:constants";

export type PlaylistListData = {
    id: number;
    title: string;
    picture_medium: string;
    nb_tracks: number;
    duration: number;
    link: string;
};

type CreatorPlaylistData = {
    id: number;
    name: string;
}

type AlbumTrackSchema = {
    id: number;
    title: string;
    cover_medium: string;
}

type ArtistTrackSchema = {
    id: number;
    name: string;
}

type TrackSchema = {
    id: number;
    title: string;
    duration: number;
    rank: number;
    time_add: number;
    album: AlbumTrackSchema;
    artist: ArtistTrackSchema;
}

export type DetailPlaylistData = PlaylistListData & {
    picture_big: string;
    creation_date: string;
    creator: CreatorPlaylistData;
    tracks: TrackSchema[];
}
