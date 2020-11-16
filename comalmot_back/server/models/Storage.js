module.exports = (sequelize, DataTypes) => {
  return sequelize.define(
    "storage",

    {
      id: {
        type: DataTypes.BIGINT,
        allowNull: false,
        primaryKey: true,
        autoIncrement: true,
      },
      purpose: {
        type: DataTypes.STRING(50),
        allowNull: true,
      },
      name: {
        type: DataTypes.STRING(100),
        allowNull: false,
      },
      price: {
        type: DataTypes.STRING(50),
        allowNull: false,
      },
      hs: {
        type: DataTypes.TINYINT,
        allowNull: false,
      },
      speed: {
        type: DataTypes.BIGINT,
        allowNull: false,
      },
    },
    {
      timestamps: false,
    }
  );
};
