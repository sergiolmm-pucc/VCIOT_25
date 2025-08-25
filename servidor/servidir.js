const express = require('express');
const app = express();
const port = 8000; // Escolha a porta que desejar

app.get('/', (req, res) => {
    res.send('<h1>Olá da minha rede!<h1>');
});

app.get('/json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({ a: 1, b: "Sergio" }, null, 3));

});


app.listen(port, () => {
    console.log(`Servidor a correr em http://localhost:${port}`);
});