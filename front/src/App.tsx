import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import { Quiz } from "./api/@types";

function App() {
  const quizData: Quiz = {
    content: "hoge",
    choices: [
      {
        question_id: 8,
        name: "option 1",
        valid: true,
      },
      {
        question_id: 8,
        name: "option 2",
        valid: false,
      },
      {
        question_id: 8,
        name: "option 3",
        valid: false,
      },
    ],
  };
  const [quiz, setQuiz] = useState<Quiz>(quizData);
  /*useEffect(() => {
    const postQuiz = async () => {
      try {
        const response = await apiClient.admin.quizes.$post({ body: quizData });
        console.log(response);
        setQuiz(quizData);
      } catch (error) {
        console.error('クイズの投稿に失敗しました', error);
      }
    };
    postQuiz();
  }, []);*/

  /*apiClient.admin.quizes.$get().then((response) => {
    console.log(response);
  }).catch((error) => {
    console.error('Error retrieving quiz:', error);
  });*/

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <div>
          {quiz && (
            <div>
              <p>Content: {quiz.content}</p>
              <p>Image: {quiz.image}</p>
              <p>Supplement: {quiz.supplement}</p>
            </div>
          )}
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
