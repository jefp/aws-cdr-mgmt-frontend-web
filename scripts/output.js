
var fs = require('fs');
function handler (data, serverless, options) {
  var logStream = fs.createWriteStream("web/config/"+serverless.getProvider('aws').getStage()+".js", {'flags': 'w'});
  
  logStream.write('const awsmobile = {\n');
  logStream.write('aws_project_region: "us-east-1",\n');
  logStream.write('aws_cognito_region: "us-east-1",\n');
  logStream.write('aws_appsync_region: "us-east-1",\n');
  logStream.write('aws_appsync_authenticationType: "AMAZON_COGNITO_USER_POOLS",\n');
  logStream.write('aws_cognito_identity_pool_id: "'+data['IdentityPoolId']+'",\n');
  logStream.write('aws_user_pools_id: "'+data['CognitoUserPoolId']+'",\n');
  logStream.write('aws_user_pools_web_client_id: "'+data['CognitoUserPoolClientId']+'",\n');
  logStream.write('aws_appsync_graphqlEndpoint: "'+data['AppsyncUrl']+'",\n');
  logStream.write('Auth: {\n');
  logStream.write('  identityPoolId: "'+data['IdentityPoolId']+'",\n');
  logStream.write('  region: "us-east-1",\n');
  logStream.write('  userPoolId: "'+data['CognitoUserPoolId']+'",\n');
  logStream.write('  userPoolWebClientId: "'+data['CognitoUserPoolClientId']+'"\n');
  logStream.write('},\n');
  logStream.write('API: {\n');
  logStream.write(' endpoints: [{\n');
  logStream.write(' name: "stats-rest-api",\n');
  logStream.write(' path: "/stats",\n');
  logStream.write(' endpoint: "'+data['ServiceEndpoint']+'",\n');
  logStream.write('}]}\n');
  logStream.write('};\n');
  logStream.end('export default awsmobile;\n');

  console.log('Received Stack Output', data)
}

module.exports = { handler }
