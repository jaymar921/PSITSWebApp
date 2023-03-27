import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { TextInput } from "react-native";

export default function CustomInput({ value, setValue, password = false }) {
  return (
    <View>
      <TextInput
        value={value}
        onChangeText={setValue}
        style={styles.inputStyle}
        secureTextEntry={password}
        placeholder={password ? "Password" : "Enter id number"}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  inputStyle: {
    paddingHorizontal: 16,
    paddingVertical: 13,
    backgroundColor: "white",
    borderRadius: 10,
  },
});
