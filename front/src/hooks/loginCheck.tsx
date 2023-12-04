import { AxiosResponse } from "axios";
import axios from "../lib/axios";

export const LogInCheck = async (): Promise<AxiosResponse<any, any> | null> => {
  try {
    // csrf-cookie 取得
    await axios.get("http://localhost/sanctum/csrf-cookie", { withCredentials: true });

    // user 取得
    const response = await axios.get("http://localhost/user", {
      withCredentials: true,
    });

    return response;
  } catch (error) {
    console.error("Login check error:", error);
    return null;
  }
};
