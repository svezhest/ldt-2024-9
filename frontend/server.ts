import express, { Request, Response } from 'express';
import React from 'react';
import ReactDOMServer from 'react-dom/server';
import App from './src/App'; // убедитесь, что App экспортируется как default в App.tsx

const app = express();

app.use(express.static('public'));

app.get('*', (req: Request, res: Response) => {
  const appHTML = ReactDOMServer.renderToString(<App />);

  const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>SSR React App</title>
    </head>
    <body>
      <div id="root">${appHTML}</div>
      <script src="/main.js"></script>
    </body>
    </html>`
  ;

  res.send(html);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});