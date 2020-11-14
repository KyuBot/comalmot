const express = require("express");
const gpus = express.Router();
const { Gpu } = require("../models");
const cors = require("cors");
gpus.use(cors());

gpus.get("/", (req, res) => {
  Gpu.findAll()
    .then((gpus) => {
      res.json(gpus);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = gpus;
