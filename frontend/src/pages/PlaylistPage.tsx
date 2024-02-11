import React, {useState} from 'react';
import Header from "../components/detailPage/Header";
import SkeletonHeader from "../components/detailPage/SkeletonHeader";

import ItemList from "../components/detailPage/ItemList";
import SkeletonItemList from "../components/detailPage/SkeletonItemList";
import {useParams} from "react-router-dom";
import {Item} from "../components/detailPage/types";
import {useGetPlaylistQuery} from "../services/playlists/playlistService";
import {WebSocketValues} from "../services/playerWebsocket/types";
import {useWebSocketContext} from "../providers/WebSocketProvider";
import useDocumentTitle from "../services/headerTitle/useHeaderTitle";
import {Box, Grid, IconButton, Typography} from "@mui/material";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";

const PlaylistPage: React.FC = () => {
    useDocumentTitle('Playlist');
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const toggleSortOrder = () => {
        setSortOrder(prevOrder => prevOrder === 'asc' ? 'desc' : 'asc');
    };
    const {actionPlayPlaylist}: WebSocketValues = useWebSocketContext();
    const {id} = useParams<{ id: string }>();
    if (!id) {
        throw new Error("ID is not defined in the URL");
    }
    const playlistId = parseInt(id);

    const formatDuration = (duration: number) => {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };

    const {data: playlistData, isLoading: playlistIsLoading} = useGetPlaylistQuery({
        id: playlistId,
        tracks_ordering: sortOrder
    });
    const type = 'playlist';
    const items: Item[] = playlistData?.tracks.map(track => ({
        id: track.id,
        title: track.title,
        description: track.artist.name,
        column1: track.album.title,
        column2: new Date(track.time_add * 1000).toLocaleString(),
        column3: formatDuration(track.duration),
        coverUrl: track.album.cover_medium,
    })) || [];

    const handlePlayClick = (playlistId: number, startFrom: number) => {
        actionPlayPlaylist(playlistId, startFrom, sortOrder);
    };
    return (
        <Box sx={{padding: 2}}>
            {playlistIsLoading ? <SkeletonHeader/> :
                <Header title={playlistData!.title} description={playlistData!.creator.name}
                        imageUrl={playlistData!.picture_medium}/>}
            {playlistIsLoading ? <SkeletonItemList count={10}/> :
                (

                    <>
                        <Box sx={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', ml: 2}}>
                            <Grid container spacing={2} sx={{flex: 1, mr: 2, alignItems: 'center'}}>
                                <Grid item xs={1}>
                                    <Typography variant="button">#</Typography>
                                </Grid>
                                <Grid item xs={2} sx={{ mr: 6}}>
                                    <Typography variant="button">TRACK</Typography>
                                </Grid>
                                <Grid item xs={3}>
                                    <Typography variant="button">Album</Typography>
                                </Grid>
                                <Grid item xs>
                                    <Box sx={{display: 'flex', alignItems: 'center'}}>
                                        <Typography variant="button">ADDED</Typography>
                                        <IconButton onClick={toggleSortOrder} size="small">
                                            {sortOrder === 'asc' ? <ArrowUpwardIcon/> : <ArrowDownwardIcon/>}
                                        </IconButton>
                                    </Box>
                                </Grid>
                                <Grid item xs={3} sx={{ mr: 4}}>
                                    <Typography variant="button">DURATION</Typography>
                                </Grid>
                            </Grid>
                        </Box>
                        <ItemList items={items} type={type} onPlay={handlePlayClick} parentItemId={playlistData!.id}/>
                    </>
                )
            }
        </Box>
    );
};

export default PlaylistPage;
