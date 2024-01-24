import {api} from "../api";
import {ArtistListData, DetailedArtistData, TrackSchema, ArtistAlbumData} from "./types";


export const artistApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getArtists: builder.query<ArtistListData[], number | void>({
            query: (limit) => ({
                url: '/api/v1/integrations/deezer/artists',
                method: 'GET',
                params: {limit: limit || 6}
            }),
        }),
        getArtist: builder.query<DetailedArtistData, number>({
            query: (id) => ({
                url: `/api/v1/integrations/deezer/artists/${id}`,
                method: 'GET',
            }),
        }),
        getArtistAlbums: builder.query<ArtistAlbumData[], number>({
            query: (id) => ({
                url: `/api/v1/integrations/deezer/artists/${id}/albums`,
                method: 'GET',
            }),
        }),
        getArtistTopTracks: builder.query<TrackSchema[], number>({
            query: (id) => ({
                url: `/api/v1/integrations/deezer/artists/${id}/top`,
                method: 'GET',
            }),
        }),
    }),
});

export const {
    useGetArtistsQuery,
    useGetArtistQuery,
    useGetArtistAlbumsQuery,
    useGetArtistTopTracksQuery
} = artistApi;
