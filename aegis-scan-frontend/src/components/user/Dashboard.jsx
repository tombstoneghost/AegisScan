import React, { useState, useEffect } from "react";
import Layout from "./layout/Layout";
import { Button, Card, CardContent, CardHeader, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from "@mui/material";
import axios from "axios";
import Cookies from 'js-cookie';
import { API_BASE } from "../config";
import { showError, showSuccess } from "../utils/misc";

const UserDashboard = () => {
    const [target, setTarget] = useState('')
    const [msg, setMsg] = useState('')
    const [err, setErr] = useState('')
    const [scans, setScans] = useState([])

    const handleChange = (e) => {
        e.preventDefault();

        setTarget(e.target.value);
    };

    const fetchData = () => {
        const token = Cookies.get('token')

        axios.get(`${API_BASE}/user/scans/running`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then(resp => {
            console.log(resp.data.result);
            setScans(resp.data.result);
        })
    };

    const updateStatus = () => {
        const token = Cookies.get('token')

        const scan_ids = scans.map((scan) => { return scan.scan_id })

        console.log(scan_ids)

        scan_ids.map((scan_id) => {
            axios.get(`${API_BASE}/user/scan/status/${scan_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }).then(resp => {
                setScans(prevData => prevData.map(item => item.scan_id === scan_id ? { ...item, status: resp.data.result} : item))
            })
        })
    }

    useEffect(() => {
        fetchData();
        updateStatus();

        const interval = setInterval(() => {
            fetchData();
            updateStatus();
        }, 30000);

        return () => clearInterval(interval)
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault()

        const data = {
            'target': target
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
    }

    const ScannerCard = () => {
        return (
            <div className="container-fluid">
                <Card>
                    <CardHeader title="Target to Scan"/>
                    <CardContent>
                        <form onSubmit={handleSubmit}>
                            <div>
                                <TextField placeholder="Enter Target" type="url" value={target} onChange={handleChange} fullWidth required/>
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
                                            <TableCell align="center">Status</TableCell>
                                            <TableCell align="center">Action</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {scans.map((scan) => (
                                            <TableRow>
                                                <TableCell align="center">{scan.scan_id}</TableCell>
                                                <TableCell align="center">{scan.url}</TableCell>
                                                <TableCell align="center">{scan.status}</TableCell>
                                                <TableCell align="center">
                                                    <Button variant="contained" href={`/scans/${scan.scan_id}`.toLowerCase()}>
                                                        View Report
                                                    </Button>
                                                </TableCell>
                                            </TableRow>
                                        ))}
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