
export type ArtistListData = {
    id: number;
    name: string;
    picture_medium: string;
    link: string;
    nb_fan: number;
    nb_album: number;
};

export type DetailedArtistData = {
    id: number;
    name: string;
    link: string;
    picture_medium: string;
    picture_big: string;
    nb_fan: number;
    nb_album: number;
}

export type ArtistAlbumData = {
    id: number;
    title: string;
    cover_medium: string;
    cover_big: string;
    release_date: string;
    fans: number;
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

export type TrackSchema = {
    id: number;
    title: string;
    duration: number;
    rank: number;
    album: AlbumTrackSchema;
    artist: ArtistTrackSchema;
}
