import { Text, View } from "react-native";
import React from "react";
import ContainerSafeView from "../../components/ContainerSafeView";
import { BarCodeScanner } from "expo-barcode-scanner";
import { useWindowDimensions } from "react-native";
import DashlineText from "../../components/DashlineText";
import useScanner from "../../hooks/useScanner";
import CodeComponent from "../../components/CodeComponent";
import { MaterialIcons } from "@expo/vector-icons";
import { Pressable } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
export default function Main() {
  const { height } = useWindowDimensions();
  const navigation = useNavigation();
  const { scanned, handleBarCodeScanned, hasPermission } = useScanner();

  if (hasPermission === null) {
    return (
      <ContainerSafeView>
        <Text>Requesting for camera permission</Text>
      </ContainerSafeView>
    );
  }

  if (hasPermission === false) {
    return (
      <ContainerSafeView>
        <Text>No access to camera</Text>
      </ContainerSafeView>
    );
  }

  const handleLogout = async () => {
    AsyncStorage.clear()
      .then(() => navigation.navigate("Login"))
      .catch((err) => console.error(err));
  };

  return (
    <ContainerSafeView>
      <Pressable
        style={{
          marginTop: 10,
          flexDirection: "row",
          justifyContent: "flex-end",
          alignItems: "center",
        }}
        onPress={handleLogout}
      >
        <MaterialIcons name="logout" size={24} color="#904e4e" />
        <Text style={{ marginLeft: 5, color: "#904e4e" }}>Logout</Text>
      </Pressable>
      <View
        style={{ borderRadius: 10, backgroundColor: "gray", marginTop: 20 }}
      >
        <BarCodeScanner
          onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
          style={{ width: undefined, height: height * 0.6 }}
        />
      </View>

      <DashlineText text="or" />

      <CodeComponent />
    </ContainerSafeView>
  );
}
