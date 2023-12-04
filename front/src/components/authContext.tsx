import React, {
  useContext,
  createContext,
  useState,
  ReactNode,
  useEffect,
  FC,
  memo,
} from "react";
import { Route, Navigate, RouteProps, useNavigate } from "react-router-dom";
import axios2 from "../lib/axios2";
import Python from "../pages/python";

interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

interface LoginData {
  email: string;
  password: string;
}
interface RegisterData {
  name: string;
  email: string;
  password: string;
  password_confirmation: string;
}
interface authProps {
  user: User | null;
  register: (registerData: RegisterData) => Promise<void>;
  signin: (loginData: LoginData) => Promise<void>;
  signout: () => Promise<void>;
}
interface Props {
  children: ReactNode;
}
interface From {
  from: Location;
}
type PrivateRouteProp = {
  children: ReactNode;
} 
type PublicRouteProp = {
  children: ReactNode;
} 



const authContext = createContext<authProps | null>(null);

//認証関連一覧
const useProvideAuth = () => {
  const [user, setUser] = useState<User | null>(null);

  
  const register = async (registerData: RegisterData) => {
    const res = await axios2.post('/register', registerData);
    axios2.get('/user').then((res_1) => {
      setUser(res_1.data);
    });
  }

  const signin = async (loginData: LoginData) => {
    try {
      const res = await axios2.post('/api/login', loginData);
    } catch (error) {
      throw error;
    }

    return axios2.get('/api/user').then((res) => {
      console.log(res.data);
      setUser(res.data)
    }).catch((error) => {
      setUser(null)
    })
  }
  const signout = async () => {
    await axios2.post('/api/logout', {});
    setUser(null);
  }

  
  useEffect(() => {
    axios2.get("/sanctum/csrf-cookie").then(() => {
      axios2
        .get("/api/user")
        .then((res) => {
          setUser(res.data);
        })
        .catch((error) => {
          setUser(null);
        });
    });
  }, []);

  return {
    user,
    register,
    signin,
    signout,
  };
};

const ProvideAuth = ({ children }: Props) => {
  const auth = useProvideAuth();
  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
};
export default ProvideAuth;

export const useAuth = () => {
  return useContext(authContext);
};

export const PrivateRoute = ({ children }: PrivateRouteProp) => {
  const auth = useAuth();
  console.log(auth?.user)

  return auth?.user ? (
    <>{children}</> 
  ) : (
    <Navigate to="/login" />
  );
};
export const PublicRoute = ({ children }: PublicRouteProp) => {
  const auth = useAuth();

  return !auth?.user ? (
    <>{children}</> 
  ) : (
    <Navigate to="/python" />
  );
};