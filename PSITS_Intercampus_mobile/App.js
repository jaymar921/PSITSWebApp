import { createStackNavigator } from "@react-navigation/stack";
import Main from "./src/views/main/Main";
import CheckForm from "./src/views/check/CheckForm";
import Login from "./src/views/login/Login";
import { NavigationContainer } from "@react-navigation/native";
import InputAddress from "./src/views/ipadd/InputAddress";
const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="InputAddress"
        screenOptions={{
          headerShown: false,
        }}
      >
        <Stack.Screen name="Main" component={Main} />
        <Stack.Screen name="InputAddress" component={InputAddress} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="CheckForm" component={CheckForm} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
