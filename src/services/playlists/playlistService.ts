import {api} from '../api';
import {PlaylistListData, DetailPlaylistData} from "./types";


export const playlistApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getPlaylists: builder.query<PlaylistListData[], number | void>({
            query: (limit) => ({
                url: '/api/v1/integrations/deezer/playlists',
                method: 'GET',
                params: {limit: limit || 6}
            }),
        }),
        getPlaylist: builder.query<DetailPlaylistData, number>({
            query: (id) => ({
                url: `/api/v1/integrations/deezer/playlists/${id}`,
                method: 'GET',
            }),
        })
    }),
});

export const {useGetPlaylistsQuery, useGetPlaylistQuery} = playlistApi;

