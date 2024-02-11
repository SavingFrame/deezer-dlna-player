import {api} from '../api';
import {Track} from "./types";
import {GetFavouriteTracksQuery} from "../playerWebsocket/types";

export const tracksApi = api.injectEndpoints({
    endpoints: (builder) => ({
        getFavouriteTracks: builder.query<Track[], GetFavouriteTracksQuery>({
            query: ({limit, ordering}) => ({
                url: '/api/v1/integrations/deezer/tracks/favorites',
                method: 'GET',
                params: {limit: limit || 6, ordering: ordering || 'asc'}
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

