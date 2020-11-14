const express = require("express");
const chatbots = express.Router();
const cors = require("cors");
chatbots.use(cors());

// const config = require("../config/dev")
const dialogflow = require("dialogflow");
const uuid = require("uuid");

const sessionId = uuid.v4();
const projectId = "practice-yiyp";
const sessionClient = new dialogflow.SessionsClient({
  keyFilename:
    "C:/Users/multicampus/Desktop/final_pjt/s03p31b206/comalmot/server/routes/practice-yiyp-3c387a682e3f.json",
});
const sessionPath = sessionClient.sessionPath(projectId, sessionId);

chatbots.post("/textQuery", async (req, res) => {
  //We need to send some information that comes from the client to Dialogflow API
  // The text query request.
  const request = {
    session: sessionPath,
    queryInput: {
      text: {
        // The query to send to the dialogflow agent
        text: req.body.text,
        // The language used by the client (en-US)
        languageCode: "ko",
      },
    },
  };

  // Send request and log result
  const responses = await sessionClient.detectIntent(request);
  console.log("Detected intent");
  const result = responses[0].queryResult;
  console.log(`  Query: ${result.queryText}`);
  console.log(`  Response: ${result.fulfillmentText}`);

  res.send(result);
});

chatbots.post("/eventQuery", async (req, res) => {
  //We need to send some information that comes from the client to Dialogflow API
  // The text query request.
  const request = {
    session: sessionPath,
    queryInput: {
      event: {
        // The query to send to the dialogflow agent
        name: req.body.event,
        // The language used by the client (en-US)
        languageCode: "ko",
      },
    },
  };

  // Send request and log result
  const responses = await sessionClient.detectIntent(request);
  console.log("Detected intent");
  const result = responses[0].queryResult;
  console.log(`  Query: ${result.queryText}`);
  console.log(`  Response: ${result.fulfillmentText}`);

  res.send(result);
});

module.exports = chatbots;

// const dialogflow = require("dialogflow");
// const uuid = require("uuid");

// /**
//  * Send a query to the dialogflow agent, and return the query result.
//  * @param {string} projectId The project to be used
//  */
// async function runSample(projectId = "practice-yiyp") {
//   // A unique identifier for the given session
//   const sessionId = uuid.v4();

//   // Create a new session
//   const sessionClient = new dialogflow.SessionsClient({
//     keyFilename:
//       "C:/Users/multicampus/Desktop/final_pjt/s03p31b206/comalmot/server/routes/practice-yiyp-3c387a682e3f.json",
//   });
//   const sessionPath = sessionClient.sessionPath(projectId, sessionId);

//   // The text query request.
//   const request = {
//     session: sessionPath,
//     queryInput: {
//       text: {
//         // The query to send to the dialogflow agent
//         text: "2",
//         // The language used by the client (en-US)
//         languageCode: "ko",
//       },
//     },
//   };

//   // Send request and log result
//   const responses = await sessionClient.detectIntent(request);
//   console.log("Detected intent");
//   const result = responses[0].queryResult;
//   console.log(`  Query: ${result.queryText}`);
//   console.log(`  Response: ${result.fulfillmentText}`);
//   if (result.intent) {
//     console.log(`  Intent: ${result.intent.displayName}`);
//   } else {
//     console.log(`  No intent matched.`);
//   }
// }

// runSample();
