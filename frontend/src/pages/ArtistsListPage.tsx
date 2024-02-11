import React from "react";
import Search from "../components/Search";
import {Box, Grid, Typography} from "@mui/material";
import SkeletonAlbumCard from "../components/detailPage/SkeletonAlbumCard";
import {useGetArtistsQuery} from "../services/artists/artistService";
import ItemCard from "../components/Dashboard/ItemCard";
import useDocumentTitle from "../services/headerTitle/useHeaderTitle";


const ArtistsListPage = () => {
    useDocumentTitle('Favorite artists');
    const {data, isLoading} = useGetArtistsQuery(999);
    return (<>
        <Box sx={{padding: 2}}>
            <Search/>
            <Typography variant="h5" component="h2">Artists</Typography>
            {isLoading ? (
                <>
                    <SkeletonAlbumCard/>
                </>
            ) : data && (
                <Grid container spacing={2}>
                    {data?.map((artist, index) => (
                        <ItemCard
                            title={artist.name}
                            description={artist.nb_fan + ' fans'}
                            description2={artist.nb_album + ' albums'}
                            imageUrl={artist.picture_medium}
                            id={artist.id}
                            type={"artist"}
                        />
                    ))}
                </Grid>
            )}
        </Box>
    </>)
}

export default ArtistsListPage;
