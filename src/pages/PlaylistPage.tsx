import React from 'react';
import Header from "../components/detailPage/Header";
import SkeletonHeader from "../components/detailPage/SkeletonHeader";

import ItemList from "../components/detailPage/ItemList";
import SkeletonItemList from "../components/detailPage/SkeletonItemList";
import {useParams} from "react-router-dom";
import {Item} from "../components/detailPage/types";
import {useGetPlaylistQuery} from "../services/playlists/playlistService";
import {WebSocketValues} from "../services/playerWebsocket/types";
import {useWebSocketContext} from "../providers/WebSocketProvider";

const PlaylistPage: React.FC = () => {
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

    const {data: playlistData, isLoading: playlistIsLoading} = useGetPlaylistQuery(playlistId);
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
        actionPlayPlaylist(playlistId, startFrom);
    };
    return (
        <div style={{padding: 16}}>
            {playlistIsLoading ? <SkeletonHeader/> :
                <Header title={playlistData!.title} description={playlistData!.creator.name} imageUrl={playlistData!.picture_medium}/>}
            {playlistIsLoading ? <SkeletonItemList/> :
                <ItemList items={items} type={type} onPlay={handlePlayClick} parentItemId={playlistData!.id} />}
        </div>
    );
};

export default PlaylistPage;
