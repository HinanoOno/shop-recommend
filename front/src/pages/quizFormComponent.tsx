import useQuizForm from "./quizForm";
import {
  Box,
  Button,
  Typography,
  TextField,
  Checkbox,
  FormControlLabel,
} from "@mui/material";
import { useForm, Controller } from "react-hook-form";
import TextComponent from "../components/textComponent";
import Loader from "../components/loader";

const QuizFormComponent = () => {
  const { control, handleSubmit, onSubmit, errors, isLoading } = useQuizForm();
  

  return (
    !isLoading?(
    <Box component="form" onSubmit={handleSubmit(onSubmit)}>
      <TextComponent
        name="content"
        label="質問内容"
        control={control}
        errors={errors}
      />
      <TextComponent
        name="image"
        label="画像"
        control={control}
        errors={errors}
      />
      <TextComponent
        name="supplement"
        label="補足"
        control={control}
        errors={errors}
      />
      {[0, 1, 2].map((index) => (
        <div key={index}>
          <Controller
            name={`choices.${index}.question_id`}
            control={control}
            render={({ field }) => (
              <>
                <TextField
                  {...field}
                  type="string"
                  label="番号"
                  error={!!errors.choices}
                />
                {errors && errors.choices && (
                  <Box component="span" color="error.main">
                    {errors.choices[index]?.question_id?.message}
                  </Box>
                )}
              </>
            )}
          />

          <TextComponent
            name={`choices.${index}.name`}
            label="選択肢"
            control={control}
            errors={errors}
          />
          <Controller
            name={`choices.${index}.valid`}
            control={control}
            render={({ field }) => (
              <>
                <TextField
                  {...field}
                  type="checkbox"
                  label="正誤"
                  error={!!errors.choices}
                />
              </>
            )}
          />
        </div>
      ))}

      <Button type="submit" variant="outlined">
        登録
      </Button>
    </Box>
  ):(
    <Loader/>
  ));
};

export default QuizFormComponent;
