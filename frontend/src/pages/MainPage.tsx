import React from 'react';
import {Box, Button, CircularProgress, Grid, Stack, Typography} from '@mui/material';
import {useGetPlaylistsQuery} from "../services/playlists/playlistService";
import {useGetArtistsQuery} from "../services/artists/artistService";
import {useGetFavouriteTracksQuery,} from "../services/tracks/tracksService";
import {useGetAlbumsQuery} from "../services/albums/albumService";
import ItemCard from "../components/Dashboard/ItemCard";
import FlowBanner from "../components/Dashboard/FlowBanner";
import useDocumentTitle from "../services/headerTitle/useHeaderTitle";
import Search from "../components/Search";
import {useNavigate} from "react-router-dom";

interface ShowAllButtonProps {
    onClick: () => void; // Define the type of the onClick prop
}


const MainPage: React.FC = () => {
    useDocumentTitle('Main Page');
    const navigate = useNavigate();
    const {data: playlistsData, isLoading: playlistIsLoading} = useGetPlaylistsQuery();
    const {data: artistsData, isLoading: artistsIsLoading} = useGetArtistsQuery();
    const {data: tracksData, isLoading: tracksIsLoading} = useGetFavouriteTracksQuery({});
    const {data: albumsData, isLoading: albumsIsLoading} = useGetAlbumsQuery();


    const ShowAllButton: React.FC<ShowAllButtonProps> = ({onClick}) => (
        <Button onClick={onClick} sx={{fontSize: '1.1rem'}}>Show all</Button>
    );


    return (
        <Box sx={{padding: 2}}>
            <Search/>
            <FlowBanner/>


            <Box sx={{marginBottom: 4, marginTop: 4}}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{marginBottom: 2}}>
                    <Typography variant="h4" component="h2">Your Last Playlists</Typography>
                    {playlistsData?.length === 6 && <ShowAllButton onClick={() => { /* Navigate to playlist detail view */
                    }}/>}
                </Stack>


                {playlistIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container spacing={2}>
                        {playlistsData?.map((playlist, index) => (
                            <ItemCard
                                id={playlist.id}
                                title={playlist.title}
                                description={playlist.nb_tracks + ' tracks'}
                                description2={'by ' + playlist.creator.name}
                                imageUrl={playlist.picture_medium}
                                type={"playlist"}
                            />
                        ))}
                    </Grid>
                )}
            </Box>

            <Box sx={{marginBottom: 4}}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{marginBottom: 2}}>
                    <Typography variant="h4" component="h2">Favorite Artists</Typography>
                    {artistsData?.length === 6 && <ShowAllButton onClick={() => {
                        navigate('/artists')
                    }}/>}
                </Stack>

                {artistsIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container spacing={2}>
                        {artistsData?.map((artist, index) => (
                            <ItemCard
                                title={artist.name}
                                id={artist.id}
                                imageUrl={artist.picture_medium}
                                type={"artist"}
                            />
                        ))}
                    </Grid>
                )}
            </Box>

            <Box sx={{marginBottom: 4}}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{marginBottom: 2}}>
                    <Typography variant="h4" component="h2">Favorite Tracks</Typography>
                    {tracksData?.length === 6 && <ShowAllButton onClick={() => {
                        navigate('/favorite-tracks')
                    }}/>}
                </Stack>

                {tracksIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container spacing={2}>
                        {tracksData?.map((track, index) => (
                            <ItemCard
                                title={track.title}
                                description={track.artist.name}
                                imageUrl={track.album.cover_medium}
                                id={track.id}
                                type={"track"}
                                extra={{albumId: track.album.id}}
                            />
                        ))}
                    </Grid>
                )}
            </Box>

            <Box sx={{marginBottom: 4}}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{marginBottom: 2}}>
                    <Typography variant="h4" component="h2">Albums</Typography>
                    {albumsData?.length === 6 && <ShowAllButton onClick={() => {
                        navigate('/albums')
                    }}/>}
                </Stack>
                {albumsIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container>
                        {albumsData?.map((album, index) => (
                            <ItemCard
                                title={album.title}
                                description={album.artist.name}
                                imageUrl={album.cover_medium}
                                id={album.id}
                                type={"album"}
                            />
                        ))}
                    </Grid>
                )}
            </Box>

        </Box>
    );
};

export default MainPage;
