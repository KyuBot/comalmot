import React from "react";
import { AutoComplete, Card } from "antd";
import { LinkOutlined } from "@ant-design/icons";
const { Meta } = Card;

function CardComponent(props) {
  return (
    <Card
      style={{ width: 300 }}
      cover={
        <img
          alt={props.cardInfo.fields.description.stringValue}
          src={props.cardInfo.fields.image.stringValue}
          style={{ width: 150, height: 150, marginLeft: 75 }}
        />
      }
      actions={[
        <a
          target="_blank"
          rel="noopener noreferrer"
          href={props.cardInfo.fields.link.stringValue}
        >
          <LinkOutlined />
        </a>,
      ]}
    >
      <Meta
        title={props.cardInfo.fields.stack.stringValue}
        description={props.cardInfo.fields.description.stringValue}
      />
    </Card>
  );
}

export default CardComponent;
