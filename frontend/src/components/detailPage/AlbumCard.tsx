import React from 'react';
import {Grid, Card, CardActionArea, CardContent, CardMedia, Typography, Box, IconButton} from '@mui/material';
import {ArtistAlbumData} from "../../services/artists/types";
import {useNavigate} from "react-router-dom";
import {WebSocketValues} from "../../services/playerWebsocket/types";
import {useWebSocketContext} from "../../providers/WebSocketProvider";
import PauseIcon from "@mui/icons-material/Pause";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

type ArtistAlbumsProps = {
    albums: ArtistAlbumData[];
};

const AlbumCard: React.FC<ArtistAlbumsProps> = ({albums}) => {
    const navigate = useNavigate();
    const {actionPlayAlbum, actionPause, playerData}: WebSocketValues = useWebSocketContext();
    const handleAlbumClick = (albumId: number) => {
        // Redirect to the album page
        navigate(`/album/${albumId}`);
    };

    const checkIfPlaying = (albumName: string) => {
        // Check if the album is currently playing
        return albumName === playerData.media_album;
    }


    return (
        <Box sx={{flexGrow: 1, padding: 2}}>
            <Grid container spacing={4}>
                {albums.map((album) => (
                    <Grid item xs={12} sm={6} md={4} lg={3} key={album.id}>
                        <Card sx={{maxWidth: 345, m: 'auto', position: 'relative'}}>
                            <CardActionArea onClick={(event) => handleAlbumClick(album.id)}>
                                <CardMedia
                                    component="img"
                                    height="140"
                                    image={album.cover_medium}
                                    alt={album.title}
                                />
                                <CardContent>
                                    <Typography gutterBottom variant="h6" component="div" noWrap>
                                        {album.title}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Released: {album.release_date}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        {album.fans.toLocaleString()} fans
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        {album.fans.toLocaleString()} fans
                                    </Typography>
                                </CardContent>
                            </CardActionArea>
                            {/* Moved the Box with IconButton outside the CardActionArea */}
                            <Box sx={{position: 'absolute', bottom: 0, right: 0, zIndex: 2, p: 1}}>
                                <IconButton
                                    aria-label={checkIfPlaying(album.title) ? 'Pause' : 'Play'}
                                    onClick={(e) => {
                                        e.stopPropagation(); // Prevent the CardActionArea click
                                        checkIfPlaying(album.title) ? actionPause() : actionPlayAlbum(album.id, null);
                                    }}
                                    size="large" // Adjust the size as needed
                                    sx={{color: 'primary.main'}} // Adjust the color to make the icon stand out
                                >
                                    {checkIfPlaying(album.title) ? <PauseIcon/> : <PlayArrowIcon/>}
                                </IconButton>
                            </Box>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );


};

export default AlbumCard;
