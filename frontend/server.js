const express = require('express');
const path = require('path');
const app = express();

const PORT = 3000;
const BUILD_DIR = path.join(__dirname, 'build');

// Serve static files from the build directory
app.use(express.static(BUILD_DIR));

// For all other routes, serve index.html (React Router handling)
app.get('*', (req, res) => {
  res.sendFile(path.join(BUILD_DIR, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`[RacketHero] Frontend server running on http://localhost:${PORT}`);
});
