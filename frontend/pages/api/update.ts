import { Client } from "pg";
import { config } from "../../config";
import type { NextApiRequest, NextApiResponse } from "next";

const client = new Client(config);

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { email: email, number: number } = req.body;
  const queries = [
    "DROP TABLE IF EXISTS users",
    "CREATE TABLE IF NOT EXISTS users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), email STRING, message STRING)",
    `INSERT INTO users (id, email, message) VALUES (DEFAULT, '${email}', '${number}')`,
    "SELECT * FROM users",
  ];

  try {
    await client.connect();
    for (let n = 0; n < queries.length; n++) {
      let result = await client.query(queries[n]);
      if (result.rows) {
        result.rows.forEach((row) => {
          console.log(row.message);
        });
      }
    }
    await client.end();
    res.json({
      message: "Success!",
    });
  } catch (err: any) {
    res.status(500).json({
      message: err.message,
    });
  }
}
