import {api} from './api';

export type PlaylistData = {
    id: number;
    title: string;
    picture_medium: string;
    nb_tracks: number;
    duration: number;
    link: string;
};

export const playlistApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getPlaylists: builder.query<PlaylistData[], number | void>({
            query: (limit) => ({
                url: '/api/v1/integrations/deezer/playlists',
                method: 'GET',
                params: { limit: limit || 6}
            }),
        }),
    }),
});

export const { useGetPlaylistsQuery } = playlistApi;

