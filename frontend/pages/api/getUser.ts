import { Pool } from "pg";
import { config } from "../../config";

const pool = new Pool(config);

export default async function handler(request: any, response: any) {
  const { email, number } = request.body;
  const queries = [
    "CREATE TABLE IF NOT EXISTS phone_numbers (email STRING NOT NULL PRIMARY KEY, number STRING)",
    ``,
  ];

  try {
    const client = await pool.connect();
    for (let n = 0; n < queries.length; n++) {
      await client.query(queries[n]);
    }
    response.json({});
  } catch (err: any) {
    response.status(500).json({
      message: err.message,
    });
  }
}
