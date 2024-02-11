export type Album = {
    id: number;
    title: string;
    cover_medium: string;
};
export type ArtistType = {
    id: number;
    name: string;
    picture_medium: string;
};
export type Track = {
    id: number;
    title: string;
    duration: number;
    artist: ArtistType;
    album: Album;
    time_add: string;
};
