import { StyleSheet, Text, View } from "react-native";
import React from "react";

export default function DashlineText({ text }) {
  return (
    <View style={{ flexDirection: "row", alignItems: "center", marginTop: 30 }}>
      <View style={{ flex: 1, height: 1, backgroundColor: "gray" }} />
      <View>
        <Text style={{ width: 50, textAlign: "center" }}>{text}</Text>
      </View>
      <View style={{ flex: 1, height: 1, backgroundColor: "gray" }} />
    </View>
  );
}

const styles = StyleSheet.create({});
