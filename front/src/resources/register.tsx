import { Box, Button, Stack, TextField } from "@mui/material";
import React from "react";
import axios from "../lib/axios";


export default function TestCreateUser(): JSX.Element {
    const handleCreate = React.useCallback((e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const formData = new FormData(e.currentTarget)
        axios.post("http://localhost/register", {
            "name": formData.get("name"),
            "email": formData.get("email"),
            "password": formData.get("password"),
            "password_confirmation": formData.get("password_confirmation")
        }, {
            withCredentials: true
        }).then(res => {
            console.log(res.data)
        }).catch(e => {
            console.error(e)
        })
    }, [])
    return (
        <Box
            p={2}
        >
            <Box
                component={"form"}
                p={3}
                onSubmit={handleCreate}
            >
                <Stack
                    spacing={2}
                >
                    <TextField
                        label="name"
                        name="name"
                        size='small'
                        required
                    />
                    <TextField
                        label="email"
                        name="email"
                        type="email"
                        size='small'
                        required
                    />
                    <TextField
                        label="password"
                        name="password"
                        type='password'
                        size='small'
                        required
                    />
                    <TextField
                        label="pasword(confirm)"
                        name="password_confirmation"
                        type='password'
                        size='small'
                        required
                    />
                    <Button
                        variant='outlined'
                        fullWidth
                        type='submit'
                    >Create!</Button>
                </Stack>
            </Box>
        </Box>
    )
}