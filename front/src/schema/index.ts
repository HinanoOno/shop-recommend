import { z } from "zod";

const ChoiceSchema = z.object({
  //数値に変換
  question_id: z.preprocess(
    (v) => Number(v),
    z.number()
  ),
  name: z.string().max(255,{message: "255文字以下で入力してください"}),
  valid: z.boolean(),
});

export const QuizSchema = z.object({
  content: z.string().max(2,{message: "255文字以下で入力してください"}),
  image: z.string().optional(),
  supplement: z.string().max(255,{message: "255文字以下で入力してください"}).optional(),
  choices: z.array(ChoiceSchema).optional(),
});

export type QuizSchema = z.infer<typeof QuizSchema>