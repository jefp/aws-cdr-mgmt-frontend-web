const CreateJob = `mutation createJob($from: String!,$to: String!,$filter: String) {
  createJob(from: $from, to: $to, filter: $filter) {
    id
    from
    to
    filter
    jobStatus
  }
}`;

const ListJobs = `query listJobs($limit: Int){
  listJobs(limit: $limit) {
    items {
      id
      from
      to
      filter
      jobStatus
      createdAt
      lastUpdated
      expires
      jobStatusDescription
      results
      }
    totalItems
    nextToken
  }
}`;

const getJob = `query getJob{
  getJob {
    items {
      id
      from
      to
      filter
      jobStatus
      createdAt
      lastUpdated
      jobStatusDescription
    }
  }
}`;


export {
  CreateJob,
  ListJobs,
}
