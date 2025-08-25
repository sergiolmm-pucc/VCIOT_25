const http = require('http'); // Import the built-in http module

// Define o endereço e a porta em que o servidor vai escutar
const hostname = '0.0.0.0'; // '0.0.0.0' faz o servidor escutar em todos os IPs da máquina, incluindo na rede local
//const hostname = '192.168.0.11'; // Localhost IP address
const port = 3000; // Port to listen on

// Create a server instance
const server = http.createServer((req, res) => {
  // Set the HTTP header for a successful response (200 OK)
  // and specify that the content type is HTML
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');

  // Send the HTML content as the response body
  res.end(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Node.js Basic Page</title>
    </head>
    <body>
        <h1>Aula de VC e  IOT</h1>
    </body>
    </html>
  `);
});

// Start the server and listen for incoming requests
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});