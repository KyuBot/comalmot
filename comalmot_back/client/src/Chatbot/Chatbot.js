import React, { useEffect } from "react";
import Axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { saveMessage } from "../_actions/message_actions";
import Message from "./Sections/Message";
import { List, Avatar } from "antd";
import { RobotOutlined, SmileOutlined } from "@ant-design/icons";
import Card from "./Sections/Card";

function Chatbot() {
  const dispatch = useDispatch();
  const messageFromRedux = useSelector((state) => state.message.messages);

  useEffect(() => {
    eventQuery("welcomeToComalmot");
  }, []);

  const textQuery = async (text) => {
    //  First  Need to  take care of the message I sent
    let conversation = {
      who: "user",
      content: {
        text: {
          text: text,
        },
      },
    };

    dispatch(saveMessage(conversation));
    // console.log('text I sent', conversation)

    // We need to take care of the message Chatbot sent
    const textQueryVariables = {
      text,
    };

    try {
      const response = await Axios.post(
        "/back/chatbots/textQuery",
        textQueryVariables
      );
      for (let content of response.data.fulfillmentMessages) {
        conversation = {
          who: "bot",
          content: content,
        };

        dispatch(saveMessage(conversation));

        console.log(conversation);
      }
    } catch (err) {
      conversation = {
        who: "bot",
        content: {
          text: {
            text: "error!!",
          },
        },
      };
      dispatch(saveMessage(conversation));
      console.log(conversation);
    }
  };

  const eventQuery = async (event) => {
    // dispatch(saveMessage(conversation))
    // console.log('text I sent', conversation)

    // We need to take care of the message Chatbot sent
    const eventQueryVariables = {
      event,
    };

    try {
      const response = await Axios.post(
        "/back/chatbots/eventQuery",
        eventQueryVariables
      );
      for (let content of response.data.fulfillmentMessages) {
        let conversation = {
          who: "bot",
          content: content,
        };

        dispatch(saveMessage(conversation));

        console.log(conversation);
      }
    } catch (err) {
      let conversation = {
        who: "bot",
        content: {
          text: {
            text: "error!!",
          },
        },
      };
      dispatch(saveMessage(conversation));

      console.log(conversation);
    }
  };

  const keyPressHandler = (e) => {
    if (e.key === "Enter") {
      if (!e.target.value) {
        return alert("you need to type somthing first");
      }

      //we will send request to text query route
      textQuery(e.target.value);

      e.target.value = "";
    }
  };

  const renderCards = (cards) => {
    return cards.map((card, i) => <Card key={i} cardInfo={card.structValue} />);
  };

  const renderOneMessage = (message, i) => {
    console.log("message", message);

    // we need to give some condition here to separate message kinds

    // template for normal text
    if (message.content && message.content.text && message.content.text.text) {
      return (
        <Message key={i} who={message.who} text={message.content.text.text} />
      );
    } else if (message.content && message.content.payload.fields.card) {
      const AvatarSrc =
        message.who === "bot" ? <RobotOutlined /> : <SmileOutlined />;

      return (
        <div>
          <List.Item style={{ padding: "1rem" }}>
            <List.Item.Meta
              avatar={<Avatar icon={AvatarSrc} />}
              title={message.who}
              description={renderCards(
                message.content.payload.fields.card.listValue.values
              )}
            />
          </List.Item>
        </div>
      );
    }
  };

  const renderMessage = (returnedMessages) => {
    if (returnedMessages) {
      return returnedMessages.map((message, i) => {
        return renderOneMessage(message, i);
      });
    } else {
      return null;
    }
  };
  return (
    <div
      style={{
        height: 700,
        width: 700,
        border: "3px solid black",
        borderRadius: "7px",
      }}
    >
      <div style={{ height: 644, width: "100%", overflow: "auto" }}>
        {renderMessage(messageFromRedux)}
      </div>
      <input
        style={{
          margin: 0,
          width: "100%",
          height: 50,
          borderRadius: "4px",
          padding: "5px",
          fontSize: "1rem",
        }}
        placeholder="Send a message..."
        onKeyPress={keyPressHandler}
        type="text"
      />
    </div>
  );
}

export default Chatbot;
