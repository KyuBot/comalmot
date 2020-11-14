import React from "react";
import { List, Avatar } from "antd";
import { RobotOutlined, SmileOutlined } from "@ant-design/icons";

function Message(props) {
  const AvatarSrc = props.who === "bot" ? <RobotOutlined /> : <SmileOutlined />;

  return (
    <List.Item style={{ padding: "1rem" }}>
      <List.Item.Meta
        avatar={<Avatar icon={AvatarSrc} />}
        title={props.who}
        description={props.text}
      />
    </List.Item>
  );
}

export default Message;
