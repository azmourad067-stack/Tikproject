import type { ReactNode } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, TextInput, type TextInputProps } from "react-native";
import { useColors } from "../theme";

export function Button(props: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  loading?: boolean;
  variant?: "primary" | "secondary";
}) {
  const c = useColors();
  const primary = (props.variant ?? "primary") === "primary";
  const off = props.disabled || props.loading;
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ disabled: !!off, busy: !!props.loading }}
      onPress={props.onPress}
      disabled={off}
      style={({ pressed }) => [
        styles.button,
        primary
          ? { backgroundColor: c.accent }
          : { backgroundColor: "transparent", borderWidth: 1, borderColor: c.border },
        { opacity: off ? 0.5 : pressed ? 0.8 : 1 },
      ]}
    >
      {props.loading ? (
        <ActivityIndicator color={primary ? c.accentText : c.text} />
      ) : (
        <Text style={[styles.buttonText, { color: primary ? c.accentText : c.text }]}>{props.title}</Text>
      )}
    </Pressable>
  );
}

export function Field(props: TextInputProps & { label: string }) {
  const c = useColors();
  const { label, style, ...rest } = props;
  return (
    <>
      <Text style={[styles.label, { color: c.text }]}>{label}</Text>
      <TextInput
        placeholderTextColor={c.muted}
        {...rest}
        style={[
          styles.input,
          { color: c.text, backgroundColor: c.surface, borderColor: c.border },
          rest.multiline && { minHeight: 110, textAlignVertical: "top" },
          style,
        ]}
      />
    </>
  );
}

export function Muted({ children }: { children: ReactNode }) {
  const c = useColors();
  return <Text style={{ color: c.muted, fontSize: 14, lineHeight: 20 }}>{children}</Text>;
}

export function ErrorText({ children }: { children: ReactNode }) {
  const c = useColors();
  if (!children) return null;
  return <Text accessibilityRole="alert" style={{ color: c.error, fontSize: 15 }}>{children}</Text>;
}

const styles = StyleSheet.create({
  button: { minHeight: 50, borderRadius: 14, alignItems: "center", justifyContent: "center", paddingHorizontal: 18 },
  buttonText: { fontSize: 17, fontWeight: "700" },
  label: { fontSize: 15, fontWeight: "600", marginBottom: 6 },
  input: { borderWidth: 1, borderRadius: 12, paddingHorizontal: 14, paddingVertical: 12, fontSize: 16 },
});
