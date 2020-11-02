const cors = require("cors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const app = express();
const port = process.env.PORT || 3000;
const sequelize = require("./models").sequelize;
sequelize.sync();

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

app.use("/api/cases", Case);
app.use("/api/cpus", Cpu);
app.use("/api/dreclists", Dreclist);
app.use("/api/gpus", Gpu);
app.use("/api/laptops", Laptop);
app.use("/api/lreclists", Lreclist);
app.use("/api/motherboards", Motherboard);
app.use("/api/rams", Ram);
app.use("/api/storages", Storage);

module.exports = app;

app.listen(port, () => console.log(`Listening on port ${port}`));
