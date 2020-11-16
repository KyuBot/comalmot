// // Custom Navigation Drawer / Sidebar with Image and Icon in Menu Options
// // https://aboutreact.com/custom-navigation-drawer-sidebar-with-image-and-icon-in-menu-options/

// import * as React from 'react';
// import {Button, View, Text, SafeAreaView} from 'react-native';

// function ChatbotScreen({navigation}) {
//   return (
//     <SafeAreaView style={{flex: 1}}>
//       <View style={{flex: 1, padding: 16}}>
//         <View
//           style={{
//             flex: 1,
//             alignItems: 'center',
//             justifyContent: 'center',
//           }}>
//           <Text
//             style={{
//               fontSize: 25,
//               textAlign: 'center',
//               marginBottom: 16,
//             }}>
//             This is Second Page under Second Page Option
//           </Text>
//         </View>
//         <Text style={{fontSize: 18, textAlign: 'center', color: 'grey'}}>
//           Custom React Navigate Drawer
//         </Text>
//         <Text style={{fontSize: 16, textAlign: 'center', color: 'grey'}}>
//           www.aboutreact.com
//         </Text>
//       </View>
//     </SafeAreaView>
//   );
// }

// export default ChatbotScreen;

import React, {useState, useEffect, useCallback} from 'react';
import {Image, View, Text, SafeAreaView, Animated} from 'react-native';
import {GiftedChat} from 'react-native-gifted-chat';
import {Dialogflow_V2} from 'react-native-dialogflow';
import {dialogflowConfig} from './env';
import Carousel from './Carousel';
import {YellowBox, LogBox} from 'react-native';
YellowBox.ignoreWarnings([
  'Animated: `useNativeDriver` was not specified. This is a required option and must be explicitly set to `true` or `false`',
  'YellowBox has been replaced with LogBox. Please call LogBox.ignoreLogs() instead.',
  'Animated.event now requires a second argument for options',
]);
// https://i.imgur.com/7k12EPD.png
const BOT_USER = {
  _id: 2,
  name: '컴알봇',
  avatar: require('../assets/comalmot_avator.png'),
};

function ChatbotScreen({navigation}) {
  const [messages, setMessages] = useState([
    {
      _id: 1,
      text: '안녕하세요! 컴퓨터 추천 혹은 고장에 대해 말해주시겠어요?',
      createdAt: new Date(),
      user: BOT_USER,
      image:
        'https://lh3.googleusercontent.com/a-/AOh14GjnADHPA_rML99usua01UySSEONffT4x4kLd6AroA=s88-c-k-c0x00ffffff-no-rj-mo',
    },
  ]);

  useEffect(() => {
    Dialogflow_V2.setConfiguration(
      dialogflowConfig.client_email,
      dialogflowConfig.private_key,
      Dialogflow_V2.LANG_KOREAN,
      dialogflowConfig.project_id,
    );
  }, []);

  function onSend(newMessage = []) {
    setMessages((previousMessages) =>
      GiftedChat.append(previousMessages, newMessage),
    );

    let message = newMessage[0].text;
    Dialogflow_V2.requestQuery(
      message,
      (result) => {
        sendBotResponse(result);
        console.log(result.queryResult.fulfillmentMessages[0]);
        // handleGoogleeResponse(result);
        // if (result.queryResult.fulfillmentMessages[1]) {
        //   console.log(result.queryResult.fulfillmentMessages[1].payload.card);
        //   return (
        //     <Carousel
        //       carditem={result.queryResult.fulfillmentMessages[1].payload.card}
        //     />
        //   );
        // }
        // .fields.card.listValue.values[0]
      },
      (error) => console.log(error),
    );
  }

  // function handleGoogleeResponse(result) {
  //   let text = result.queryResult.fulfillmentMessages[0].text.text[0];
  //   sendBotResponse(text);
  //   // let desc = result.queryResult.fulfillmentMessages[1].payload.card[0].stack;
  //   // sendBotResponse(desc);
  // }

  function sendBotResponse(result) {
    let num = messages.length + 1;
    if (result.queryResult) {
      if (result.queryResult.fulfillmentMessages[1]) {
        let text = result.queryResult.fulfillmentMessages[0].text.text[0];
        let desc = result.queryResult.fulfillmentMessages[1].payload.card;
        let msg1 = {
          _id: num,
          text,
          createdAt: new Date(),
          user: BOT_USER,
          image: '',
        };
        setMessages(
          (previousMessages) => GiftedChat.append(previousMessages, msg1),
          sendBotResponse(desc),
        );
      } else {
        let text = result.queryResult.fulfillmentMessages[0].text.text[0];
        let msg = {
          _id: num,
          text,
          createdAt: new Date(),
          user: BOT_USER,
          image: '',
        };
        setMessages((previousMessages) =>
          GiftedChat.append(previousMessages, msg),
        );
      }
    } else {
      for (item of result) {
        let text = item.stack + '\n' + item.description + '\n' + item.link;
        let img = item.image;
        let msg = {
          _id: num + 1,
          text,
          createdAt: new Date(),
          user: BOT_USER,
          image: img,
        };

        setMessages((previousMessages) =>
          GiftedChat.append(previousMessages, msg),
        );
        num += 1;
      }
    }

    // console.log(messages);
  }

  return (
    <SafeAreaView style={{flex: 1}}>
      <View style={{flex: 1, backgroundColor: '#fff'}}>
        <GiftedChat
          messages={messages}
          onSend={(newMessage) => onSend(newMessage)}
          user={{
            _id: 1,
          }}
        />
      </View>
    </SafeAreaView>
  );
}

export default ChatbotScreen;
