const express = require("express");
const lreclists = express.Router();
const { Lreclist } = require("../models");
const cors = require("cors");
lreclists.use(cors());

lreclists.get("/", (req, res) => {
  Lreclist.findAll()
    .then((lreclists) => {
      res.json(lreclists);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = lreclists;
