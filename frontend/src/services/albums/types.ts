type ArtistType = {
    id: number;
    name: string;
    picture_medium: string;
    // link: string;
};

export type AlbumType = {
    id: number;
    title: string;
    link: string;
    cover_medium: string;
    artist: ArtistType;
    nb_tracks: number;
    duration: number;
    release_date: string;
};

export type AlbumTrackType = {
    id: number;
    title: string;
    duration: number;
};

export type AlbumDetailType = AlbumType & {
    cover_big: string;
    fans: number | null;
    tracks: AlbumTrackType[]
};
