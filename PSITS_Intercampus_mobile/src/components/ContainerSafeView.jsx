import React from "react";
import { SafeAreaView } from "react-native";
import { Text } from "react-native";
import { ScrollView } from "react-native";
import { Platform } from "react-native";
import { StatusBar } from "react-native";
import { useWindowDimensions } from "react-native";

export default function ContainerSafeView({ children }) {
  const { width } = useWindowDimensions();
  return (
    <SafeAreaView
      style={{
        paddingTop: Platform.OS === "android" ? StatusBar.currentHeight : 0,
        paddingHorizontal: width * 0.065,
        flex: 1,
        backgroundColor: "#F5F5F5",
      }}
    >
      <ScrollView showsVerticalScrollIndicator={false}>{children}</ScrollView>
    </SafeAreaView>
  );
}
