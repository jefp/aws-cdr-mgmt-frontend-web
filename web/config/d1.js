const awsmobile = {
aws_project_region: "us-east-1",
aws_cognito_region: "us-east-1",
aws_appsync_region: "us-east-1",
aws_appsync_authenticationType: "AMAZON_COGNITO_USER_POOLS",
aws_cognito_identity_pool_id: "us-east-1:eb48d4e4-44fa-499a-b23b-bb3d356e8872",
aws_user_pools_id: "us-east-1_t7TXY3FDy",
aws_user_pools_web_client_id: "2qdgj978or9bpdru3nvjufgnpk",
aws_appsync_graphqlEndpoint: "https://rkocvagfwvaopcxznztabnuxaa.appsync-api.us-east-1.amazonaws.com/graphql",
Auth: {
  identityPoolId: "us-east-1:eb48d4e4-44fa-499a-b23b-bb3d356e8872",
  region: "us-east-1",
  userPoolId: "us-east-1_t7TXY3FDy",
  userPoolWebClientId: "2qdgj978or9bpdru3nvjufgnpk"
},
API: {
 endpoints: [{
 name: "stats-rest-api",
 path: "/stats",
 endpoint: "https://nfy06fn3ac.execute-api.us-east-1.amazonaws.com/d1",
}]}
};
export default awsmobile;
