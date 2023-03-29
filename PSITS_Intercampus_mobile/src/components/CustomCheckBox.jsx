import { StyleSheet, Text, View } from "react-native";
import React from "react";
import Checkbox from "expo-checkbox";

export default function CustomCheckBox({ value, setValue, text }) {
  return (
    <View style={styles.section}>
      <Checkbox
        style={styles.checkbox}
        value={value}
        onValueChange={setValue}
        color={value ? "#00b4d8" : undefined}
      />
      <Text style={{ marginLeft: 10 }}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    flexDirection: "row",
    alignItems: "center",
  },
  checkbox: {
    marginVertical: 8,
  },
});
