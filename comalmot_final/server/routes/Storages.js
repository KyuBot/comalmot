const express = require("express");
const storages = express.Router();
const { Storage } = require("../models");
const cors = require("cors");
storages.use(cors());

storages.get("/", (req, res) => {
  Storage.findAll()
    .then((storages) => {
      res.json(storages);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = storages;
