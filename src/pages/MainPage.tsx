import React, {useEffect, useState} from 'react';
import {CircularProgress, Dialog, DialogContent, DialogTitle, Grid, TextField, Typography} from '@mui/material';
import {useGetPlaylistsQuery} from "../services/playlists/playlistService";
import {useGetArtistsQuery} from "../services/artists/artistService";
import {useGetFavouriteTracksQuery,} from "../services/tracksService";
import {useGetAlbumsQuery} from "../services/albums/albumService";
import ItemCard from "../components/Dashboard/ItemCard";
import FlowBanner from "../components/Dashboard/FlowBanner";
import useDocumentTitle from "../services/headerTitle/useHeaderTitle";
import Search from "../components/Dashboard/Search";



const MainPage: React.FC = () => {
    useDocumentTitle('Main Page');
    const {data: playlistsData, isLoading: playlistIsLoading} = useGetPlaylistsQuery();
    const {data: artistsData, isLoading: artistsIsLoading} = useGetArtistsQuery();
    const {data: tracksData, isLoading: tracksIsLoading} = useGetFavouriteTracksQuery();
    const {data: albumsData, isLoading: albumsIsLoading} = useGetAlbumsQuery();

    const [searchQuery, setSearchQuery] = useState('');
    const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('');
    const [isSearchDialogOpen, setSearchDialogOpen] = useState(false);


    useEffect(() => {
        const handler = setTimeout(() => {
            if (searchQuery.trim() !== '') {
                setDebouncedSearchQuery(searchQuery);
                setSearchDialogOpen(true);
            } else {
                setSearchDialogOpen(false);
            }
        }, 3000);

        return () => clearTimeout(handler);
    }, [searchQuery]);

    const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
    };
    const handleCloseSearchDialog = () => {
        setSearchDialogOpen(false);
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            // Logic to execute on Enter key press
            if (searchQuery.trim() !== '') {
                setDebouncedSearchQuery(searchQuery);
                setSearchDialogOpen(true);
            }
        }
    };





    return (
        <div style={{padding: 16}}>
            <TextField
                fullWidth
                label="Search Music"
                variant="outlined"
                style={{ marginBottom: 16 }}
                value={searchQuery}
                onChange={handleSearchChange}
                onKeyDown={handleKeyDown}
            />

            <FlowBanner />

            <Dialog open={isSearchDialogOpen} onClose={handleCloseSearchDialog} maxWidth="md" fullWidth>
                <DialogTitle>Search Results</DialogTitle>
                <DialogContent>
                    {debouncedSearchQuery && <Search searchQuery={debouncedSearchQuery} />}
                </DialogContent>
            </Dialog>



            <section>
                <Typography variant="h4" component="h1">Your Last Playlists</Typography>
                {playlistIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container spacing={2}>
                        {playlistsData?.map((playlist, index) => (
                            <Grid item xs={6} sm={4} md={3} lg={2} xl={1} key={index}>
                                <ItemCard
                                    id={playlist.id}
                                    title={playlist.title}
                                    description={playlist.nb_tracks + ' tracks'}
                                    imageUrl={playlist.picture_medium}
                                    type={"playlist"}
                                />
                            </Grid>
                        ))}
                    </Grid>
                )}
            </section>

            <section>
                <Typography variant="h4" component="h1">Favorite artists</Typography>
                {artistsIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container spacing={2}>
                        {artistsData?.map((artist, index) => (
                            <Grid item xs={6} sm={4} md={3} lg={2} xl={1} key={index}>
                                <ItemCard
                                    title={artist.name}
                                    id={artist.id}
                                    imageUrl={artist.picture_medium}
                                    type={"artist"}
                                />
                            </Grid>
                        ))}
                    </Grid>
                )}
            </section>

            <section>
                <Typography variant="h4" component="h1">Favorite Tracks</Typography>
                {tracksIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container spacing={2}>
                        {tracksData?.map((track, index) => (
                            <Grid item xs={6} sm={4} md={3} lg={2} xl={1} key={index}>
                                <ItemCard
                                    title={track.title}
                                    description={track.artist.name}
                                    imageUrl={track.album.cover_medium}
                                    id={track.id}
                                    type={"track"}
                                    extra={{albumId: track.album.id}}
                                />
                            </Grid>
                        ))}
                    </Grid>
                )}
            </section>

            <section>
                <Typography variant="h4" component="h1">Albums</Typography>
                {albumsIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container>
                        {albumsData?.map((album, index) => (
                            <Grid item xs={6} sm={4} md={3} lg={2} xl={1} key={index}>
                                <ItemCard
                                    title={album.title}
                                    description={album.artist.name}
                                    imageUrl={album.cover_medium}
                                    id={album.id}
                                    type={"album"}
                                />
                            </Grid>
                        ))}
                    </Grid>
                )}
            </section>

        </div>
    );
};

export default MainPage;
