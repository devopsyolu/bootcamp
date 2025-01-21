// index.mjs
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

export const handler = async (event) => {
  console.log("Event received:", JSON.stringify(event));

  // Check which resource was called
  const resource = event.resource; // e.g. "/hello" or "/upload"
  const method = event.httpMethod || "GET";

  // 1) /hello
  if (resource === "/hello") {
    if (method === "GET") {
      return {
        statusCode: 200,
        body: JSON.stringify({ message: "Hello from Node.js 22!" }),
      };
    } else {
      return {
        statusCode: 405,
        body: JSON.stringify({ error: "Method not allowed on /hello" }),
      };
    }
  }

  // 2) /upload
  if (resource === "/upload") {
    if (method !== "POST") {
      return {
        statusCode: 405,
        body: JSON.stringify({
          error: "Method not allowed. Only POST is supported on /upload.",
        }),
      };
    }

    if (!event.body) {
      return { statusCode: 400, body: JSON.stringify({ error: "No body found" }) };
    }

    let bucketName, fileContent;
    try {
      const parsedBody = JSON.parse(event.body);
      bucketName = parsedBody.bucket;
      fileContent = parsedBody.file;
    } catch (err) {
      console.error("JSON parse error:", err);
      return { statusCode: 400, body: JSON.stringify({ error: "Invalid JSON body" }) };
    }

    if (!bucketName || !fileContent) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          error: "Missing 'bucket' or 'file' parameter.",
        }),
      };
    }

    try {
      const s3 = new S3Client({});
      const objectKey = `uploaded-${Date.now()}.txt`;
      const putCommand = new PutObjectCommand({
        Bucket: bucketName,
        Key: objectKey,
        Body: fileContent,
      });
      await s3.send(putCommand);

      return {
        statusCode: 200,
        body: JSON.stringify({
          message: `File '${objectKey}' created in bucket '${bucketName}'`,
        }),
      };
    } catch (error) {
      console.error("S3 error:", error);
      return { statusCode: 500, body: JSON.stringify({ error: "Could not write to S3" }) };
    }
  }

  // 3) Resource not found
  return {
    statusCode: 404,
    body: JSON.stringify({ error: `Unknown resource: ${resource}` }),
  };
};
