import { StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import ContainerSafeView from "../../components/ContainerSafeView";
import { Platform } from "react-native";
import { StatusBar } from "react-native";
import { useWindowDimensions } from "react-native";
import { Pressable } from "react-native";
import { TextInput } from "react-native-gesture-handler";
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function InputAddress() {
  const [ipAdd, setIpAdd] = useState("");
  const [port, setPort] = useState("");

  const { height } = useWindowDimensions();
  const navigation = useNavigation();

  const handleNext = async () => {
    if (ipAdd.trim() === "" || port.trim() === "") {
      alert("Input both details!");
      return;
    }

    await AsyncStorage.multiSet([
      ["ipadd", ipAdd],
      ["port", port],
    ]);

    navigation.navigate("Login");
  };

  return (
    <ContainerSafeView>
      <View style={{ height: height * 0.25, marginBottom: 50 }}>
        <View style={{ height: height * 0.15, marginTop: height * 0.1 }}>
          <Text style={styles.header}>Hello Admin!</Text>
          <Text style={styles.semiHeader}>
            Please input your IP Adress and the port.
          </Text>
        </View>
      </View>
      <View style={{ height: height * 0.75 }}>
        <TextInput
          value={ipAdd}
          onChangeText={setIpAdd}
          style={styles.inputStyle}
          placeholder={"127.0.0.0"}
        />
        <View style={{ marginVertical: 5 }} />
        <TextInput
          value={port}
          onChangeText={setPort}
          style={styles.inputStyle}
          placeholder={"5000"}
        />

        <Pressable style={styles.next} onPress={handleNext}>
          <Text style={styles.buttonText}>Next</Text>
        </Pressable>
      </View>
    </ContainerSafeView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === "android" ? StatusBar.currentHeight : 0,
  },
  next: {
    paddingVertical: 15,
    borderRadius: 10,
    marginTop: 20,
    backgroundColor: "#00b4d8",
  },
  header: {
    textAlign: "center",
    fontSize: 30,
    fontWeight: "700",
    marginBottom: 10,
    opacity: 0.7,
  },
  semiHeader: {
    fontSize: 20,
    opacity: 0.5,
    textAlign: "center",
  },
  buttonText: {
    textAlign: "center",
    color: "white",
    fontWeight: "700",
    fontSize: 20,
  },
  inputStyle: {
    paddingHorizontal: 16,
    paddingVertical: 13,
    backgroundColor: "white",
    borderRadius: 10,
  },
});
