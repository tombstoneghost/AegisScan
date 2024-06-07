import React, { useState } from "react";
import Layout from "./layout/Layout";
import { Button, Card, CardContent, CardHeader, TextField } from "@mui/material";
import axios from "axios";
import Cookeis from 'js-cookie';
import { API_BASE } from "../config";
import { showError, showSuccess } from "../utils/misc";
import OnGoingScan from "./components/OnGoingScan";

const UserDashboard = () => {
    const [target, setTarget] = useState('')
    const [msg, setMsg] = useState('')
    const [err, setErr] = useState('')

    const handleChange = (e) => {
        e.preventDefault();

        setTarget(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault()

        const data = {
            'target': target
        };

        const token = Cookeis.get('token')

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
                            <Button className="mt-3" variant="contained">
                                Scan
                            </Button>
                        </form>
                        {showError(err, err)}
                        {showSuccess(msg, msg)}
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <Layout>
            {ScannerCard()}
            {OnGoingScan()}
        </Layout>
    )
};

export default UserDashboard;