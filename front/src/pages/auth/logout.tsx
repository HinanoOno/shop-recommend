import { Box, Button, Typography } from "@mui/material";

interface TestLogoutProps {
  user: string;
  onLogout: () => void;
}

export const TestLogout: React.FC<TestLogoutProps> = ({ user, onLogout }) => {
  const handleLogout = () => {
    onLogout();
  };
  return (
    <Box p={3}>
      <Typography>{user}</Typography>
      <Button variant="outlined" fullWidth onClick={handleLogout}>
        Logout!
      </Button>
    </Box>
  );
};
