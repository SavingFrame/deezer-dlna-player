import React from 'react';
import {Box, Typography} from "@mui/material";
import Search from "../components/Search";
import {useGetAlbumsQuery} from "../services/albums/albumService";
import SkeletonAlbumCard from "../components/detailPage/SkeletonAlbumCard";
import AlbumCard from "../components/detailPage/AlbumCard";
import useDocumentTitle from "../services/headerTitle/useHeaderTitle";


const AlbumsListPage = () => {
    useDocumentTitle('Favourite albums');
    const {data, isLoading} = useGetAlbumsQuery(999);
    return (
        <Box sx={{padding: 2}}>
            <Search/>
            {isLoading ? (
                <>
                    <Typography variant="h5" component="h2">Albums</Typography>
                    <SkeletonAlbumCard/>
                </>
            ) : data && (
                <>
                    <Typography variant="h5" component="h2">Albums</Typography>
                    <AlbumCard albums={data}/>
                </>
            )}
        </Box>
    )
}

export default AlbumsListPage;
