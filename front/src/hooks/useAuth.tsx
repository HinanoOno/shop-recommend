import { useNavigate, useParams } from "react-router-dom";
import axios from "../lib/axios";

import express from "express";

const app = express();

export const useAuth = () => {
  let navigate = useNavigate();

  const csrf = () => axios.get("http://localhost/sanctum/csrf-cookie");

  const login = async ({
    email,
    password,
  }: {
    email: string;
    password: string;
  }) => {
    
    await csrf();
    axios
      .post("http://localhost/api/login", { email, password })
      .then((res) => console.log(res));
  };

  return {
    login,
  };
};
