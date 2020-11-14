const express = require("express");
const rams = express.Router();
const { Ram } = require("../models");
const cors = require("cors");
rams.use(cors());

rams.get("/", (req, res) => {
  Ram.findAll()
    .then((rams) => {
      res.json(rams);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = rams;
