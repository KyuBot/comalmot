import 'react-native-gesture-handler';

import * as React from 'react';
import {useState, useEffect, Component} from 'react';
import {NavigationContainer, StackActions} from '@react-navigation/native';
import{Text} from 'react-native';
import HomeScreen from './src/screens/HomeScreen';
import Login from './src/screens/Login';
import ChatbotScreen from './src/screens/ChatbotScreen';
import { createDrawerNavigator } from '@react-navigation/drawer';
import Icon from 'react-native-vector-icons';
import RNKommunicateChat from 'react-native-kommunicate-chat';
const Drawer = createDrawerNavigator();

function App() {
  return (
    <NavigationContainer>
      <Drawer.Navigator initialRouteName="HomeScreen" screenOptions={{
        headerStyle:{
          backgroundColor: '#009387',
        },
        headerTintColor: '#fff',
        headerTitleStyle:{
          fontWeight:'bold'
        },
        headerLeft:(Icon)
        
      }}>
        <Drawer.Screen name="컴알못" component={HomeScreen}/>
        <Drawer.Screen name="로그인" component={Login}/>
        <Drawer.Screen name="챗봇" component={ChatbotScreen}/>
      </Drawer.Navigator>
    </NavigationContainer>
  );
}

export default App;