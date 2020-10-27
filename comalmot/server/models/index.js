const path = require("path");
const Sequelize = require("sequelize");

const env = process.env.NODE_ENV || "development";
const config = require(path.join(__dirname, "..", "config", "config.json"))[
  env
];
const db = {};

const sequelize = new Sequelize(
  config.database,
  config.username,
  config.password,
  config
);

db.sequelize = sequelize;
db.Sequelize = Sequelize;

db.Cpu = require("./Cpu")(sequelize, Sequelize);
db.Gpu = require("./Gpu")(sequelize, Sequelize);
db.Motherboard = require("./Motherboard")(sequelize, Sequelize);
db.Storage = require("./Storage")(sequelize, Sequelize);
db.Ram = require("./Ram")(sequelize, Sequelize);
db.Case = require("./Case")(sequelize, Sequelize);
db.Laptop = require("./Laptop")(sequelize, Sequelize);
db.Dreclist = require("./Dreclist")(sequelize, Sequelize);
db.Lreclist = require("./Lreclist")(sequelize, Sequelize);

db.Cpu.hasMany(db.Dreclist, { foreignKey: "cpu_id", sourceKey: "id" });
db.Dreclist.belongsTo(db.Cpu, { foreignKey: "cpu_id", targetKey: "id" });

db.Gpu.hasMany(db.Dreclist, { foreignKey: "gpu_id", sourceKey: "id" });
db.Dreclist.belongsTo(db.Gpu, { foreignKey: "gpu_id", targetKey: "id" });

db.Motherboard.hasMany(db.Dreclist, {
  foreignKey: "motherboard_id",
  sourceKey: "id",
});
db.Dreclist.belongsTo(db.Motherboard, {
  foreignKey: "motherboard_id",
  targetKey: "id",
});

db.Ram.hasMany(db.Dreclist, { foreignKey: "ram_id", sourceKey: "id" });
db.Dreclist.belongsTo(db.Ram, { foreignKey: "ram_id", targetKey: "id" });

db.Case.hasMany(db.Dreclist, { foreignKey: "case_id", sourceKey: "id" });
db.Dreclist.belongsTo(db.Case, { foreignKey: "case_id", targetKey: "id" });

db.Storage.hasMany(db.Dreclist, { foreignKey: "storage_id", sourceKey: "id" });
db.Dreclist.belongsTo(db.Storage, {
  foreignKey: "storage_id",
  targetKey: "id",
});

db.Laptop.hasMany(db.Lreclist, { foreignKey: "laptop_id", sourceKey: "id" });
db.Lreclist.belongsTo(db.Laptop, { foreignKey: "laptop_id", targetKey: "id" });

module.exports = db;
