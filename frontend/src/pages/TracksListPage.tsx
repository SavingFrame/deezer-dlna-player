import React, {useState} from 'react';
import {Box, Grid, IconButton, Typography} from "@mui/material";
import {useGetFavouriteTracksQuery} from "../services/tracks/tracksService";
import SkeletonItemList from "../components/detailPage/SkeletonItemList";
import ItemList from "../components/detailPage/ItemList";
import Search from "../components/Search";
import {Item} from "../components/detailPage/types";
import useDocumentTitle from "../services/headerTitle/useHeaderTitle";
import {WebSocketValues} from "../services/playerWebsocket/types";
import {useWebSocketContext} from "../providers/WebSocketProvider";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';


const TracksListPage = () => {
    useDocumentTitle('Favorite tracks');
    const {actionPlayFavoriteTracks}: WebSocketValues = useWebSocketContext();
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const {data, isLoading} = useGetFavouriteTracksQuery({limit: 999, ordering: sortOrder});

    const toggleSortOrder = () => {
        setSortOrder(prevOrder => prevOrder === 'asc' ? 'desc' : 'asc');
    };

    const formatDuration = (duration: number) => {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };

    const handlePlayClick = (_: number, id: number) => {
        actionPlayFavoriteTracks(id, sortOrder);
    }
    const items: Item[] = data?.map(track => ({
        id: track.id,
        title: track.title,
        description: track.artist.name,
        coverUrl: track.album.cover_medium,
        column1: formatDuration(track.duration),
        column2: new Date(track.time_add).toLocaleString(),
    })) || [];
    return (
        <Box sx={{padding: 2}}>
            <Search/>
            <Typography variant="h5" component="h2">Favourite tracks</Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', ml: 2 }}>
                <Grid container spacing={2} sx={{flex: 1, mr: 2, alignItems: 'center' }}>
                    <Grid item xs={1}>
                        <Typography variant="button">#</Typography>
                    </Grid>
                    <Grid item xs={3}>
                        <Typography variant="button">TRACK</Typography>
                    </Grid>
                    <Grid item xs>
                        <Typography variant="button">DURATION</Typography>
                    </Grid>
                    <Grid item xs>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography variant="button">ADDED</Typography>
                            <IconButton onClick={toggleSortOrder} size="small">
                                {sortOrder === 'asc' ? <ArrowUpwardIcon /> : <ArrowDownwardIcon />}
                            </IconButton>
                        </Box>
                    </Grid>
                </Grid>
            </Box>

            {isLoading ? <SkeletonItemList count={40}/> :
                <ItemList items={items} type={"playlist"} parentItemId={0}
                          onPlay={handlePlayClick}/>}
        </Box>
    )
}

export default TracksListPage;
