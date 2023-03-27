import { StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import ContainerSafeView from "../../components/ContainerSafeView";
import { Pressable } from "react-native";
import { StackActions, useNavigation } from "@react-navigation/native";

import HeaderBackMain from "../../components/HeaderBackMain";
import CustomCheckBox from "../../components/CustomCheckBox";
import { useWindowDimensions } from "react-native";
import useSendForm from "../../hooks/useSendForm";
import { ActivityIndicator } from "react-native";
import { Alert } from "react-native";

export default function CheckForm({ route }) {
  const { code, responseData } = route.params;
  const [attended, setAttended] = useState(
    responseData.data.attended === "true"
  );
  const [claimed, setClaimed] = useState(responseData.data.claimed === "true");
  const [loading, setLoading] = useState(false);
  const { height } = useWindowDimensions();
  const navigation = useNavigation();
  const { send } = useSendForm();
  const handleSubmit = async () => {
    setLoading(true);
    const info = {
      regId: responseData.data.id,
      checked: attended,
      option: "attended",
    };

    const info1 = {
      regId: responseData.data.id,
      checked: claimed,
      option: "claimed",
    };

    const res = await Promise.all([
      await send(info, responseData.data.attended, "attended"),
      await send(info1, responseData.data.claimed, "claimed"),
    ]);

    if (res[0] && res[1]) {
      Alert.alert("Info", "Successfully updated.", [
        {
          text: "OK",
          onPress: () => {
            setLoading(false);
            navigation.dispatch(StackActions.replace("Main"));
          },
        },
      ]);
    } else {
      alert("Something went wrong in updating");
      setLoading(false);
    }
  };

  return (
    <ContainerSafeView>
      <HeaderBackMain />

      <View
        style={{
          justifyContent: "space-between",
          height: height * 0.9,
          marginTop: 30,
        }}
      >
        <View>
          <CustomCheckBox
            value={attended}
            setValue={setAttended}
            text="Attended"
          />
          <CustomCheckBox
            value={claimed}
            setValue={setClaimed}
            text="Claimed"
          />
          <Text style={{ marginTop: 10 }}>
            Registration Code: <Text style={{ color: "gray" }}>{code}</Text>
          </Text>
          <Text style={{ marginTop: 10 }}>
            Id No.:{" "}
            <Text style={{ color: "gray" }}>{responseData.data.idno}</Text>
          </Text>
          <Text style={{ marginTop: 10 }}>
            Student Name:{" "}
            <Text style={{ color: "gray" }}>
              {responseData.data.meta_data.split("|")[0]}
            </Text>
          </Text>
          <Text style={{ marginTop: 10 }}>
            Payment:{" "}
            <Text style={{ color: "gray" }}>{responseData.data.payment}</Text>
          </Text>
          <Text style={{ marginTop: 10 }}>
            Shirt Size:{" "}
            <Text style={{ color: "gray" }}>
              {responseData.data.shirt_size}
            </Text>
          </Text>
        </View>

        <Pressable
          style={styles.button}
          onPress={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator />
          ) : (
            <Text style={{ textAlign: "center", fontSize: 18, color: "white" }}>
              Submit
            </Text>
          )}
        </Pressable>
      </View>
    </ContainerSafeView>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 15,
    backgroundColor: "#00b4d8",
    borderRadius: 10,
    marginBottom: 20,
  },
});
