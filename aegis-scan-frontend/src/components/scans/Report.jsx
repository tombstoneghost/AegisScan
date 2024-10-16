import React, { useEffect, useState } from "react";
import Layout from "../user/layout/Layout";
import { useParams } from "react-router-dom";
import { Alert, Button, Card, CardContent, CardHeader, Chip, Typography } from "@mui/material";
import axios from "axios";
import { API_BASE } from "../config";
import Cookies from 'js-cookie';
import Spider from "./Spider";
import Passive from "./Passive";
import Active from "./Active";

const Report = () => {
    const { scanId } = useParams();
    const [scanDetail, setScanDetail] = useState({
        scan_id: "",
        url: "",
        scan_type: "",
        status: "",
        result: "",
        start_time: "", 
        end_time: "",
        duration: "",
        user_id: "",
        spider_scan_id: "",
        active_scan_id: ""
    })

    const fetchData = () => {
        const token = Cookies.get('token')
        
        axios.get(`${API_BASE}/user/scan/results/${scanId}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }).then(resp => {
            console.log(resp.data.result);
            setScanDetail(resp.data.result);
        })
    };

    useEffect(() => {
        fetchData()
    }, [])

    const ReportLayout = () => {
        return (
            <div>
                <div>
                    {/* Header Card */}
                    <Card>
                        <CardHeader title={
                            <div className="row">
                                <div className="col">
                                    <Typography variant="h5">Scan Results</Typography>
                                </div>
                                <div className="col" style={{textAlign: 'right'}}>
                                    <Button href="/dashboard/all-scans" variant="outlined">Back</Button>
                                </div>
                            </div>
                        } subheader={scanDetail.url}/>
                        <CardContent>
                            <div className="mb-2">
                                <Typography variant="body1">Scan ID: <Chip variant="outlined" label={scanDetail.scan_id} /></Typography>
                            </div>
                            <div className="row">
                                <div className="col">
                                    <Typography variant="body1">
                                        Scan Type: <Chip color="success" label={String(scanDetail.scan_type).charAt(0).toLocaleUpperCase() + String(scanDetail.scan_type).slice(1)} />
                                    </Typography>
                                </div>
                                <div className="col">
                                    <Typography variant="body1">Scan Start Time: <Chip variant="outlined" label={scanDetail.start_time} /></Typography>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                    {/* Results */}
                    {scanDetail.scan_type === 'spider' && (
                        <Spider results={scanDetail.result}/>
                    )}
                    {scanDetail.scan_type === 'passive' && (
                        <Passive results={scanDetail.result}/>
                    )}
                    {scanDetail.scan_type === 'active' && (
                        <Active results={scanDetail.result}/>
                    )}
                </div>
            </div>
        )
    }

    return (
        <Layout>
            <ReportLayout />
        </Layout>
    )
};

export default Report;