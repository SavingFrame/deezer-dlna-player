import React, {useState} from 'react';
import Header from "../components/detailPage/Header";
import SkeletonHeader from "../components/detailPage/SkeletonHeader";

import ItemList from "../components/detailPage/ItemList";
import SkeletonItemList from "../components/detailPage/SkeletonItemList";
import {useParams} from "react-router-dom";
import {Item} from "../components/detailPage/types";
import {WebSocketValues} from "../services/playerWebsocket/types";
import {useWebSocketContext} from "../providers/WebSocketProvider";
import {
    useGetArtistQuery,
    useGetArtistTopTracksQuery,
    useGetArtistAlbumsQuery
} from "../services/artists/artistService";
import {Box, Button, Typography} from "@mui/material";
import AlbumCard from "../components/detailPage/AlbumCard";
import SkeletonAlbumCard from "../components/detailPage/SkeletonAlbumCard";
import useDocumentTitle from "../services/headerTitle/useHeaderTitle";

const ArtistPage: React.FC = () => {
    useDocumentTitle('Artist');
    const {actionPlayArtistTopTracks}: WebSocketValues = useWebSocketContext();
    const {id} = useParams<{ id: string }>();
    if (!id) {
        throw new Error("ID is not defined in the URL");
    }
    const artistId = parseInt(id);

    const [displayCount, setDisplayCount] = useState(5); // Initial number of items to display

    const loadMoreItems = () => {
        const itemsPerPage = displayCount === 5 ? 15 : 20
        setDisplayCount(prevCount => prevCount + itemsPerPage);
    };


    const formatDuration = (duration: number) => {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };

    const {data: artistData, isLoading: artistIsLoading} = useGetArtistQuery(artistId);
    const {data: artistTopTracksData, isLoading: artistTopTracksIsLoading} = useGetArtistTopTracksQuery(artistId);
    const {data: artistAlbumsData, isLoading: artistAlbumsIsLoading} = useGetArtistAlbumsQuery(artistId);
    const type = 'artist';
    const items: Item[] = artistTopTracksData?.map(track => ({
        id: track.id,
        title: track.title,
        description: track.artist.name,
        column1: track.album.title,
        column2: track.rank.toString(),
        column3: formatDuration(track.duration),
        coverUrl: track.album.cover_medium,
    })) || [];

    const displayedItems = items.slice(0, displayCount);


    const handlePlayClick = (artistId: number, startFrom: number) => {
        actionPlayArtistTopTracks(artistId, startFrom);
    };

    return (
        <div style={{padding: 16}}>
            {
                artistIsLoading ? <SkeletonHeader/> :
                    <Header
                        title={artistData!.name}
                        description={artistData!.nb_fan + ' fans'}
                        imageUrl={artistData!.picture_big}
                    />
            }
            {artistTopTracksIsLoading ? <SkeletonItemList count={5}/> :
                <>
                    <Typography variant="h5">Top tracks</Typography>
                    <ItemList items={displayedItems} type={type} onPlay={handlePlayClick}
                              parentItemId={artistId}/>
                    {displayCount < items.length && (
                        <Box display="flex" justifyContent="center" marginTop={2}>
                            <Button variant="contained" color="primary" onClick={loadMoreItems}>
                                Show More
                            </Button>
                        </Box>
                    )}

                </>
            }
            {artistAlbumsIsLoading ? (
                <>
                    <Typography variant="h5" component="h2">Albums</Typography>
                    <SkeletonAlbumCard/>
                </>
            ) : artistAlbumsData && (
                <>
                    <Typography variant="h5" component="h2">Albums</Typography>
                    <AlbumCard albums={artistAlbumsData}/>
                </>
            )}


        </div>
    );
};

export default ArtistPage;
