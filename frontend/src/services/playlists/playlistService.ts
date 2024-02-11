import {api} from '../api';
import {PlaylistListData, DetailPlaylistData, GetPlaylistQuery} from "./types";


export const playlistApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getPlaylists: builder.query<PlaylistListData[], number | void>({
            query: (limit) => ({
                url: '/api/v1/integrations/deezer/playlists',
                method: 'GET',
                params: {limit: limit || 6}
            }),
        }),
        getPlaylist: builder.query<DetailPlaylistData, GetPlaylistQuery>({
            query: ({id, tracks_ordering}) => ({
                url: `/api/v1/integrations/deezer/playlists/${id}`,
                params: {tracks_ordering: tracks_ordering || 'asc'},
                method: 'GET',
            }),
        })
    }),
});

export const {useGetPlaylistsQuery, useGetPlaylistQuery} = playlistApi;

