import React, {useEffect, useState} from "react";
import Layout from "../user/layout/Layout";
import { Card, CardHeader, CardContent, TableContainer, Table, TableHead, TableRow, TableCell, IconButton, Paper, TableBody } from "@mui/material";
import { Visibility, RestartAlt, Delete } from '@mui/icons-material'
import Cookies from 'js-cookie';
import { API_BASE } from "../config";
import axios from "axios";
import { showSuccess } from "../utils/misc";


const AllScans = () => {
    const [scans, setScans] = useState([])
    const [msg, setMsg] = useState('')
    const [err, setErr] = useState('')

    const fetchData = () => {
        const token = Cookies.get('token')

        axios.get(`${API_BASE}/user/scans/all`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }).then(resp => {
            setScans(resp.data.result)
        })
    };

    useEffect(() => {
        fetchData();
    }, [])

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
    };

    const handleDelete = (id) => (e) => {
        const token = Cookies.get('token')

        setMsg('');
        setErr('');

        axios.get(`${API_BASE}/user/scan/delete/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }).then(resp => {
            setMsg(resp.data.result)
        }).finally(() => {
            fetchData();
        })
    }

    const AllScansCard = () => {
        return (
            <div className="mt-4 container-fluid">
                <Card>
                    <CardContent>
                        {showSuccess(msg, msg)}
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
                                        {scans.map((scan, idx) => (
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
                                                    <IconButton variant="contained" onClick={handleDelete(scan.scan_id)} color="error">
                                                        <Delete />
                                                    </IconButton>
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
    }

    return (
        <Layout>
            <AllScansCard />
        </Layout>
    )
};

export default AllScans;