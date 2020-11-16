// Imports the Google Cloud client library.
const { Storage } = require("@google-cloud/storage");

// Instantiates a client. If you don't specify credentials when constructing
// the client, the client library will look for credentials in the
// environment.
const storage = new Storage();
// Makes an authenticated API request.
async function listBuckets() {
  try {
    const results = await storage.getBuckets();

    const [buckets] = results;

    console.log("Buckets:");
    buckets.forEach((bucket) => {
      console.log(bucket.name);
    });
  } catch (err) {
    console.error("ERROR:", err);
  }
}
listBuckets();
// // Imports the Google Cloud client library
// const { Storage } = require("@google-cloud/storage");

// // Creates a client
// // const storage = new Storage();
// // Creates a client from a Google service account key.
// const storage = new Storage({ keyFilename: "practice-yiyp-3c387a682e3f.json" });

// /**
//  * TODO(developer): Uncomment these variables before running the sample.
//  */
// const bucketName = "bucket-name";

// async function createBucket() {
//   // Creates the new bucket
//   await storage.createBucket(bucketName);
//   console.log(`Bucket ${bucketName} created.`);
// }

// createBucket().catch(console.error);
