/* 
 * Primary file for the API
 *
 */

 // Dependencies
 var http = require('http');
 var url = require('url');

 // The server should respond to all requests with a string
 var server = http.createServer(function(req, res){

 	// Get the URL and parse it
 	var parsedUrl = url.parse(req.url,true);

 	// Get the path from the URL
 	var path = parsedUrl.pathname;

 	// This regex trimms off the slashes on the begin/end of the request
 	var trimmedPath = path.replace(/^\/+|\/+$/g,'');

 	// Get the query string as an object
 	var queryStringObject = parsedUrl.query;

 	// Get the HTTP Method
 	var method = req.method.toLowerCase();

 	// Ger the headers as an object
 	var headers = req.headers;

 	// Get the payload

 	// Send the response
 	res.end('Hello World\n'); 	

 	// Log the request path
 	console.log('Request received with these headers: ' , headers);
 });

 // Start the server, and have it listen on port 3000
 server.listen(3000, function(){
 	console.log("The server is listening on port 3000 now");
 });

