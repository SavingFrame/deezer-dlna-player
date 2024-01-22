import React from 'react';
import Header from "../components/detailPage/Header";
import SkeletonHeader from "../components/detailPage/SkeletonHeader";

import ItemList from "../components/detailPage/ItemList";
import SkeletonItemList from "../components/detailPage/SkeletonItemList";
import {useGetAlbumQuery} from "../services/albums/albumService";
import {useParams} from "react-router-dom";
import {Item} from "../components/detailPage/types";
import {WebSocketValues} from "../services/playerWebsocket/types";
import {useWebSocketContext} from "../providers/WebSocketProvider";

const AlbumPage: React.FC = () => {
    const {actionPlayAlbum}: WebSocketValues = useWebSocketContext();
    const {id} = useParams<{ id: string }>();
    if (!id) {
        throw new Error("ID is not defined in the URL");
    }
    const albumId = parseInt(id);

    const formatDuration = (duration: number) => {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };

    const {data: albumData, isLoading: albumIsLoading} = useGetAlbumQuery(albumId);
    const type = 'album';
    const items: Item[] = albumData?.tracks.map(track => ({
        id: track.id,
        title: track.title,
        description: albumData.artist.name,
        column1: formatDuration(track.duration),
    })) || [];

    const handlePlayClick = (albumId: number, startFrom: number) => {
        actionPlayAlbum(albumId, startFrom);
    };

    return (
        <div style={{padding: 16}}>
            {albumIsLoading ? <SkeletonHeader/> :
                <Header title={albumData!.title} description={albumData!.artist.name} imageUrl={albumData!.cover_big}/>}
            {albumIsLoading ? <SkeletonItemList/> :
                <ItemList items={items} type={type} albumCoverUrl={albumData!.cover_medium} parentItemId={albumData!.id}
                          onPlay={handlePlayClick}/>}
        </div>
    );
};

export default AlbumPage;
