import {api} from "../api";
import {AlbumDetailType, AlbumType} from "./types";


export const albumApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getAlbums: builder.query<AlbumType[], number | void>({
            query: (limit) => ({
                url: '/api/v1/integrations/deezer/albums',
                method: 'GET',
                params: {limit: limit || 6}
            }),
        }),
        getAlbum: builder.query<AlbumDetailType, number>({
            query: (id) => ({
                url: `/api/v1/integrations/deezer/albums/${id.toString()}`,
                method: 'GET',
            }),
        }),
    }),
});

export const {useGetAlbumsQuery, useGetAlbumQuery} = albumApi;
