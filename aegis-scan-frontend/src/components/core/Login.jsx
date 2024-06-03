import React, { useState } from "react";
import { Avatar, Card, CardContent, Stack, Typography, TextField, Button, Alert } from '@mui/material'
import { LockOutlined } from '@mui/icons-material'
import axios from 'axios';
import {API_BASE} from '../config';
import { useNavigate } from "react-router-dom";
import { showError, showLoading, showSuccess } from "../utils/misc";
import Cookies from 'js-cookie'

const LoginPage = () => {
    const [data, setData] = useState({
        username: '',
        password: '',
        msg: '',
        success: false, 
        error: false,
        loading: false
    });

    const {username, password, msg, success, error, loading} = data;

    const navigate = useNavigate()

    const submitLogin = (e) => {
        e.preventDefault()

        setData({...data, loading: true})

        const formData = {
            'username': username, 
            'password': password
        }

        axios.post(`${API_BASE}/auth/login`, formData)
        .then(resp => {
            if(resp.data.access_token) {
                setData({...data, msg: resp.data.msg, success: true, error: false, loading: false})
                Cookies.set('token', resp.data.access_token)
                navigate('/dashboard')

            } else {
                setData({...data, msg: resp.data.msg, success: false, error: true, loading: false})
            }
        })
    };

    const handleChange = name => e => {
        setData({...data, [name]: e.target.value})
    }

    const LoginForm = () => {
        return (
            <Card style={{width: '50vh'}}>
                <CardContent>
                    <Avatar className="ml-auto mr-auto" style={{backgroundColor: '#3b8deb'}}>
                        <LockOutlined />
                    </Avatar>
                    <div className="mt-3 text-center">
                        <div className="m-2">
                            <Typography>Welcome to Aegis Scan</Typography>
                        </div>
                        <form onSubmit={submitLogin}>
                            <div>
                                <TextField placeholder="Username" name="username" value={username} onChange={handleChange('username')} fullWidth required/>
                            </div>
                            <div className="mt-3">
                                <TextField placeholder="Password" name="password" type="password" value={password} onChange={handleChange('password')} fullWidth required/>
                            </div>
                            <div className="mt-3">
                                <Button type="submit" variant="contained" color="primary">Login</Button>
                            </div>
                        </form>
                        {showError(error, msg)}
                        {showSuccess(success, msg)}
                        {showLoading(loading)}
                    </div>
                </CardContent>
            </Card>
        )
    }

    return (
        <div className="LoginPage">
            <Stack direction="row" justifyContent="center" alignItems="center" style={{height: '100vh'}}>
                {LoginForm()}
            </Stack>
        </div>
    )
};

export default LoginPage;
