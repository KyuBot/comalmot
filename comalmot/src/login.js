import React, {Component, useState, useEffect} from 'react';
import {StyleSheet, Text, View, Image} from 'react-native';
import CustomButton from './CustomButton';
import Hamburger from 'react-native-hamburger';
import {
  GoogleSignin,
  GoogleSigninButton,
  statusCodes,
} from '@react-native-community/google-signin';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      active: false,
      pushData: [],
      loggedIn: false,
    };
  }
  componentDidMount() {
    GoogleSignin.configure({
      webClientId:
        '908068370908-4a2mer5q4jtel697qv6h5viocn5bv4bg.apps.googleusercontent.com',
      offlineAccess: true,
      hostedDomain: '',
      forceConsentPrompt: true,
    });
  }
  _signIn = async () => {
    try {
      await GoogleSignin.hasPlayServices();
      const userInfo = await GoogleSignin.signIn();
      this.setState({userInfo: userInfo, loggedIn: true});
    } catch (error) {
      if (error.code === statusCodes.SIGN_IN_CANCELLED) {
        // user cancelled the login flow
      } else if (error.code === statusCodes.IN_PROGRESS) {
        // operation (f.e. sign in) is in progress already
      } else if (error.code === statusCodes.PLAY_SERVICES_NOT_AVAILABLE) {
        // play services not available or outdated
      } else {
        // some other error happened
      }
    }
  };
  isSignedIn = async () => {
    const isSignedIn = await GoogleSignin.isSignedIn();
    this.setState({isLoginScreenPresented: !isSignedIn});
  };
  getCurrentUser = async () => {
    const currentUser = await GoogleSignin.getCurrentUser();
    this.setState({currentUser});
  };
  signOut = async () => {
    try {
      await GoogleSignin.revokeAccess();
      await GoogleSignin.signOut();
      this.setState({user: null, loggedIn: false});
    } catch (error) {
      console.error(error);
    }
  };

  render() {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Hamburger
            active={this.state.active}
            type="spinArrow"
            onPress={() => this.setState({active: !this.state.active})}
          />
        </View>
        <View style={styles.title}>
          <Text style={{fontSize: 35, color: 'black'}}>
            어서와,{'\n'}컴알못이지?
          </Text>
        </View>
        <View style={styles.content}>
          <Image
            style={{height: '100%', width: '100%', resizeMode: 'contain'}}
            source={require('./img/main.png')}
          />
        </View>
        <View style={styles.footer}>
          <GoogleSigninButton
            style={{width: 192, height: 48}}
            size={GoogleSigninButton.Size.Wide}
            color={GoogleSigninButton.Color.Dark}
            onPress={this._signIn}
            disabled={this.state.isSigninInProgress}
          />
          <CustomButton
            buttonColor={'#023e73'}
            title={'로그인'}
            onPress={() => alert('로그인 버튼')}
          />
          <View style={styles.buttonContainer}>
            {!this.state.loggedIn && <Text>You are currently logged out</Text>}
            {this.state.loggedIn && (
              <Button
                onPress={this.signOut}
                title="Signout"
                color="#841584"></Button>
            )}
          </View>
          {this.state.loggedIn && (
            <View>
              <View style={styles.listHeader}>
                <Text>User Info</Text>
              </View>
              <View style={styles.dp}>
                <Image
                  style={{width: 100, height: 100}}
                  source={{
                    uri:
                      this.state.userInfo &&
                      this.state.userInfo.user &&
                      this.state.userInfo.user.photo,
                  }}
                />
              </View>
              <View style={styles.detailContainer}>
                <Text style={styles.title}>Name</Text>
                <Text style={styles.message}>
                  {this.state.userInfo &&
                    this.state.userInfo.user &&
                    this.state.userInfo.user.name}
                </Text>
              </View>
              <View style={styles.detailContainer}>
                <Text style={styles.title}>Email</Text>
                <Text style={styles.message}>
                  {this.state.userInfo &&
                    this.state.userInfo.user &&
                    this.state.userInfo.user.email}
                </Text>
              </View>
              <View style={styles.detailContainer}>
                <Text style={styles.title}>ID</Text>
                <Text style={styles.message}>
                  {this.state.userInfo &&
                    this.state.userInfo.user &&
                    this.state.userInfo.user.id}
                </Text>
              </View>
            </View>
          )}
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  listHeader: {
    backgroundColor: '#eee',
    color: '#222',
    height: 44,
    padding: 12,
  },
  detailContainer: {
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    paddingTop: 10,
  },
  message: {
    fontSize: 14,
    paddingBottom: 15,
    borderBottomColor: '#ccc',
    borderBottomWidth: 1,
  },
  dp: {
    marginTop: 32,
    paddingHorizontal: 24,
    flexDirection: 'row',
    justifyContent: 'center',
  },
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
    flexDirection: 'row',
    justifyContent: 'center',
  },
  buttonContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
    flexDirection: 'row',
    justifyContent: 'center',
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
