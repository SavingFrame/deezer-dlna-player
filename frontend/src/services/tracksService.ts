import {api} from './api';

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
};

export const tracksApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getFavouriteTracks: builder.query<Track[], number | void>({
            query: (limit) => ({
                url: '/api/v1/integrations/deezer/tracks/favorites',
                method: 'GET',
                params: {limit: limit || 6}
            }),
        }),
        playTrack: builder.mutation<void, number>({
            query: (id) => ({
                url: `/api/v1/integrations/deezer/tracks/${id}/play`,
                method: 'GET',
            }),
        }),
    }),
});

export const {useGetFavouriteTracksQuery, usePlayTrackMutation} = tracksApi;

