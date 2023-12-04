import {
  Avatar,
  Box,
  Button,
  Checkbox,
  Container,
  FormControlLabel,
  Grid,
  Stack,
  TextField,
  Typography,
  createTheme,
} from "@mui/material";

import React, { FormEvent, useState } from "react";
import axios2 from "../../lib/axios2";
import { TestLogout } from "./logout";

import { useAuth } from "../../components/authContext";
import { Link, useNavigate } from "react-router-dom";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";

interface LoginData {
  email: string;
  password: string;
}

export default function LoginPage(): JSX.Element {
  const [loggedInUser, setLoggedInUser] = useState(null);
  const auth = useAuth();
  const navigation = useNavigate();

  const handleLogout = () => {
    axios2.get("http://localhost/sanctum/csrf-cookie").then(() => {
      auth
        ?.signout()
        .then(() => {
          navigation("/login");
        })
        .catch((error) => {
          console.log(error);
        });
    });
  };

  /*const handleLogin = React.useCallback(
    (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);
      console.log(formData);
      axios.get("http://localhost/sanctum/csrf-cookie").then((res) => {
        axios
          .post("http://localhost/api/login", {
            email: formData.get("email"),
            password: formData.get("password"),
          })
          .then((res) => {
            console.log(res);
            axios
              .get("http://localhost/api/user", {
                withCredentials: true,
              })
              .then((res) => {
                console.log(res.data.name);

                setLoggedInUser(res.data.name);
              })
              .catch((e) => {
                console.error(e);
              });
          })
          .catch((e) => {
            console.error(e);
          });
      });
    },
    []
  );*/

  const handleLogin = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    const data: LoginData = {
      email: email,
      password: password,
    };

    console.log(data);
    axios2.get("http://localhost/sanctum/csrf-cookie").then(() => {
      auth
        ?.signin(data)
        .then(() => {
          navigation("/python");
        })
        .catch((error) => {
          console.log(error);
        });
    });
  };

  //コピーライト部分
  function Copyright(props: any) {
    return (
      <Typography
        variant="body2"
        color="text.secondary"
        align="center"
        {...props}
      >
        {"Copyright © "}
        <Link to="https://mui.com/" color="inherit">
          Your Website
        </Link>{" "}
        {new Date().getFullYear()}
        {"."}
      </Typography>
    );
  }

  return (
    <>
      <Box>
        {auth?.user && (
          <TestLogout user={auth.user.name} onLogout={handleLogout} />
        )}
      </Box>
      {/*<Box
        p={2}
        display="flex"
        alignItems="center"
        justifyContent="center"
        height="100vh"
      >
        <Box component={"form"} p={3} onSubmit={handleLogin}>
          <Stack spacing={2}>
            <TextField
              label="email"
              name="email"
              type="email"
              size="small"
              required
            />
            <TextField
              label="password"
              name="password"
              type="password"
              size="small"
              required
            />
            <Button variant="outlined" fullWidth type="submit">
              Login!
            </Button>
          </Stack>
        </Box>
        </Box>*/}
        <Container component="main" maxWidth="xs">
          <Box
            sx={{
              marginTop: 8,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
            <Box
              component="form"
              onSubmit={handleLogin}
              sx={{ mt: 1 }}
            >
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
            </Box>
          </Box>
          <Copyright sx={{ mt: 8, mb: 4 }} />
        </Container>
    </>
  );
}
