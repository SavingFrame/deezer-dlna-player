import React from "react";
import {WebSocketValues} from "../../services/playerWebsocket/types";
import {useWebSocketContext} from "../../providers/WebSocketProvider";
import {useNavigate} from "react-router-dom";
import {Card, CardContent, CardMedia, IconButton, Typography} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

interface ItemProps {
    title: string;
    description?: string;
    imageUrl: string;
    id: number;
    type: "track" | "album" | "playlist" | "artist";
    extra?: any;
}

const ItemCard: React.FC<ItemProps> = ({title, description, imageUrl, id, type, extra}) => {
    const {actionPlayTrack, actionPlayAlbum}: WebSocketValues = useWebSocketContext();
    const navigate = useNavigate();

    const navigateToDetail = () => {
        if (type === "track") {
            navigate(`/album/${extra.albumId}`); // Redirect to the detail page
        } else {
            navigate(`/${type}/${id}`); // Redirect to the detail page
        }
    };
    const handlePlay = (event: React.MouseEvent<HTMLButtonElement>, instanceId: number) => {
        event.stopPropagation(); // Prevents redirect when the play button is clicked
        if (type === "track") {
            actionPlayTrack(id);
        } else if (type === "album") {
            actionPlayAlbum(id, null);
        }
    }

    return (
        <Card style={{position: 'relative', width: '100%'}} onClick={navigateToDetail}>
            <div style={{paddingTop: '100%'}}></div>
            {/* Aspect ratio box */}
            <CardMedia
                style={{position: 'absolute', top: 0, bottom: 0, left: 0, right: 0}}
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
                onClick={(event) => handlePlay(event, id)}
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

export default ItemCard;
