import { Quiz } from "../api/@types";
import { QuizSchema } from "../schema";
import { useForm, useWatch, SubmitHandler } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { useState } from "react";
import { apiClient } from "../utils/client";


const useQuizForm = () => {
  const {
    control,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<Quiz>({
    mode: "onChange",
    reValidateMode: "onBlur",
    defaultValues: undefined,
    resolver: zodResolver(QuizSchema),
  });

  const watchedInput = useWatch({ control });
  console.log(watchedInput)
  console.log(errors)

  //loading
  const [isLoading, setLoading] = useState(false)

  const onSubmit: SubmitHandler<QuizSchema> = async(data) => {
    try {
      setLoading(true)
      const validatedData = QuizSchema.parse(data);
      const response = await apiClient.admin.quizes.$post({ body: validatedData });
      console.log(response);
      reset();
    } catch (error) {
      console. error("クイズの投稿に失敗しました", error);
    } finally{
      setLoading(false)
    }
  }
  
  
  

  return {
    control,
    handleSubmit,
    onSubmit,
    errors,
    isLoading
  };
};

export default useQuizForm;
