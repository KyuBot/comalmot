const cors = require("cors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const app = express();
const port = process.env.PORT || 5000;
// const sequelize = require("./models").sequelize;
// sequelize.sync();

// app.use(require("connect-history-api-fallback")());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
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
const Chatbot = require("./routes/Chatbots");

app.use("/back/cases", Case);
app.use("/back/cpus", Cpu);
app.use("/back/dreclists", Dreclist);
app.use("/back/gpus", Gpu);
app.use("/back/laptops", Laptop);
app.use("/back/lreclists", Lreclist);
app.use("/back/motherboards", Motherboard);
app.use("/back/rams", Ram);
app.use("/back/storages", Storage);
app.use("/back/chatbots", Chatbot);

module.exports = app;

app.listen(port, () => console.log(`Listening on port ${port}`));
