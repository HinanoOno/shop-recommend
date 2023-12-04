import { useCallback, useEffect, useMemo, useState } from "react";

import { Choice, Quiz } from "../api/@types";
import { useAsync } from "../services/useAsync";
import Loader from "../components/loader";
import { apiClient } from "../utils/client";

const Quizes = () => {
  const [quizes, setQuizes] = useState<Quiz[]>();

  const fetchQuizes = useCallback(async () => {
    try {
      const response = await apiClient.admin.quizes.$get();
      const dataArray = Object.values(response);
      const updatedArray: any[] = [];
      dataArray.forEach((quiz) => {
        if (Array.isArray(quiz)) {
          quiz.forEach((data) => {
            updatedArray.push(data);
          });
        }
      });
      setQuizes(updatedArray);
      console.log(quizes);
    } catch (error) {
      console.error("クイズの取得に失敗しました", error)
    }
    return quizes;
  }, []);


  /*useEffect(() => {
    fetchQuizes();
  }, [fetchQuizes]);*/
  const { data, loading, error } = useAsync(fetchQuizes);


  return (
    !loading ?(
    <div>
      <table>
        <thead>
          <tr>
            <th>クイズ内容</th>
            <th>画像</th>
            <th>補足</th>
            <th>選択肢</th>
          </tr>
        </thead>
        <tbody>
          {quizes &&
            Object.values(quizes).map((quiz, index) => (
              <tr key={index}>
                <td>{quiz.content}</td>
                <td>{quiz.image}</td>
                <td>{quiz.supplement}</td>
                <td>
                  <ul>
                    {quiz.choices &&
                      quiz.choices?.map((choice, choiceIndex) => (
                        <li key={choiceIndex}>
                          {`ID: ${choice.question_id}, Name: ${choice.name}, Valid: ${choice.valid}`}
                        </li>
                      ))}
                  </ul>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
    ):(
      <Loader/>
    )
  );
};

export default Quizes;
