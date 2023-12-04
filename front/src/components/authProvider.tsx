import React, { createContext, useContext, useEffect, useState } from "react";
import { LogInCheck } from "../hooks/loginCheck";

export type LoggedInType = {
  setUserAuth: (value: boolean) => void;
  setUserID: (value: number) => void;
  setUserName: (value: string) => void;
  userAuth: boolean;
  userid: number|null;
  username: string|null;
};

//コンテキストの作成
export const LoggedInContext = createContext<LoggedInType>({} as LoggedInType);

type Props = {
  children: React.ReactNode
}

//認証情報とセットするコンテキスト
export const LoggedInProvider = (props:Props) => {
  // globalなstateのデフォルトの値を作成
  const [username, setUserName] = useState<string|null>("");
  const [userid, setUserID] = useState<number|null>(0);
  const [userAuth, setUserAuth] = useState<boolean>(false);

  //初回だけ、ログインチェックを行う
  useEffect(() => {
    LogInCheck().then((res) => {
      if (res) {
        setUserName(res.data.name);
        setUserID(res.data.user_id);
        setUserAuth(true);
      } else {
        setUserName(null);
        setUserID(null);
        setUserAuth(false);
      }
    });
  }, []);

  return (
    <LoggedInContext.Provider
      value={{
        username,
        setUserName,
        userid,
        setUserID,
        userAuth,
        setUserAuth,
      }}
    >
      {props.children}
    </LoggedInContext.Provider>
  );
};

export const AuthProvider= () => {
  return useContext(LoggedInContext);
};
