const cors = require("cors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const app = express();
const port = process.env.PORT || 3000;
// const sequelize = require("./models").sequelize;
// sequelize.sync();

// app.use(require("connect-history-api-fallback")());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));
app.use(cors());

const Case = require("./routes/Cases");
const Cpu = require("./routes/Cpus");
const Dreclist = require("./routes/Dreclists");
const Gpu = require("./routes/Gpus");
const Laptop = require("./routes/Laptops");
const Lreclist = require("./routes/Lreclists");
const Motherboard = require("./routes/Motherboards");
const Ram = require("./routes/Rams");
const Storage = require("./routes/Storages");

app.use("/web/cases", Case);
app.use("/web/cpus", Cpu);
app.use("/web/dreclists", Dreclist);
app.use("/web/gpus", Gpu);
app.use("/web/laptops", Laptop);
app.use("/web/lreclists", Lreclist);
app.use("/web/motherboards", Motherboard);
app.use("/web/rams", Ram);
app.use("/web/storages", Storage);

module.exports = app;

app.listen(port, () => console.log(`Listening on port ${port}`));
