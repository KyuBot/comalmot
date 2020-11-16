import React, {useState, useEffect, Component} from 'react';
import {StyleSheet, View, Text, Image, Button} from 'react-native';
import {Header, Colors} from 'react-native/Libraries/NewAppScreen';
import {
  GoogleSignin,
  GoogleSigninButton,
  statusCodes,
} from '@react-native-community/google-signin';
import auth from '@react-native-firebase/auth';

const Login = ({navigation}) => {
  const [loggedIn, setloggedIn] = useState(false);
  const [user, setUser] = useState([]);

  _signIn = async () => {
    try {
      await GoogleSignin.hasPlayServices();
      const {accessToken, idToken} = await GoogleSignin.signIn();
      setloggedIn(true);

      const credential = auth.GoogleAuthProvider.credential(
        idToken,
        accessToken,
      );
      await auth().signInWithCredential(credential);
    } catch (error) {
      if (error.code === statusCodes.SIGN_IN_CANCELLED) {
        // user cancelled the login flow
        alert('Cancel');
      } else if (error.code === statusCodes.IN_PROGRESS) {
        alert('Signin in progress');
        // operation (f.e. sign in) is in progress already
      } else if (error.code === statusCodes.PLAY_SERVICES_NOT_AVAILABLE) {
        alert('PLAY_SERVICES_NOT_AVAILABLE');
        // play services not available or outdated
      } else {
        // some other error happened
      }
    }
  };
  function onAuthStateChanged(user) {
    setUser(user);
    console.log(user);
    if (user) setloggedIn(true);
  }
  useEffect(() => {
    GoogleSignin.configure({
      scopes: ['email'], // what API you want to access on behalf of the user, default is email and profile
      webClientId:
        '908068370908-4a2mer5q4jtel697qv6h5viocn5bv4bg.apps.googleusercontent.com', // client ID of type WEB for your server (needed to verify user ID and offline access)
      offlineAccess: true, // if you want to access Google API on behalf of the user FROM YOUR SERVER
    });
    const subscriber = auth().onAuthStateChanged(onAuthStateChanged);
    return subscriber; // unsubscribe on unmount
  }, []);

  signOut = async () => {
    try {
      await GoogleSignin.revokeAccess();
      await GoogleSignin.signOut();
      auth()
        .signOut()
        .then(() => alert('Your are signed out!'));
      setloggedIn(false);
      // setuserInfo([]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View style={styles.container} contentInsetAdjustmentBehavior="automatic">
      <View style={styles.header}></View>
      <View style={styles.title}></View>
      <View style={styles.content}></View>

      <View style={styles.footer}>
        {!loggedIn && (
          <GoogleSigninButton
            style={{width: 192, height: 48}}
            size={GoogleSigninButton.Size.Wide}
            color={GoogleSigninButton.Color.Light}
            onPress={this._signIn}
          />
        )}
        <View style={styles.buttonContainer}>
          {!user && <Text>You are currently logged out</Text>}
          {user && (
            <View>
              <Text>Welcome {user.displayName}</Text>
              <Button
                onPress={this.signOut}
                title="LogOut"
                color="skyblue"></Button>
            </View>
          )}
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  engine: {
    position: 'absolute',
    right: 0,
  },
  body: {
    backgroundColor: Colors.white,
  },
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: '#fff',
  },
  header: {
    width: '100%',
    height: '5%',
    backgroundColor: '#fff',
  },
  title: {
    width: '100%',
    height: '18%',
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingBottom: 30,
    backgroundColor: '#fff',
  },
  footer: {
    width: '100%',
    height: '20%',
    //backgroundColor: '#1ad657',
  },
});
export default Login;
