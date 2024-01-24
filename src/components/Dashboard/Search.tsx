import React from 'react';
import {
    Avatar,
    Button,
    CircularProgress,
    List,
    ListItem,
    ListItemAvatar, ListItemButton,
    ListItemText,
    Typography
} from '@mui/material';
import {
    useGetSearchAlbumsQuery,
    useGetSearchArtistsQuery,
    useGetSearchTracksQuery
} from "../../services/search/searchService";
import {useNavigate} from "react-router-dom";

// Assuming fetchData is a prop function that knows which endpoint to hit based on category
type SearchProps = {
    searchQuery: string;
};

const Search: React.FC<SearchProps> = ({ searchQuery }) => {
    const navigate = useNavigate();
    const { data: artistsData, isLoading: artistsIsLoading } = useGetSearchArtistsQuery({query: searchQuery});
    const { data: tracksData, isLoading: tracksIsLoading } = useGetSearchTracksQuery({query: searchQuery});
    const { data: albumsData, isLoading: albumsIsLoading } = useGetSearchAlbumsQuery({query: searchQuery});


    return (
        <div>
            <Typography variant="h6">Artists</Typography>
            {artistsIsLoading ? <CircularProgress/> : null}
            <List>
                {artistsData?.map((artist) => (
                    <ListItemButton key={artist.id} onClick={() => navigate(`artist/${artist.id}`)}>
                        <ListItemAvatar>
                            <Avatar src={artist.picture_medium} />
                        </ListItemAvatar>
                        <ListItemText primary={artist.name} secondary={`Fans: ${artist.nb_fan}`} />
                    </ListItemButton>
                ))}
            </List>
            <Button onClick={() => {}}>Show More Artists</Button>

            <Typography variant="h6">Albums</Typography>
            {albumsIsLoading ? <CircularProgress/> : null}
            <List>
                {albumsData?.map((album) => (
                    <ListItemButton key={album.id} onClick={() => navigate(`album/${album.id}`)}>
                        <ListItemAvatar>
                            <Avatar src={album.cover_medium} />
                        </ListItemAvatar>
                        <ListItemText primary={album.title} secondary={`Tracks: ${album.nb_tracks}`} />
                    </ListItemButton>
                ))}
            </List>
            <Button onClick={() => {}}>Show More Albums</Button>

            <Typography variant="h6">Tracks</Typography>
            {tracksIsLoading ? <CircularProgress/> : null}
            <List>
                {tracksData?.map((track) => (
                    <ListItemButton key={track.id} onClick={() => navigate(`album/${track.album.id}`)}>
                        <ListItemAvatar>
                            <Avatar src={track.album.cover_medium} />
                        </ListItemAvatar>
                        <ListItemText primary={track.title} secondary={`Artist: ${track.artist.name}`} />
                    </ListItemButton>
                ))}
            </List>
            <Button onClick={() => {}}>Show More Tracks</Button>
        </div>
    );
};

export default Search;
