import React from 'react';
import {Card, CardMedia, CardContent, Typography, TextField, Grid, IconButton, CircularProgress} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import {useGetPlaylistsQuery} from "../services/playlistService";
import {useGetArtistsQuery} from "../services/artistService";
import {useGetFavouriteTracksQuery,} from "../services/tracksService";
import {useWebSocketContext} from "../providers/WebSocketProvider";
import {WebSocketValues} from "../services/playerWebsocket";



interface ItemProps {
    title: string;
    description?: string;
    imageUrl: string;
    id: number;
}

const ItemCard: React.FC<ItemProps> = ({title, description, imageUrl, id}) => {
    const {actionPlayTrack}: WebSocketValues = useWebSocketContext();

    const handlePlayTrack = (trackId: number) => {
        console.log('11')
        actionPlayTrack(trackId);
    };
    return (
        <Card style={{margin: 8, width: 250, height: 250, position: 'relative'}}>
            <CardMedia
                style={{height: '100%', width: '100%', position: 'absolute', top: 0, left: 0}}
                image={imageUrl}
                title={title}
            />
            <CardContent style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                textAlign: 'center'
            }}>
                <Typography variant="h6" component="h2" style={{color: 'white'}}>
                    {title}
                </Typography>
                {description && <Typography color="textSecondary">{description}</Typography>}
            </CardContent>
            <IconButton
                aria-label="play"
                onClick={() => handlePlayTrack(id)}
                style={{
                    position: 'absolute',
                    bottom: 10,
                    left: '50%',
                    transform: 'translateX(-50%)',
                    backgroundColor: 'white'
                }}
            >
                <PlayArrowIcon color="primary"/>
            </IconButton>
        </Card>
    )
};

const MainPage: React.FC = () => {
    const {data: playlistsData, isLoading: playlistIsLoading} = useGetPlaylistsQuery();
    // const playlists = [{title: 'Playlist 1', description: 'Description 1', imageUrl: 'playlist-image-url'}];
    const {data: artistsData, isLoading: artistsIsLoading} = useGetArtistsQuery();
    const {data: tracksData, isLoading: tracksIsLoading} = useGetFavouriteTracksQuery();

    // handle play track button click


    return (
        <div style={{padding: 16}}>
            <TextField fullWidth label="Search Music" variant="outlined" style={{marginBottom: 16}}/>

            <section>
                <Typography variant="h4" component="h1">Your Last Playlists</Typography>
                {playlistIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container>
                        {playlistsData?.map((playlist, index) => (
                            <Grid item xs={4} sm={2} md={2} key={index}>
                                <ItemCard id={playlist.id}
                                          title={playlist.title} description={playlist.nb_tracks + ' tracks'}
                                          imageUrl={playlist.picture_medium}/>
                            </Grid>
                        ))}
                    </Grid>
                )}
            </section>

            <section>
                <Typography variant="h4" component="h1">Favoruite artists</Typography>
                {artistsIsLoading ? (
                    <CircularProgress/>
                ) : (
                    <Grid container>
                        {artistsData?.map((artist, index) => (
                            <Grid item xs={4} sm={2} md={2} key={index}>
                                <ItemCard title={artist.name} id={artist.id}
                                          imageUrl={artist.picture_medium}/>
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
                    <Grid container>
                        {tracksData?.map((track, index) => (
                            <Grid item xs={4} sm={2} md={2} key={index}>
                                <ItemCard title={track.title} description={track.artist.name}
                                          imageUrl={track.album.cover_medium}
                                          id={track.id}/>
                            </Grid>
                        ))}
                    </Grid>
                )}
            </section>
        </div>
    );
};

export default MainPage;
