import { Divider, Drawer, List, ListItem, ListItemButton, ListItemText, Toolbar, Typography, autocompleteClasses } from "@mui/material";
import React from "react";;

const SideMenu = () => {
    const drawerWidth = 240;

    const MenuItems = [
        {
            "name": "New Scan",
            "href": "/"
        },
        {
            "name": "All Scans",
            "href": "/dashboard/all-scans"
        }
    ]

    return (
        <Drawer sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
            }}
            PaperProps={{
                className: 'SideMenuBg',
                sx: {
                    color: 'whitesmoke'
                }
            }}
            variant="permanent"
            anchor="left">
                <Toolbar disableGutters>
                    <Typography variant="h6"
                        noWrap
                        component="a"
                        href={window.location.pathname}
                        sx={{
                        ml: 'auto',
                        mr: 'auto',
                        display: { xs: 'none', md: 'flex' },
                        fontFamily: 'monospace',
                        fontWeight: 700,
                        letterSpacing: '.3rem',
                        color: 'inherit',
                        textDecoration: 'none',
                        }}>
                        AegisScan
                    </Typography>
                </Toolbar>
                <Divider sx={{opacity: '1'}}/>
                <List>
                    {MenuItems.map((item, index) => (
                        <ListItem key={index} disablePadding>
                            <ListItemButton href={item.href}>
                                <ListItemText className="text-center">
                                    <Typography variant="h6" fontWeight={600}>
                                        {item.name}
                                    </Typography>
                                </ListItemText>
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
        </Drawer>
    )
};

export default SideMenu;