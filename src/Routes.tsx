import React, {FC} from 'react';
import {Route, Routes} from 'react-router-dom';
import MainPage from "./pages/MainPage";
import Layout from "./components/Layout";
import AlbumPage from "./pages/AlbumPage";
import PlaylistPage from "./pages/PlaylistPage";

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
        </Routes>
    );
};

export default AppRoutes;
