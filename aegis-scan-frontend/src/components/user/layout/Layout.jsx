import { AppBar, Box, Button, Toolbar, Typography } from "@mui/material";
import axios from "axios";
import React from "react";
import { API_BASE } from "../../config";
import Cookies from 'js-cookie'
import { useNavigate } from "react-router-dom";
import SideMenu from "./SideMenu";

const Layout = ({children}) => {
    const drawerWidth = 240;

    const navigate = useNavigate()

    const handleLogout = (e) => {
        e.preventDefault()

        const token = Cookies.get('token')

        axios.get(`${API_BASE}/auth/logout`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then(resp => {
            if(String(resp.data.msg).includes("Successful")) {
                Cookies.remove('token');
                navigate('/')   
            }
        })
    }

    return (
        <>
            <Box sx={{ display: 'flex'}}>
                <AppBar position="fixed"
                    sx={{
                    width: { sm: `calc(100% - ${drawerWidth}px)` },
                    ml: { sm: `${drawerWidth}px` },
                    }} className="HeaderClass">
                    <div className="container-fluid">
                        <Toolbar>
                            <div className="ml-auto">
                                <Button 
                                    variant="outlined" 
                                    style={{color: 'white', borderColor: 'white'}}
                                    onClick={handleLogout}>
                                    Logout
                                </Button>
                            </div>
                        </Toolbar>
                    </div>
                </AppBar>
                <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
                    <SideMenu />
                </Box>
                <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
                    <Toolbar />
                    {children}
                </Box>
            </Box>
        </>
    )
};

export default Layout;