const express = require("express");
const cases = express.Router();
const { Case } = require("../models");
const cors = require("cors");
cases.use(cors());

cases.get("/", (req, res) => {
  Case.findAll()
    .then((cases) => {
      res.json(cases);
    })
    .catch((err) => {
      console.error(err);
    });
});

module.exports = cases;
