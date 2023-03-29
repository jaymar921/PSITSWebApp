import { StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import { TextInput } from "react-native";
import { Pressable } from "react-native";
import { useNavigation } from "@react-navigation/native";
import useCheckRegCode from "../hooks/useCheckRegCode";
import { Alert } from "react-native";
import { ActivityIndicator } from "react-native";

export default function CodeComponent() {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const { checkRegCode } = useCheckRegCode();

  const navigation = useNavigation();
  const handleSubmit = async () => {
    setLoading(true);
    if (code.trim() === "") return;
    const upper = code.toUpperCase();
    const res = await checkRegCode(upper);

    setLoading(false);
    if (res) {
      navigation.navigate("CheckForm", {
        code: code.toUpperCase(),
        responseData: res,
      });
    } else {
      Alert.alert("", "Invalid Registration Code!", [
        {
          text: "Ok",
          onPress: () => setLoading(false),
        },
      ]);
    }
  };
  return (
    <View>
      <Text style={styles.header}>Enter Registration Code</Text>
      <TextInput
        value={code}
        onChangeText={setCode}
        placeholder="Enter code Here..."
        style={styles.code}
      />
      <Pressable
        style={styles.button}
        onPress={handleSubmit}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator />
        ) : (
          <Text style={{ textAlign: "center", color: "white", fontSize: 18 }}>
            Next
          </Text>
        )}
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  button: {
    padding: 10,
    marginVertical: 20,
    backgroundColor: "#00b4d8",
    borderRadius: 5,
  },
  code: {
    paddingVertical: 10,
    paddingHorizontal: 15,
    backgroundColor: "white",
    borderRadius: 10,
  },
  header: {
    marginVertical: 20,
    textAlign: "center",
    fontSize: 20,
    fontWeight: "600",
  },
});
