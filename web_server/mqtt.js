// Authorize Self Sign Certificate
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

const mqtt    = require('mqtt'),
      PARAMS  = {
                  rejectUnauthorized: false,
                  username: 'guest',
                  password: 'guest'
                },
      client  = mqtt.connect('tls://192.168.2.27:1883', PARAMS) // Using SSL.

client.on('connect', function () {
  client.subscribe('State', function (err) {
    if (!err) {
	     console.log("subscribed to State");
    }
  });
});

client.on('message', function (topic, message) {
  console.log(new Date().toISOString());
  console.log(message.toString());
  // to do end the connection, we want to listen all the time.
});
