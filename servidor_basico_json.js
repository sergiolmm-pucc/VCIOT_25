const http = require('http');

//const hostname = '192.168.0.11'; // Localhost
const hostname = '0.0.0.0'; // '0.0.0.0' faz o servidor escutar em todos os IPs da máquina, incluindo na rede local
const port = 3000;

const data = {
  message: 'Aula de VCIOT !',
  timestamp: new Date().toISOString()
};

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json'); // Set content type to JSON
  res.end(JSON.stringify(data)); // Convert JavaScript object to JSON string and send
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});