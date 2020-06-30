const awsmobile = {
aws_project_region: "us-east-1",
aws_cognito_region: "us-east-1",
aws_appsync_region: "us-east-1",
aws_appsync_authenticationType: "AMAZON_COGNITO_USER_POOLS",
aws_cognito_identity_pool_id: "us-east-1:a3d9ff0e-434c-49db-bfa1-a55ea2622073",
aws_user_pools_id: "us-east-1_IEMStMdeY",
aws_user_pools_web_client_id: "2d2rq1db9j3e6rjm4s5k415bs",
aws_appsync_graphqlEndpoint: "https://tybap4gesngotb5jeoq6nk3aiu.appsync-api.us-east-1.amazonaws.com/graphql",
Auth: {
  identityPoolId: "us-east-1:a3d9ff0e-434c-49db-bfa1-a55ea2622073",
  region: "us-east-1",
  userPoolId: "us-east-1_IEMStMdeY",
  userPoolWebClientId: "2d2rq1db9j3e6rjm4s5k415bs"
},
API: {
 endpoints: [{
 name: "stats-rest-api",
 path: "/stats",
 endpoint: "https://k70eswvagi.execute-api.us-east-1.amazonaws.com/prd",
}]}
};
export default awsmobile;
