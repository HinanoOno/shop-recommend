import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import NewQuiz from "./pages/newquiz";
import Quizes from "./pages/quizes";
import QuizFormComponent from "./pages/quizFormComponent";
import Python from "./pages/python";
import LoginPage from "./pages/auth/login";
import TestCreateUser from "./resources/register";
import ProvideAuth, {
  PrivateRoute,
  PublicRoute,
} from "./components/authContext";
import MyPage from "./pages/mypage";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
//ページ全体のテーマ
const defaultTheme = createTheme({
  palette: {
    mode: 'light',
  }
})

root.render(
  <>
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
        <ProvideAuth>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<App />} />
              <Route path="/quiz" element={<NewQuiz />} />
              <Route path="/quizes" element={<Quizes />} />
              <Route path="/quizform" element={<QuizFormComponent />} />
              <Route path="/python" element={<PrivateRoute children={<Python />} />} />
              <Route
                path="/my-page"
                element={<MyPage />}
              />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<TestCreateUser />} />
            </Routes>
          </BrowserRouter>
        </ProvideAuth>
    </ThemeProvider>
  </>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
