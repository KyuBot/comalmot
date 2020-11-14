const express = require("express");
const motherboards = express.Router();
const { Motherboard } = require("../models");
const cors = require("cors");
motherboards.use(cors());

motherboards.get("/", (req, res) => {
  Motherboard.findAll()
    .then((motherboards) => {
      res.json(motherboards);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = motherboards;
