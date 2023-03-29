import { StyleSheet, Text, View } from "react-native";
import React, { useEffect, useState } from "react";
import { StatusBar } from "react-native";
import { Platform } from "react-native";
import ContainerSafeView from "../../components/ContainerSafeView";
import CustomInput from "../../components/AuthCustomInput";
import { Pressable } from "react-native";
import { useWindowDimensions } from "react-native";
import { useNavigation } from "@react-navigation/native";
import useLogin from "../../hooks/useLogin";
import { ActivityIndicator } from "react-native";
import Checkbox from "expo-checkbox";
import AsyncStorage from "@react-native-async-storage/async-storage";

export default function Login() {
  const [idNo, setIdNo] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [value, setValue] = useState(false);

  const { height } = useWindowDimensions();
  const navigation = useNavigation();
  const { login } = useLogin();

  useEffect(() => {
    const getUserSaved = async () => {
      const idno = await AsyncStorage.getItem("idno");
      const password = await AsyncStorage.getItem("password");

      if (idno !== null && password !== null) {
        navigation.navigate("Main");
      }
    };

    getUserSaved();
  }, []);

  const handleOnLogin = async () => {
    setLoading(true);
    const isPermitted = await login(idNo, password);

    if (isPermitted) {
      try {
        if (value) {
          await AsyncStorage.multiSet([
            ["idno", idNo],
            ["password", password],
          ]);
        }

        navigation.navigate("Main");
      } catch (error) {
        console.error(error);
      }
    } else {
      alert("Invalid Credentials!");
    }

    setLoading(false);
    setPassword("");
    setIdNo("");
  };

  return (
    <ContainerSafeView>
      <View style={{ height: height * 0.25, marginBottom: 50 }}>
        <View style={{ height: height * 0.15, marginTop: height * 0.1 }}>
          <Text style={styles.header}>Hello Admin!</Text>
          <Text style={styles.semiHeader}>Welcome back go break a neck.</Text>
        </View>
      </View>
      <View style={{ height: height * 0.75 }}>
        <CustomInput value={idNo} setValue={setIdNo} />
        <View style={{ marginVertical: 5 }} />
        <CustomInput value={password} setValue={setPassword} password={true} />
        <View
          style={{
            flexDirection: "row",
            alignItems: "center",
            marginTop: 15,
          }}
        >
          <Checkbox
            value={value}
            onValueChange={setValue}
            color={value ? "#00b4d8" : undefined}
          />
          <Text style={{ marginLeft: 7, color: "gray" }}>Stay logged in</Text>
        </View>

        <Pressable
          style={styles.login}
          onPress={handleOnLogin}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator />
          ) : (
            <Text style={styles.loginText}>Login</Text>
          )}
        </Pressable>
      </View>
    </ContainerSafeView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === "android" ? StatusBar.currentHeight : 0,
  },
  login: {
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
  loginText: {
    textAlign: "center",
    color: "white",
    fontWeight: "700",
    fontSize: 20,
  },
});
