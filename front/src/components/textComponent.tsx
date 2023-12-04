import { Box, TextField, Typography } from "@mui/material";
import { FC } from "react";
import { Controller } from "react-hook-form";

type TextProps = {
  name: string;
  label: string;
  control: any;
  errors: any;
};

const TextComponent: FC<TextProps> = ({ name,label, control, errors }) => {
  return (
    <>
    <Controller
      name={name}
      control={control}
      render={({ field }) => (
        <><TextField
          {...field}
          type="text"
          label={label}
          error={!!errors[name]}
          />
          {errors&&(
          <Box>
            {errors[name]?.message}
          </Box>
          )}
          </>
      )}
    />
    </>
  );
};

export default TextComponent;
