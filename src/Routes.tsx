import React, {FC} from 'react';
import {Route, Routes} from 'react-router-dom';
import MainPage from "./pages/MainPage";
import Layout from "./components/Layout";

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
        </Routes>
    );
};

export default AppRoutes;
