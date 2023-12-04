import { FC } from "react";
import { Quiz } from "./../api/@types";


import { useForm, SubmitHandler } from "react-hook-form";
import Loader from "../components/loader";
import { apiClient } from "../utils/client";

const NewQuiz: FC = () => {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Quiz>();

  const onSubmit: SubmitHandler<Quiz> = async (data) => {
    try {
      const response = await apiClient.admin.quizes.$post({ body: data });
      console.log(response);
    } catch (error) {
      console.error('クイズの投稿に失敗しました', error);
    }
  }

  // watch
  const choices = watch("choices");

  const generateChoicesForm = () => {
    const choicesForms = [];
    for (let i = 0; i < 3; i++) {
      choicesForms.push(
        <div key={i} className="form-item">
          <label>
            <span>選択肢 {i + 1}</span>
            <div>
              <label>
                Question ID:
                <input
                  type="number"
                  {...register(`choices.${i}.question_id`, {
                    required: "Question IDを入力してください",
                  })}
                />
              </label>
              <label>
                Name:
                <input
                  type="text"
                  {...register(`choices.${i}.name`, {
                    required: "名前を入力してください",
                  })}
                />
              </label>
              <label>
                Valid:
                <input
                  type="checkbox"
                  {...register(`choices.${i}.valid`)}
                />
              </label>
            </div>
          </label>
        </div>
      );
    }
    return choicesForms;
  };

  const choicesForms = generateChoicesForm();

 

  return (
    <div className="wrapper">
      <h1>React Form</h1>
      <section className="section">
        <h2>useState Form</h2>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="form-item">
            <label>
              <span>質問</span>
              <input
                type="text"
                {...register("content", {
                  required: "質問を入力してください",
                  maxLength: {
                    value: 255,
                    message: "255文字以下で入力してください",
                  },
                })}
              />
            </label>
            {errors.content?.message && (
              <p className="error-message">{errors.content?.message}</p>
            )}
          </div>
          <div className="form-item">
            <label>
              <span>補足</span>
              <input
                type="text"
                {...register("supplement", {
                  required: "補足を入力してください",
                })}
              />
            </label>
            {errors.supplement?.message && (
              <p className="error-message">{errors.supplement?.message}</p>
            )}
          </div>

          {choicesForms}
          
          <input type="submit" value="Submit" />
        </form>
      </section>
    </div>
  );
};

export default NewQuiz;
