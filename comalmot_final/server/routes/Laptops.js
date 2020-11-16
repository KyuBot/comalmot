const express = require("express");
const laptops = express.Router();
const { Laptop } = require("../models");
const cors = require("cors");
laptops.use(cors());

laptops.get("/", (req, res) => {
  Laptop.findAll()
    .then((laptops) => {
      res.json(laptops);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = laptops;
