module.exports = (sequelize, DataTypes) => {
  return sequelize.define(
    "gpu",

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
        type: DataTypes.BIGINT,
        allowNull: false,
      },
      rate: {
        type: DataTypes.BIGINT,
        allowNull: true,
      },
    },
    {
      timestamps: false,
    }
  );
};
