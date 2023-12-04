import { Box, CircularProgress } from '@mui/material';

type Props = {
  height?: string | number;
};

export default function Loader({ height = 500 }: Props) {
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height,
      }}
    >
      <CircularProgress />
    </Box>
  );
}
