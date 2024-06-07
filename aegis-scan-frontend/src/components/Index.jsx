import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./core/Login";
import UserDashboard from "./user/Dashboard";
import AdminDashboard from "./admin/Dashboard";

const Index = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/">
                    <Route index element={<LoginPage />} />
                </Route>
                <Route path="/dashboard">
                    <Route index element={<UserDashboard />} />
                </Route>
                <Route path="/admin">
                    <Route index element={<AdminDashboard />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
};

export default Index;