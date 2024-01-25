import React from "react";
import {Card, CardActionArea, CardMedia, CardContent, Typography, Box, IconButton, Grid} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";
import {useNavigate} from "react-router-dom";
import {useWebSocketContext} from "../../providers/WebSocketProvider";

interface ItemProps {
    title: string;
    description?: string;
    description2?: string;
    imageUrl: string;
    id: number;
    type: "track" | "album" | "playlist" | "artist";
    extra?: any;
}

const ItemCard: React.FC<ItemProps> = ({title, description, imageUrl, id, type, description2, extra}) => {
    const navigate = useNavigate();
    const {actionPlayTrack, actionPlayAlbum, playerData, actionPause} = useWebSocketContext();

    const navigateToDetail = () => {
        if (type === "track") {
            navigate(`/album/${extra.albumId}`);
        } else {
            navigate(`/${type}/${id}`);
        }
    };

    const checkIfPlaying = () => {
        // Adjust this condition based on how you determine if the item is currently playing
        return playerData.media_album === title;
    };

    const handlePlay = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.stopPropagation();
        if (checkIfPlaying()) {
            actionPause();
        } else {
            type === "track" ? actionPlayTrack(id) : actionPlayAlbum(id, null);
        }
    };

    return (
        <Grid item xs={12} sm={6} md={4} lg={3} xl={2}>
            <Card sx={{ width: '100%', m: 'auto', position: 'relative' }} onClick={navigateToDetail}>
                <CardActionArea>
                    <CardMedia
                        component="img"
                        height="200"
                        image={imageUrl}
                        alt={title}
                    />
                    <CardContent>
                        <Typography gutterBottom variant="h6" component="div" noWrap>
                            {title}
                        </Typography>
                        {description && <Typography variant="body2" color="text.secondary">
                            {description}
                        </Typography>}
                        {description2 && <Typography variant="body2" color="text.secondary">
                            {description2}
                        </ Typography>}
                    </CardContent>
                </CardActionArea>
                <Box sx={{position: 'absolute', bottom: 0, right: 0, zIndex: 2, p: 1}}>
                    <IconButton
                        aria-label={checkIfPlaying() ? 'Pause' : 'Play'}
                        onClick={handlePlay}
                        size="large"
                        sx={{color: 'primary.main'}}
                    >
                        {checkIfPlaying() ? <PauseIcon/> : <PlayArrowIcon/>}
                    </IconButton>
                </Box>
            </Card>
        </Grid>
    );
};

export default ItemCard;
