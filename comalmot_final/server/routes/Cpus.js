const express = require("express");
const cpus = express.Router();
const { Cpu } = require("../models");
const cors = require("cors");
cpus.use(cors());

cpus.get("/", (req, res) => {
  Cpu.findAll()
    .then((cpus) => {
      res.json(cpus);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = cpus;
