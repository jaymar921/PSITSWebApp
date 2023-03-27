import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { Pressable } from "react-native";
import { useNavigation, StackActions } from "@react-navigation/native";
import { Ionicons } from "@expo/vector-icons";
export default function HeaderBackMain() {
  const navigation = useNavigation();
  return (
    <Pressable
      onPress={() => navigation.dispatch(StackActions.replace("Main"))}
      style={styles.header}
    >
      <Ionicons name="arrow-back-sharp" size={24} color="black" />
      <Text style={{ marginLeft: 5, fontSize: 17 }}>Back</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 5,
  },
});
