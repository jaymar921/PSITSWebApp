import { useEffect, useState } from "react";
import { BarCodeScanner } from "expo-barcode-scanner";
import { useNavigation } from "@react-navigation/native";
import useCheckRegCode from "./useCheckRegCode";
import { Alert } from "react-native";

export default function useScanner() {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);

  const { checkRegCode } = useCheckRegCode();

  const navigation = useNavigation();

  useEffect(() => {
    // setTimeout(() => {
    const getBarCodeScannerPermissions = async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === "granted");
    };

    getBarCodeScannerPermissions();

    return () => {
      setScanned(false);
    };
    // }, 500);
  }, []);

  const handleBarCodeScanned = async ({ data }) => {
    setScanned(true);

    const res = await checkRegCode(data);
    if (res) {
      navigation.navigate("CheckForm", { code: data, responseData: res });
    } else {
      Alert.alert("Warning", "Invalid registration Code", [
        {
          text: "OK",
          onPress: () => {
            setScanned(false);
          },
        },
      ]);
    }
  };

  return { scanned, handleBarCodeScanned, hasPermission };
}
