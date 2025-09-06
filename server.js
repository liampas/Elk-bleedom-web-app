const express = require('express');
const { exec } = require('child_process');
const app = express();
const path = require('path');

app.use(express.static(__dirname));

// Serve index.html from the same folder
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/run', (req, res) => {
    const hex = req.query.hex;
    exec(`python3 colors.py ${hex}`, (err, stdout) => {
        if (err) return res.send(err.message);
        res.send(stdout);
    });
});

app.get('/off', (req, res) => {
    exec(`python3 colors.py off`, (err, stdout) => {
        if (err) return res.send(err.message);
        res.send(stdout);
    });
});

const { spawn } = require('child_process');
app.get('/scan', (req, res) => {
    spawn(`./scan.sh`, { detached: true, stdio: 'ignore' }).unref();
	res.send('scan started');
});

app.listen(9999, () => console.log('Server running on http://localhost:9999'));

