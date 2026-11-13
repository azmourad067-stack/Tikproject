import { useColorScheme } from "react-native";

const light = {
  bg: "#fffaf7",
  surface: "#ffffff",
  text: "#1d1a1f",
  muted: "#5f5866",
  border: "#e7e1ea",
  accent: "#e0405e",
  accentText: "#ffffff",
  them: "#efeaf2",
  ai: "#fff1d6",
  aiBorder: "#f0c46b",
  error: "#b3261e",
};

const dark: typeof light = {
  bg: "#141216",
  surface: "#1e1b21",
  text: "#f4f0f6",
  muted: "#b3abb9",
  border: "#332e38",
  accent: "#ff5c7a",
  accentText: "#1a0d10",
  them: "#2c2831",
  ai: "#3a3020",
  aiBorder: "#8a6a2a",
  error: "#ff8a80",
};

export type Colors = typeof light;

export function useColors(): Colors {
  return useColorScheme() === "dark" ? dark : light;
}
