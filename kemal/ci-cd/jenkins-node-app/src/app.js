// src/app.js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send("Bu urun Jenkins uzerinde CI calistirilarak olusturulmustur, devopsyolu.");
});

module.exports = app;
