import React, { useState, useEffect } from "react";
import Layout from "./layout/Layout";
import { Button, Card, CardContent, CardHeader, FormControl, IconButton, InputLabel, MenuItem, Paper, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField } from "@mui/material";
import axios from "axios";
import Cookies from 'js-cookie';
import { API_BASE } from "../config";
import { showError, showSuccess } from "../utils/misc";
import { Visibility, RestartAlt } from '@mui/icons-material'

const UserDashboard = () => {
    const [target, setTarget] = useState('')
    const [scanType, setScanType] = useState('')
    const [appType, setAppType] = useState('')
    const [msg, setMsg] = useState('')
    const [err, setErr] = useState('')
    const [scans, setScans] = useState([])

    const handleChange = (name) => (e) => {
        e.preventDefault();

        if(name === 'target'){
            setTarget(e.target.value);
        } else if(name === 'scanType') {
            setScanType(e.target.value);
        } else if(name === 'appType') {
            setAppType(e.target.value)
        }
        
    };

    const fetchData = async () => {
        const token = Cookies.get('token')

        try {
            const resp = await axios.get(`${API_BASE}/user/scans/running`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
    
            const runningScans = resp.data.result;

            setScans(runningScans);
    
            const updatedScans = await Promise.all(
                runningScans.map(scan => 
                    axios.get(`${API_BASE}/user/scan/status/${scan.scan_id}`, {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }).then(statusResp => ({
                        ...scan, 
                        status: statusResp.data.result,
                        progress: statusResp.data.progress
                    }))
                )
            );
    
            setScans(updatedScans);
        } catch(error) {
            console.error("Error fetching data:", error)
        }
    }

    useEffect(() => {
        fetchData();

        const interval = setInterval(() => {
            fetchData();
        }, 10000);

        return () => clearInterval(interval)
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault()

        const data = {
            'target': target,
            'scan_type': scanType,
            'app_type': appType
        };

        const token = Cookies.get('token')

        setMsg('');
        setErr('')

        axios.post(`${API_BASE}/user/scan-target`, data, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }).then(resp => {
            if(resp.data.msg) {
                setMsg(resp.data.msg);
                setErr('');
            } else if(resp.data.err) {
                setErr(resp.data.err);
                setMsg('');
            }
        }).finally(() => {
            fetchData()
        })
    };

    const handleRestart = (id) => (e) => {
        e.preventDefault()

        const target = scans.filter((scan) => {
            if(scan.scan_id === id) {
                return scan
            }
        })

        const data = {
            'target': target[0].url,
            'scan_type': target[0].scan_type
        };

        const token = Cookies.get('token')

        setMsg('');
        setErr('');

        axios.post(`${API_BASE}/user/scan-target`, data, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }).then(resp => {
            if(resp.data.msg) {
                setMsg(resp.data.msg);
                setErr('');
            } else if(resp.data.err) {
                setErr(resp.data.err);
                setMsg('');
            }
        }).finally(() => {
            fetchData()
        })
    }

    const ScannerCard = () => {
        return (
            <div className="container-fluid">
                <Card>
                    <CardHeader title="Target to Scan"/>
                    <CardContent>
                        <form onSubmit={handleSubmit}>
                            <div>
                                <TextField placeholder="Enter Target" type="url" value={target} onChange={handleChange('target')} fullWidth required/>
                            </div>
                            <div className="mt-2">
                                <FormControl fullWidth>
                                    <InputLabel id="app-type-label">Application Type</InputLabel>
                                    <Select
                                        labelId="app-type-label"
                                        id="app-type-select"
                                        label="Application Type"
                                        onChange={handleChange('appType')}>
                                        <MenuItem value={"ecom"}>E-Com</MenuItem>
                                        <MenuItem value={"blog"}>Blog</MenuItem>
                                        <MenuItem value={"social_media"}>Social Media</MenuItem>
                                        <MenuItem value={"cms"}>CMS</MenuItem>
                                        <MenuItem value={"forums"}>Forums</MenuItem>
                                        <MenuItem value={"educational"}>Educational</MenuItem>
                                        <MenuItem value={"news_media"}>News Media</MenuItem>
                                        <MenuItem value={"android"}>Android</MenuItem>
                                    </Select>
                                </FormControl>
                            </div>
                            <div className="mt-2">
                                <FormControl fullWidth>
                                    <InputLabel id="scan-type-label">Scan Type</InputLabel>
                                    <Select
                                        labelId="scan-type-label"
                                        id="scan-type-select"
                                        label="Scan Type"
                                        onChange={handleChange('scanType')}>
                                        <MenuItem value={"spider"}>Spider</MenuItem>
                                        <MenuItem value={"passive"}>Passive</MenuItem>
                                        <MenuItem value={"active"}>Active</MenuItem>
                                        <MenuItem value={"complete"}>Complete</MenuItem>
                                    </Select>
                                </FormControl>
                            </div>
                            <Button type="submit" className="mt-3" variant="contained">
                                Scan
                            </Button>
                        </form>
                        {showError(err, err)}
                        {showSuccess(msg, msg)}
                    </CardContent>
                </Card>
            </div>
        )
    };

    const OnGoingScan = () => {
        return (
            <div className="mt-4 container-fluid">
                <Card>
                    <CardHeader title="On Going Scans" />
                    <CardContent>
                        <div>
                            <TableContainer component={Paper}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell align="center">Scan ID</TableCell>
                                            <TableCell align="center">URL</TableCell>
                                            <TableCell align="center">Scan Type</TableCell>
                                            <TableCell align="center">Status</TableCell>
                                            <TableCell align="center">Action</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {scans.map((scan, idx) => {
                                            if(!String(scan.status).includes("Completed")) {
                                                return (
                                                    <TableRow key={idx}>
                                                        <TableCell align="center">{scan.scan_id}</TableCell>
                                                        <TableCell align="center">{scan.url}</TableCell>
                                                        <TableCell align="center">{String(scan.scan_type).toUpperCase()}</TableCell>
                                                        <TableCell align="center">{scan.status}</TableCell>
                                                        <TableCell align="center">
                                                            <IconButton variant="contained" color="success" href={`/scans/${scan.scan_id}`.toLowerCase()} disabled={!String(scan.status).includes('Completed')}>
                                                                <Visibility />
                                                            </IconButton>
                                                            <IconButton variant="contained" onClick={handleRestart(scan.scan_id)} color="primary" disabled={scan.status !== 'Failed'}>
                                                                <RestartAlt />
                                                            </IconButton>
                                                        </TableCell>
                                                    </TableRow>
                                                )
                                            }
                                        })}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </div>
                    </CardContent>
                </Card>
            </div>
        )
    };

    return (
        <Layout>
            {ScannerCard()}
            {OnGoingScan()}
        </Layout>
    )
};

export default UserDashboard;