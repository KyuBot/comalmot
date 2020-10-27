import React, {Component} from 'react';
import {StyleSheet, Text, View} from 'react-native';
import CustomButton from './CustomButton';

type Props = {};
export default class App extends Component<Props> {
  render() {
    return (
      <View style={styles.container}>
        <View style={styles.header}><Text>header</Text></View>
        <View style={styles.title}><Text>title</Text></View>
        <View style={styles.content}><Text>content</Text></View>
        <View style={styles.footer}>
          <CustomButton
            buttonColor={'#023e71'}
            title={'회원가입'}
            onPress={() => alert('회원가입 버튼')}/>
          <CustomButton />
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: 'white',
  },
  header: {
    width:'100%',
    height:'9%',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ff9a9a',
  },
  title: {
    width:'100%',
    height:'18%',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#9aa9ff',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#d6ca1a',
  },
  footer: {
    width:'100%',
    height:'20%',
    backgroundColor: '#1ad657',
  },
});