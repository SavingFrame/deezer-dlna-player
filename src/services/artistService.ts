import {api} from "./api";


export type ArtistType = {
    id: number;
    name: string;
    picture_medium: string;
    link: string;
};

export const artistApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getArtists: builder.query<ArtistType[], number | void>({
            query: (limit) => ({
                url: '/api/v1/integrations/deezer/artists',
                method: 'GET',
                params: {limit: limit || 6}
            }),
        }),
    }),
});

export const {useGetArtistsQuery} = artistApi;
