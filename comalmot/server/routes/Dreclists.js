const express = require("express");
const dreclists = express.Router();
const { Dreclist } = require("../models");
const cors = require("cors");
dreclists.use(cors());

dreclists.get("/", (req, res) => {
  Dreclist.findAll()
    .then((dreclists) => {
      res.json(dreclists);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = dreclists;
