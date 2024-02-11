import React, {FC} from 'react';
import {Route, Routes} from 'react-router-dom';
import MainPage from "./pages/MainPage";
import Layout from "./components/Layout";
import AlbumPage from "./pages/AlbumPage";
import PlaylistPage from "./pages/PlaylistPage";
import ArtistPage from "./pages/ArtistPage";
import AlbumsListPage from "./pages/AlbumsListPage";
import ArtistsListPage from "./pages/ArtistsListPage";
import TracksListPage from "./pages/TracksListPage";

const AppRoutes: FC = () => {
    // const navigate = useNavigate();
    return (
        <Routes>
            <Route
                path="/"
                element={
                    <Layout>
                        <MainPage/>
                    </Layout>
                }
            />
            <Route
                path={"/favorite-tracks"}
                element={
                    <Layout>
                        <TracksListPage/>
                    </Layout>
                }
            />
            <Route
                path={"/albums"}
                element={
                    <Layout>
                        <AlbumsListPage/>
                    </Layout>
                }
            />
            <Route
                path={"/album/:id"}
                element={
                    <Layout>
                        <AlbumPage/>
                    </Layout>
                }
            />
            <Route
                path={"/playlist/:id"}
                element={
                    <Layout>
                        <PlaylistPage/>
                    </Layout>
                }
            />
            <Route
                path={"/artist/:id"}
                element={
                    <Layout>
                        <ArtistPage/>
                    </Layout>
                }
            />
            <Route
                path={"/artists"}
                element={
                    <Layout>
                        <ArtistsListPage/>
                    </Layout>
                }
            />
        </Routes>
    );
};

export default AppRoutes;
