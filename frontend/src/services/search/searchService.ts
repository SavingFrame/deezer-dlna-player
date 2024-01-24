
import {api} from '../api';
import {TrackData, AlbumData, ArtistData} from "./types";


export const playlistApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getSearchTracks: builder.query<TrackData[], {query: string, limit? : number | undefined, offset?: number | undefined}>({
            query: ({query, limit, offset}) => ({
                url: `/api/v1/integrations/deezer/search/tracks/${query}`,
                method: 'GET',
                params: {
                    limit: limit || 6,
                    offset: offset || 0
                }
            }),
        }),
        getSearchAlbums: builder.query<AlbumData[], {query: string, limit? : number | undefined, offset?: number | undefined}>({
            query: ({query, limit, offset}) => ({
                url: `/api/v1/integrations/deezer/search/albums/${query}`,
                method: 'GET',
                params: {
                    limit: limit || 6,
                    offset: offset || 0
                }
            }),
        }),
        getSearchArtists: builder.query<ArtistData[], {query: string, limit? : number | undefined, offset?: number | undefined}>({
            query: ({query, limit, offset}) => ({
                url: `/api/v1/integrations/deezer/search/artists/${query}`,
                method: 'GET',
                params: {
                    limit: limit || 6,
                    offset: offset || 0
                }
            }),
        }),
    }),
});

export const {
    useGetSearchTracksQuery,
    useGetSearchAlbumsQuery,
    useGetSearchArtistsQuery
} = playlistApi;

